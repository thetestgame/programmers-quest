from datetime import datetime
import enum

from quest.distributed import objects
from quest.engine import runtime


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkRejectCodes(enum.Enum):
    """
    """

    #"122" is the magic number for login problems.
    # See https://github.com/Astron/Astron/blob/master/doc/protocol/10-client.md
    NRC_INVALID_AUTH = 122

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class LoginManager(objects.QuestDistributedObjectGlobal):
    """
    """

    def generateInit(self):
        """
        """

        super().generateInit()
        self.notify.info(datetime.now().strftime("%H:%M:%S")+" LoginManager.generateInit() for "+str(self.doId))

    def login(self, username, password):
        """
        """

        # FIXME: Use TLS so that these are encrypted!
        self.notify.info(datetime.now().strftime("%H:%M:%S")+" LoginManager.login("+username+", <password>) in "+str(self.doId))
        self.sendUpdate("login", [username, password])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class LoginManagerAI(objects.QuestDistributedObjectGlobalAI):
    """
    """

    def generate(self):
        """
        """

        super().generate()
        self.notify.info(datetime.now().strftime("%H:%M:%S")+" LoginManagerAI.generate() for "+str(self.doId))

    def set_maproot(self, maproot_doId):
        """
        """

        self.notify.info(datetime.now().strftime("%H:%M:%S")+" LoginManagerAI.set_maproot("+str(maproot_doId)+") in "+str(self.doId))
        self.sendUpdate("set_maproot", [maproot_doId])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class LoginManagerUD(objects.QuestDistributedObjectGlobalUD):
    """
    """

    def generate(self):
        """
        """

        super().generate()
        self.notify.info(datetime.now().strftime("%H:%M:%S")+" LoginManagerUD.generate() for "+str(self.doId))

    def set_maproot(self, maproot_doId):
        """
        Tells the LoginManagerUD what maproot to notify on login.
        """

        self.notify.info(datetime.now().strftime("%H:%M:%S")+" LoginManagerUD.set_maproot("+str(maproot_doId)+") in "+str(self.doId))
        #self.maproot = DistributedMaprootUD(self.air)
        #self.maproot.generateWithRequiredAndId(maproot_doId, 0, 1)

    def login(self, username, password):
        """
        """

        clientId = self.air.get_msg_sender()
        print(datetime.now().strftime("%H:%M:%S")+" LoginManagerUD.login("+username+", <password>)  in "+str(self.doId)+" for client "+str(clientId))
        if (username == "guest") and (password == "guest"):
            # Authenticate a client
            # FIXME: "2" is the magic number for CLIENT_STATE_ESTABLISHED,
            # for which currently no mapping exists.
            self.air.setClientState(clientId, 2)

            # The client is now authenticated; create an Avatar
            #self.maproot.sendUpdate("createAvatar", # Field to call
            #                        [clientId])     # Arguments
            self.maproot.create_avatar(clientId)
            
            # log login
            self.notify.info("Login successful (user: %s)" % (username,))

        else:
            # Disconnect for bad auth and log attempt
            self.air.eject(clientId, NetworkRejectCodes.NRC_INVALID_AUTH, "Bad credentials")
            self.notify.info("Ejecting client for bad credentials (user: %s)" % (username,))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#