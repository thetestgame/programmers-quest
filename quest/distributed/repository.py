from distutils.log import error
from email import message
from panda3d import core as p3d
from panda3d_astron import repository as astron
from pytest import fail, param

from quest.distributed import constants
from quest.framework import singleton, localizer
from quest.engine import prc, runtime, core, logging
from quest.gui import elements as gui_styles
from quest.gui import flow
from quest.login import screen as login_screen

from direct.distributed import MsgTypes
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm import FSM

from playfab import PlayFabServerAPI
import traceback
import sys

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class NetworkRepositoryConstants(object):
    """
    Constants for the quest module network repositories
    """

    NETWORK_DC_FILES = ['config/direct.dc', 'config/quest.dc']
    NETWORK_METHOD = astron.AstronClientRepository.CM_NET

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestNetworkRepository(singleton.Singleton):
    """
    Base class for quest module network repositories
    """

    def __init__(self):
        super().__init__()
        self.notify = logging.get_notify_category(type(self).__name__)
        self.notify.setInfo(True)
        self.GameGlobalsId = constants.NetworkGlobalObjectIds.GLOBAL_GAME_ROOT.value

        self.active_shard_map = {}
        self.active_shard = None

    def configure_global_managers(self) -> None:
        """
        Configures all our global network objects
        """
        
        self.login_manager = self.generateGlobalObject(constants.NetworkGlobalObjectIds.DOG_LOGIN_MANAGER.value, 'QuestLoginManager')
        self.event_manager = self.generateGlobalObject(constants.NetworkGlobalObjectIds.DOG_EVENT_MANAGER.value, 'QuestEventManager')
        self.avatar_manager = self.generateGlobalObject(constants.NetworkGlobalObjectIds.DOG_AVATAR_MANAGER.value, 'QuestAvatarManager')

    def handle_connection_established(self) -> None:
        """
        Handles post connection established operations on the repository instance
        """

        # Perform our post connect setup
        self.configure_global_managers()

    def has_available_shards(self) -> None:
        """
        Checks if there are any available shards
        """

        for shard in list(self.active_shard_map.values()):
            if shard.get_available():
                return True

        return False

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestClientRepository(astron.AstronClientRepository, FSM.FSM, QuestNetworkRepository):
    """
    Client Astron repository instance for the Programmers Quest! game client
    """

    def __init__(self, *args, **kwargs):
        self.notify.setInfo(True)
        kwargs['dcFileNames'] = NetworkRepositoryConstants.NETWORK_DC_FILES
        kwargs['connectMethod'] = NetworkRepositoryConstants.NETWORK_METHOD
        kwargs['threadedNet'] = prc.get_prc_bool('want-threaded-network', False)

        QuestNetworkRepository.__init__(self)
        astron.AstronClientRepository.__init__(self,*args, **kwargs)
        FSM.FSM.__init__(self, '%s-FSM' % self.__class__.__name__)

        runtime.cr = self
        runtime.base.cr = self

        # Callback events. These names are "magic" (defined in AstronClientRepository)
        self.accept("CLIENT_HELLO_RESP", self.client_is_handshaked)
        self.accept("CLIENT_EJECT", self.ejected)
        self.accept("LOST_CONNECTION", self.lost_connection)

        self._server_shard_interest_handle = None
        self._status_dialog = gui_styles.QuestDirectDialog(message='test')
        self._showing_connection_failure = False

    def connect(self, host: str, port: int) -> None:
        """
        Attempts to establish a connection to the Astron ClientAgent instance
        """

        self.request('Connect', host, port)

    def _set_network_status_message(self, message: str = None, callback = None) -> None:
        """
        """

        if message is None:
            self._status_dialog.hide()
        else:
            self.notify.info('NetworkEvent: %s' % message)
            self._status_dialog.set_message(message)
            self._status_dialog.show()

    def enterConnect(self, host: str, port: int) -> None:
        """
        """

        url = p3d.URLSpec()
        url.setServer(host)
        url.setPort(port)

        self.notify.info('Connecting to %s:%s...' % (host, port))
        super().connect([url],                          
            successCallback = self.connection_success,
            failureCallback = self.connection_failure)

    # Connection established. Send CLIENT_HELLO to progress from NEW to UNKNOWN.
    # Normally, there could be code here for things to do before entering making
    # the connection and actually interacting with the server.
    def connection_success(self, *args) -> None:
        """
        Handles the connection established event once the repository connects to Astron's CA
        """

        self.send_hello()

    def send_hello(self) -> None:
        """
        Sends our hello message to the Astron server cluster ClientAgent
        """

        client_dc_hash = self.get_dc_file().get_hash()
        client_version = constants.APPLICATION_VERSION
        
        if prc.has_prc_key('manual-dc-hash'):
            client_dc_hash = int(prc.get_prc_string('manual-dc-hash'), 16)

        if runtime.dev:
            client_version = 'quest-dev' # Development always runs as quest-dev

        self.notify.info('Attempting to handshake with server gateway')
        dg = PyDatagram()
        dg.add_uint16(MsgTypes.CLIENT_HELLO)
        dg.add_uint32(client_dc_hash)
        dg.add_string(client_version)
        self.send(dg)

    def connection_failure(self, *args, **kwargs) -> None:
        """
        Called when the connection to the ClientAgent cannot be established
        """

        self.demand('ConnectionFailure', 1, 'Connection could not be established', self.connection_failure.__name__)

    def lost_connection(self) -> None:
        """
        Called when the connection to the ClientAgent is lost.
        """

        if not self._showing_connection_failure:
            self.demand('ConnectionFailure', 2, 'Connection to the game server was lost', self.lost_connection.__name__)

    def ejected(self, error_code: int, reason: str) -> None:
        """
        Called when the ClientAgent ejects us from the game network.
        """

        self.demand('ConnectionFailure', error_code, reason, self.ejected.__name__)

    def enterConnectionFailure(self, error_code: int, reason: str, failure_type: str) -> None:
        """
        """

        if self._showing_connection_failure:
            return
        self._showing_connection_failure = True

        self.notify.warning('Connection to the game server has been closed (Type: %s | Code: %s | Reason: %s)' % (failure_type, error_code, reason))
        message_code = error_code
        if not localizer.ApplicationLocalizer.has_network(message_code):
            message_code = 3
        
        error_message = localizer.ApplicationLocalizer.get_network(message_code) % { 'error_code': error_code, 'reason': reason}
        self._set_network_status_message(error_message, callback=self._handle_connection_failure_popup_callback)
        self.stopHeartbeat()

    def exitConnectionFailure(self) -> None:
        """
        """

        self._showing_connection_failure = False

    def _handle_connection_failure_popup_callback(self, option: str) -> None:
        """
        """

        sys.exit()

    def client_is_handshaked(self, *args):
        """
        Handles the handshake completed callback signaling we are ready to start performing network operations
        """

        self.notify.info('ClientAgent handshake complete')
        self.handle_connection_established()
        self.startHeartbeat()
        self.request('Login')

    def enterLogin(self) -> None:
        """
        Enters the login connection management FSM state. Attempts to authenticate with the Astron cluster instnace
        """

        done_event = 'client-login-screen-complete'
        #self.login_screen = login_screen.ClientLoginScreen('config/screens/clientLoginScreen.ini', done_event)
        #self.login_screen.setup()

        self.login_manager.configure_authentication_handlers(
            success=self.client_is_authenticated,
            failure=self.client_authentication_failure)

        ## Start the authentication process with our startup arguments
        pq_startup_email = runtime.application.get_startup_variable('PQ_EMAIL')
        pq_startup_password = runtime.application.get_startup_variable('PQ_PASSWORD')
        self.login_manager.authenticate_with_email_password(pq_startup_email, pq_startup_password)

    def client_is_authenticated(self) -> None:
        """
        Handles the authentication success callback signaling we can now ready to enter the game world
        """

        self.notify.info('Authentication with UberDOG complete.')
        self.request('WaitForBaseInterest')
 
    def client_authentication_failure(self, code: int, message: str) -> None:
        """
        Handles the authentication failure callback. Informs the user of the issue.
        """

        self._set_network_status_message('Authentication failed (%s). Reason: %s' % (code, message))

    def enterWaitForBaseInterest(self) -> None:
        """
        """

        self._set_network_status_message('Waiting for server to assign base interest...')
        self.accept_once('CLIENT_ADD_INTEREST_MULTIPLE', self._handle_base_interest_add_callback)

    def _handle_base_interest_add_callback(self, context: int, interest_id: int, parent_id: int, zone_ids: list) -> None:
        """
        """

        # Verify this is the interest handle callback we are looking for. If not accept again and wait
        if not all(zone_id in constants.STARTING_NETWORK_ZONES for zone_id in zone_ids):
            self.accept_once('CLIENT_ADD_INTEREST_MULTIPLE', self._handle_base_interest_add_callback)
            return

        self.accept_once(self.getAllInterestsCompleteEvent(), self._handle_base_interest_complete_callback) #TODO: properly filter to only the base interests

    def _handle_base_interest_complete_callback(self) -> None:
        """
        """

        # Check if we have any available shards
        self._set_network_status_message('Base network interest assigned. Checking for server shards...')
        if not self.has_available_shards():
            self.request('NoServers')
        else:
            self.request('ChooseCharacter')

    def enterNoServers(self) -> None:
        """
        """

        self.notify.warning('Failed to connect to game server. There are no shards available to connect to')
        #error_message = localizer.ApplicationLocalizer.get_network('NO_SHARDS_AVAILABLE')
        #runtime.gui_manager.show_popup_message(error_message, callback=self._handle_no_servers_popup_callback)

    def _handle_no_servers_popup_callback(self, option: str) -> None:
        """
        """

        sys.exit()

    def enterChooseCharacter(self) -> None:
        """
        """

        first_district = list(self.active_shard_map.values())[0]
        self.notify.info('Connecting to shard: %s' % first_district.get_name())

        self._set_network_status_message(None)
        self.avatar_manager.retrieve_potential_characters()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestInternalRepository(astron.AstronInternalRepository, QuestNetworkRepository):
    """
    Internal Astron repository instance for the Programmers Quest! AI and UberDOG server instances
    """

    def __init__(self, base_channel: int, state_server_channel: int, db_server_channel: int, dc_suffix='AI'):
        QuestNetworkRepository.__init__(self)
        self.notify.info('Starting internal repository (Base: %d | State server: %d | Database: %d | Suffix: %s)' % 
            (base_channel, state_server_channel, db_server_channel, dc_suffix))
        
        threaded_net = prc.get_prc_bool('want-threaded-network', False)
        astron.AstronInternalRepository.__init__(self, base_channel, 
            state_server_channel, NetworkRepositoryConstants.NETWORK_DC_FILES, 
            dc_suffix, NetworkRepositoryConstants.NETWORK_METHOD, threaded_net)

        runtime.air = self
        runtime.base.air = self
        self.db_server_channel = db_server_channel

    def connect(self, astron_ip: str, astron_port: int) -> None:
        """
        Connects the internal repository instance to Astron's Message Director instance
        """

        self.notify.info('Connecting to Astron MD at %s:%s' % (astron_ip, astron_port))
        super().connect(astron_ip, astron_port)

    def get_character_id_from_sender(self) -> int:
        """
        """
        
        return self.get_msg_sender() & 0xFFFFFFFF

    def get_account_id_from_sender(self) -> int:
        """
        """

        return (self.get_msg_sender() >> 32) & 0xFFFFFFFF

    def handleConnected(self) -> None:
        """
        Handles the connection established event once the repository connects to Astron's MD
        """

        super().handleConnected()
        self.handle_connection_established()

    def writeServerEvent(self, logtype: str, *args, **kwargs) -> None:
        """
        Custom override of the Astron writeServerEvent to pipe server events to the Azure PlayFab PlayStream system as well as
        the internal Astron EventLogger server instance
        """

        # Write to Astron's internal event logger
        super().writeServerEvent(logtype, *args, **kwargs)

        # Write to PlayFab's event stream
        logtype = logtype.replace('-', '_')
        request = {
            'EventName': logtype,
            'Body': kwargs
        }

        PlayFabServerAPI.WriteTitleEvent(request, self._handle_write_title_event_callback)

    def _handle_write_title_event_callback(self, results: dict, error: dict) -> None:
        """
        Handles the results from the WriteTitleEvent api request
        """

    def readerPollOnce(self) -> None:
        """
        Custom implementation of readerPollOnce to catch network errors and
        handle problems safely on a per connection basis rather then bringing
        the whole site down.
        """

        try:
            super().readerPollOnce()
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception as e:
            self.eject(self.getMsgSender(), 4, '')
            if runtime.dev:
                print(traceback.format_exc())

        return 1

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #