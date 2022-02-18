from panda3d import core as p3d

from quest.distributed import astron, constants
from quest.framework import singleton
from quest.engine import core, runtime

import sys

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestClientNetworkManager(singleton.Singleton, core.QuestObject):
    """
    """

    def __init__(self, *args, **kwargs):
        core.QuestObject.__init__(self)

        self.cr = astron.AstronClientRepository(
            dcFileNames = ["config/quest.dc"],
            connectMethod = astron.AstronClientRepository.CM_NET)
        runtime.base.cr = self.cr
        
        self.active_shard_map = {}
        self.active_shard = None

        # Callback events. These names are "magic" (defined in AstronClientRepository)
        self.accept("CLIENT_HELLO_RESP", self.client_is_handshaked)
        self.accept("CLIENT_EJECT", self.ejected)
        self.accept("CLIENT_OBJECT_LEAVING", self.avatar_leaves)
        self.accept("CLIENT_OBJECT_LEAVING_OWNER", self.avatar_leaves_owner)
        self.accept("LOST_CONNECTION", self.lost_connection)

        url = p3d.URLSpec()
        url.setServer("127.0.0.1")
        url.setPort(6667)
        # FIXME: No idea why this doesn't work instead...
        # url = URLSpec("127.0.0.1", 6667)
        self.notify.debug("Connecting...")
        self.cr.connect([url],
                          successCallback = self.connection_success,
                          failureCallback = self.connection_failure)

    # Connection established. Send CLIENT_HELLO to progress from NEW to UNKNOWN.
    # Normally, there could be code here for things to do before entering making
    # the connection and actually interacting with the server.
    def connection_success(self, *args):
        """
        """

        self.cr.sendHello("quest-dev")

    def connection_failure(self):
        """
        """

        self.notify.error("Failed to connect")
        sys.exit()

    def lost_connection(self):
        """
        """

        self.notify.error("Lost connection")
        sys.exit()

    def ejected(self, error_code, reason):
        """
        """

        self.notify.error("Ejected! %d: %s" % (error_code, reason))
        sys.exit()

    def client_is_handshaked(self, *args):
        """
        """

        login_manager = self.cr.generateGlobalObject(constants.NetworkGlobalObjectIds.DOG_LOGIN_MANAGER, 'LoginManager')
        # Log in and receive; leads to enter_owner (ownership of avatar)
        login_manager.login("guest", "guest")

    def avatar_leaves(self, do_id):
        print("Avatar leaving: "+str(do_id))

    def avatar_leaves_owner(self, do_id):
        print("AvatarOV leaving: "+str(do_id))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#