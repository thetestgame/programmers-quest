from sre_constants import SUCCESS
from panda3d import core as p3d
from panda3d_astron import repository as astron

from quest.distributed import constants
from quest.framework import singleton
from quest.engine import prc, runtime

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

        self.active_shard_map = {}
        self.active_shard = None

    def configure_global_managers(self) -> None:
        """
        Configures all our global network objects
        """
        
        self.login_manager = self.generateGlobalObject(constants.NetworkGlobalObjectIds.DOG_LOGIN_MANAGER, 'QuestLoginManager')

    def handle_connection_established(self) -> None:
        """
        Handles post connection established operations on the repository instance
        """

        # Perform our post connect setup
        self.configure_global_managers()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestClientRepository(astron.AstronClientRepository, QuestNetworkRepository):
    """
    Client Astron repository instance for the Programmers Quest! game client
    """

    def __init__(self, *args, **kwargs):
        kwargs['dcFileNames'] = NetworkRepositoryConstants.NETWORK_DC_FILES
        kwargs['connectMethod'] = NetworkRepositoryConstants.NETWORK_METHOD
        super().__init__(*args, **kwargs)

        runtime.cr = self
        runtime.base.cr = self

        # Callback events. These names are "magic" (defined in AstronClientRepository)
        self.accept("CLIENT_HELLO_RESP", self.client_is_handshaked)
        self.accept("CLIENT_EJECT", self.ejected)
        self.accept("CLIENT_OBJECT_LEAVING", self.avatar_leaves)
        self.accept("CLIENT_OBJECT_LEAVING_OWNER", self.avatar_leaves_owner)
        self.accept("LOST_CONNECTION", self.lost_connection)

    def connect(self, host: str, port: int) -> None:
        """
        Attempts to establish a connection to the Astron ClientAgent instance
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

        self.sendHello(constants.APPLICATION_VERSION)

    def connection_failure(self) -> None:
        """
        """

        self.notify.error("Failed to connect")

    def lost_connection(self) -> None:
        """
        """

        self.notify.error("Lost connection")

    def ejected(self, error_code: int, reason: str) -> None:
        """
        """

        self.notify.error("Ejected! %d: %s" % (error_code, reason))

    def client_is_handshaked(self, *args):
        """
        Handles the handshake completed callback signaling we are ready to start performing network operations
        """

        self.handle_connection_established()
        self.login_manager.initiate_authentication(
            success=self.client_is_authenticated,
            failure=self.client_authentication_failure)

    def client_is_authenticated(self) -> None:
        """
        Handles the authentication success callback signaling we can now ready to enter the game world
        """

        # TEMP
        from quest.characters import player
        s = player.PlayerCharacter('characters/playerCharacter.ini')
        s.setup()
        s.root.reparent_to(runtime.render)
        s.set_local(True)
        runtime.camera_mgr.camera_follow_target = s.root

    def client_authentication_failure(self, code: int, message: str) -> None:
        """
        Handles the authentication failure callback. Informs the user of the issue.
        """

    def avatar_leaves(self, do_id: int) -> None:
        """
        """

        print("Avatar leaving: "+str(do_id))

    def avatar_leaves_owner(self, do_id: int) -> None:
        """
        """

        print("AvatarOV leaving: "+str(do_id))

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestInternalRepository(astron.AstronInternalRepository, QuestNetworkRepository):
    """
    Internal Astron repository instance for the Programmers Quest! AI and UberDOG server instances
    """

    def __init__(self, baseChannel, serverId, dcSuffix='AI'):
        threaded_net = prc.get_prc_bool('want-threaded-network', False)
        super().__init__(baseChannel, serverId, 
            NetworkRepositoryConstants.NETWORK_DC_FILES, 
            dcSuffix, NetworkRepositoryConstants.NETWORK_METHOD, threaded_net)

        runtime.air = self
        runtime.base.air = self
        self.districtId = self.GameGlobalsId = baseChannel

    def handleConnected(self) -> None:
        """
        Handles the connection established event once the repository connects to Astron's MD
        """

        super().handleConnected()
        self.handle_connection_established()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #