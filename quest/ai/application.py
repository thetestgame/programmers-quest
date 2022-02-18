from quest.framework import application
from quest.distributed import constants
from quest.ai import repository

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAIApplication(application.QuestApplication):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_game(self) -> None:
        """
        Performs game setup operations on the server application
        """

        super().setup_game()
        self.connect_to_astron()

    def connect_to_astron(self) -> None:
        """
        Establishes our connection to the Astron MessageDirector
        """

        shard_channel = int(self.get_startup_variable('AI_SHARD_CHANNEL', constants.NetworkChannels.AI_DEFAULT_CHANNEL))
        state_server_channel = int(self.get_startup_variable("STATE_SERVER_CHANNEL", constants.NetworkChannels.STATE_SERVER_DEFAULT_CHANNEL))
        db_server_channel = int(self.get_startup_variable('DATABASE_SERVER_CHANNEL', constants.NetworkChannels.DATABASE_SERVER_DEFAULT_CHANNEL))
        shard_name = self.get_startup_variable('SHARD_NAME', 'Hacker Valley')

        # Establish our repository connection
        self.air = repository.QuestAIRepository.instantiate_singleton(
            shard_name=shard_name,
            base_channel=shard_channel, 
            state_server_channel=state_server_channel,
            db_server_channel=db_server_channel)
        
        astron_address = self.get_startup_variable('ASTRON_IP', '127.0.0.1').split(':')
        astron_ip = astron_address[0]
        astron_port = astron_address[1]
        self.air.connect(astron_ip, astron_port)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Programmer's Quest MMO AI server application
    """ 

    kwargs['headless'] = True
    kwargs['application_cls'] = QuestAIApplication

    return application.main(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#