from numpy import single
from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import registry, utilities, singleton, configurable

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldManagerBase(singleton.Singleton, configurable.Configurable, core.QuestObject):
    """
    """

    def __init__(self, config_path: str):
        self.configured_worlds = {}

        singleton.Singleton.__init__(self)
        configurable.Configurable.__init__(self, config_path)
        core.QuestObject.__init__(self)

    def load_worlds_data(self, data: dict) -> None:
        """
        """

        self.configured_worlds = data

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldManager(WorldManagerBase):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldManagerAI(WorldManagerBase):
    """
    """

    def __init__(self, air: object, config_path: str):
        super().__init__(config_path)

        self._air = air
        self.loaded_worlds = {}

    def generate_server_worlds(self) -> None:
        """
        """

        self.notify.info('Generating %d worlds...' % len(self.configured_worlds.keys()))
        for world_id, world_config in self.configured_worlds.items():
            world_instance = self._generate_server_world(world_id, world_config)
            self.loaded_worlds[world_id] = world_instance

    def _generate_server_world(self, world_id: int, world_config_file: str) -> object:
        """
        """

        print(world_config_file)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#