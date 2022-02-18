from quest.distributed import objects
from quest.engine import runtime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedShardServerBase(object):
    """
    Base shared class for all shard server objects
    """

    def __init__(self):
        self.name = 'Undefined'
        self.available = 0

    def _get_repository() -> object:
        """
        Returns our repository instance
        """

        repository = None
        if runtime.has_cr():
            repository = runtime.cr
        elif runtime.has_air():
            repository = runtime.air

        assert repository != None, 'No repository found on runtime'
        return repository

    def announceGenerate(self) -> None:
        """
        """

        super().announceGenerate()

        repository = self._get_repository()
        repository.active_shard_map[self.doId] = self
        self.send_update_event()

    def delete(self) -> None:
        """
        """

        if runtime.has_cr():
            if runtime.cr.active_shard is self:
                runtime.cr.active_shard = None
        
        repository = self._get_repository()
        if self.doId in repository.active_shard_map:
            del repository.active_shard_map[self.doId]

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

    def get_available(self) -> bool:
        """
        """

        return self.available
    
    def get_name(self) -> str:
        """
        """

        return self.name

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedShardServer(objects.QuestDistributedObject, DistributedShardServerBase):
    """
    Client side implementation of the distributed shard server object used to identify AI server instances
    """

    neverDisable = 1 # Legacy magic value from Pandas original DO implementation

    def __init__(self, cr: object):
        super().__init__(cr)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedShardServerAI(objects.DistributedObjectAI, DistributedShardServerBase):
    """
    AI side implementation of the distributed shard server object used to identify AI server instances
    """

    def __init__(self, air: object, name: str = "Undefined"):
        super().__init__(air)
        self.air = air
        self.air.active_shard = self
        
    def delete(self) -> None:
        """
        """

        self.ignore_all()
        self.b_set_available(0)
        
        super().delete(self)
    
    def d_set_available(self, available: bool) -> None:
        """
        """

        self.send_update("setAvailable", [available])

    def b_set_available(self, available: bool) -> None:
        """
        """

        self.set_available(available)
        self.d_set_available(available)
               
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

class DistributedShardServerUD(objects.QuestDistributedObjectUD, DistributedShardServerBase):
    """
    UberDOG side implementation of the distributed shard server object used to identify AI server instances
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#