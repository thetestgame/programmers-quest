from datetime import datetime
import enum
from unittest import result

from pytest import fail

from quest.distributed import objects
from quest.engine import runtime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class AuthResultcode(enum.Enum):
    """
    """

    ARC_SUCCESS = 200
    ARC_INVALID_TOKEN = 100

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestLoginManager(objects.QuestDistributedObjectGlobal):
    """
    """

    def __init__(self, cr):
        super().__init__(cr)

        self._auth_success_callback = None
        self._auth_failure_callback = None

    def initiate_authentication(self, success: object = None, failure: object = None) -> None:
        """
        Initiates the authentication request process with the UberDOG server instance
        """

        self._auth_success_callback = success
        self._auth_failure_callback = failure
        self.d_request_authentication('quest-dev') #TODO
        
    def d_request_authentication(self, token: str) -> None:
        """
        Sends an authentication request to the game server
        """

        self.send_update('request_authentication', [token])

    def handle_request_authentication_result(self, code: int, message: str) -> None:
        """
        Handles the authentication results from the UberDOG server
        """

        if code != AuthResultcode.ARC_SUCCESS.value and self._auth_failure_callback != None:
            self._auth_failure_callback(code, message)
        elif self._auth_success_callback != None:
            self._auth_success_callback()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestLoginManagerAI(objects.QuestDistributedObjectGlobalAI):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestLoginManagerUD(objects.QuestDistributedObjectGlobalUD):
    """
    """

    # "122" is the magic number for login problems.
    # See https://github.com/Astron/Astron/blob/master/doc/protocol/10-client.md
    ASTRON_CA_INVALID_AUTH = 122

    def request_authentication(self, token: str) -> None:
        """
        """

        client_id = self.air.get_msg_sender()
        if (token == "quest-dev"):
            # Authenticate a client
            # FIXME: "2" is the magic number for CLIENT_STATE_ESTABLISHED,
            # for which currently no mapping exists.
            self.air.setClientState(client_id, 2)
            self.notify.info("Login successful (user: %s)" % (token,))
            self.send_authentication_result(client_id, AuthResultcode.ARC_SUCCESS)
        else:
            # Disconnect for bad auth and log attempt
            self.air.eject(client_id, self.ASTRON_CA_INVALID_AUTH, "Bad credentials")
            self.notify.info("Ejecting client for bad credentials (user: %s)" % (token,))

    def send_authentication_result(self, channel_id: int, result_code: AuthResultcode, message: str = 'Ok') -> None:
        """
        Sends the authentication result to a client instance
        """

        self.sendUpdateToChannel(channel_id, 'handle_request_authentication_result', [result_code.value, message])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class LoginManagerOperation(object):
    """
    Base class for all LoginManager server operations
    """

    def __init__(self, login_manager: QuestLoginManagerUD, sender: object):
        self._login_manager = login_manager
        self._sender = sender
        self._callback = None

    @property
    def login_manager(self) -> QuestLoginManagerUD:
        """
        Returns our login_manager variable instance as a property
        """

        return self._login_manager

    @property
    def sender(self) -> object:
        """
        Returns our sender variable instance as a property
        """

        return self._sender

    @property
    def callback(self) -> object:
        """
        Returns our callback variable instance as a property
        """

        return self._callback

    def set_callback(self, callback: object) -> None:
        """
        Sets our callback variable instance
        """

        return self._callback

    def _handle_done(self) -> None:
        """
        """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
