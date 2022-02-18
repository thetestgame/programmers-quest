from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import application
from quest.distributed import repository, constants

import argparse

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAIApplication(application.QuestApplication):
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

        shard_channel = int(self.get_startup_variable('AI_SHARD_CHANNEL', constants.NetworkChannels.AI_DEFAULT_CHANNEL))
        state_server_channel = int(self.get_startup_variable("STATE_SERVER_CHANNEL", constants.NetworkChannels.STATE_SERVER_DEFAULT_CHANNEL))

        # Establish our repository connection
        self.air = repository.QuestInternalRepository.instantiate_singleton(
            baseChannel=shard_channel, 
            serverId=state_server_channel)
        self.air.connect("127.0.0.1", 7199)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Programmer's Quest MMO AI server application
    """ 

    kwargs['headless'] = True
    kwargs['application_cls'] = QuestAIApplication

    return application.main(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#