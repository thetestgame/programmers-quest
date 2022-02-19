from quest.framework import application
from quest.distributed import constants
from quest.uberdog import repository

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestUberDOGApplication(application.QuestApplication):
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

        # Establish our repository connection
        state_server_channel = int(self.get_startup_variable("STATE_SERVER_CHANNEL", constants.NetworkChannels.STATE_SERVER_DEFAULT_CHANNEL))
        db_server_channel = int(self.get_startup_variable('DATABASE_SERVER_CHANNEL', constants.NetworkChannels.DATABASE_SERVER_DEFAULT_CHANNEL))

        self.air = repository.QuestUberDOGRepository.instantiate_singleton(
            state_server_channel=state_server_channel,
            db_server_channel=db_server_channel,)
        self.air.districtId = constants.NetworkChannels.UBERDOG_DEFAULT_CHANNEL
        self.air.shard_id = self.air.districtId

        astron_address = self.get_startup_variable('ASTRON_IP', '127.0.0.1').split(':')
        astron_ip = astron_address[0]
        astron_port = astron_address[1]
        self.air.connect(astron_ip, astron_port)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Programmer's Quest MMO UberDOG server application
    """ 

    kwargs['headless'] = True
    kwargs['application_cls'] = QuestUberDOGApplication

    return application.main(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#