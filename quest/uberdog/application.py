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
        state_server_channel = int(self.get_startup_variable("STATE_SERVER_CHANNEL", constants.NetworkChannels.STATE_SERVER_DEFAULT_CHANNEL))
        self.air = repository.QuestInternalRepository.instantiate_singleton(
            baseChannel=constants.NetworkChannels.UBERDOG_DEFAULT_CHANNEL, 
            serverId=state_server_channel,
            dcSuffix="UD")
        self.air.connect("127.0.0.1", 7199)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Programmer's Quest MMO UberDOG server application
    """ 

    kwargs['headless'] = True
    kwargs['application_cls'] = QuestUberDOGApplication

    return application.main(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#