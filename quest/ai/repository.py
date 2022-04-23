from quest.framework import application
from quest.distributed import repository, constants, shard
from quest.engine import runtime
from quest.world import manager

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAIRepository(repository.QuestInternalRepository):
    """
    """

    def __init__(self, shard_name, base_channel, state_server_channel, db_server_channel, dcSuffix='AI'):
        super().__init__(base_channel, state_server_channel, db_server_channel, dcSuffix)
        self.shard_id = self.allocateChannel()
        self.districtId = self.shard_id
        self.shard_name = shard_name

        self.shard_instance = None

    def handle_connection_established(self) -> None:
        """
        Handles post connection established operations on the repository instance
        """
        
        super().handle_connection_established()

        # Generate our shard server instance
        self.notify.info('Creating Shard Server instance (%s)' % self.shard_id)
        self.shard_instance = shard.DistributedShardServerAI(self, self.shard_name)
        self.shard_instance.generateWithRequiredAndId(self.shard_id, self.getGameDoId(), constants.NetworkZones.QUEST_ZONE_ID_SHARDS.value)
        self.shard_instance.setAI(self.ourChannel)

        # Generate our server objects
        self.generate_global_objects()
        self.generate_world_objects()

        # Set our selves as ready
        self.shard_instance.b_set_available(True)
        self.notify.info('Server Shard (%s) server is ready.' % self.shard_name)

    def generate_global_objects(self) -> None:
        """
        """

        self.notify.info('Generating server global objects')

    def generate_world_objects(self) -> None:
        """
        """

        self.notify.info('Generating server side world information')
        self.world_manager = manager.WorldManagerAI(self, 'config/worldManager.ini')
        self.world_manager.generate_server_worlds()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
