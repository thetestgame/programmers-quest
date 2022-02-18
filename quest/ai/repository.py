from quest.framework import application
from quest.distributed import repository, constants, shard
from quest.engine import runtime

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
        self.shard_instance = shard.DistributedShardServerAI(self, self.shard_name)
        self.shard_instance.generateWithRequiredAndId(self.shard_id, self.getGameDoId(), constants.NetworkZones.QUEST_ZONE_ID_SHARDS)
        self.shard_instance.setAI(self.ourChannel)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
