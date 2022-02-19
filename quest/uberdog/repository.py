from quest.framework import application
from quest.distributed import repository, constants, game
from quest.engine import runtime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestUberDOGRepository(repository.QuestInternalRepository):
    """
    """

    def __init__(self, state_server_channel, db_server_channel):
        super().__init__(constants.NetworkChannels.UBERDOG_DEFAULT_CHANNEL, state_server_channel, db_server_channel, 'UD')

    def handle_connection_established(self) -> None:
        """
        Handles post connection established operations on the repository instance
        """
        
        super().handle_connection_established()

        # Create our distributed root game object
        self.notify.info('Generateing root game object (%d)...' % self.getGameDoId())
        self.root_game_obj = game.DistributedGameAI(self)
        self.root_game_obj.generateWithRequiredAndId(self.getGameDoId(), 0, 1)

        self.generate_global_objects()
        self.notify.info('UberDOG server ready.')

    def generate_global_objects(self) -> None:
        """
        """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
