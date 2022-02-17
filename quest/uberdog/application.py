from sqlite3 import connect
from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import application
from quest.distributed import repository, constants

import argparse

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestUberDOGApplication(application.QuestApplication):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_game(self) -> None:
        """
        """

        super().setup_game()
        self.connect_to_astron()

    def connect_to_astron(self) -> None:
        """
        Establishes our connection to the Astron MessageDirector
        """

        # Establish our repository connection
        self.base.air = repository.AstronInternalRepository(
            baseChannel=constants.NetworkChannels.UBERDOG_CHANNEL, 
            serverId=constants.NetworkChannels.STATE_SERVER_CHANNEL,
            dcFileNames=['config/quest.dc'],
            dcSuffix="UD",
            connectMethod=repository.AstronInternalRepository.CM_NET)
        self.base.air.connect("127.0.0.1", 7199)
        self.districtId = self.base.air.GameGlobalsId = constants.NetworkChannels.UBERDOG_CHANNEL

        # Create our global object instances
        self.login_manager = self.base.air.generateGlobalObject(constants.NetworkGlobalObjectIds.DOG_LOGIN_MANAGER, 'LoginManager')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Programmer's Quest MMO UberDOG server application
    """ 

    parser = argparse.ArgumentParser(description="Programmer's Quest UberDOG server")
    #parser.add_argument('-p', '--port', type=int, default=9099, help='Port to listen for incoming connections against')

    #parsed_args = parser.parse_args()
    #startup_prc = 'server-port %d\n' % parsed_args.port

    kwargs['headless'] = True
    #kwargs['startup_prc'] = startup_prc
    kwargs['application_cls'] = QuestUberDOGApplication

    return application.main(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#