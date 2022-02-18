from quest import client
from quest.distributed import objects
from quest.engine import runtime
from quest.client import network as client_network

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedShardServer(objects.QuestDistributedObject):
    """
    """

    neverDisable = 1 # Legacy magic value from Pandas original DO implementation

    def __init__(self, cr: object):
        super().__init__(cr)

        self.name = 'Undefined'
        self.available = 0
        self.playerCount = 0
        self.newPlayerCount = 0

    def announceGenerate(self) -> None:
        """
        """

        super().announceGenerate()

        cr = client_network.QuestClientNetworkManager.get_singleton()
        cr.active_shard_map[self.doId] = self
        self.send_update_event()

    def delete(self) -> None:
        """
        """

        cr = client_network.QuestClientNetworkManager.get_singleton()
        if cr.active_shard is self:
            cr.active_shard = None
        
        if self.doId in cr.active_shard_map:
            del cr.active_shard_map[self.doId]

        super().delete()
        self.send_update_event()

    def send_update_event(self) -> None:
        """
        """

        runtime.messenger.send('shardListUpdated')

    def set_available(self, available: bool) -> None:
        """
        """

        self.available = available
        self.send_update_event()

    def set_name(self, name: str) -> None:
        """
        """

        self.name = name
        self.send_update_event()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedShardServerAI(objects.DistributedObjectAI):
    """
    """

    def __init__(self, air: object, name: str = "Undefined"):
        super().__init__(air)
        self.air = air
        self.name = name
        self.available = 0
        
    def delete(self):
        self.ignore_all()
        self.b_set_available(0)
        
        super().delete(self)        
    
    def get_available(self) -> bool:
        """
        """

        return self.available
    
    def get_name(self) -> str:
        """
        """

        return self.name
    
    def set_available(self, available: bool) -> None:
        """
        """

        self.available = available
    
    def d_set_available(self, available: bool) -> None:
        """
        """

        self.send_update("setAvailable", [available])

    def b_set_available(self, available: bool) -> None:
        """
        """

        self.set_available(available)
        self.d_set_available(available)
            
    def set_name(self, name: str) -> None:
        """
        """

        self.name = name
               
    def d_set_name(self, name: str) -> None:
        """
        """

        self.send_update("set_name", [name])

    def b_set_name(self, name: str) -> None:
        """
        """

        self.set_name(name)
        self.d_set_name(name)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedShardServerUD(objects.QuestDistributedObjectUD):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#