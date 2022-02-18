from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import application, utilities
from quest.client import flow, network, settings, camera
from quest.world import world

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClientApplication(application.QuestApplication):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_framework(self) -> None:
        """
        """
        
        super().setup_framework()

        # Load our user defined settings into memory and apply them to the application and engine runtime
        local_settings = settings.LocalClientSettings('user_settings.ini' if runtime.dev else utilities.get_local_data_path('user_settings.ini'))
        self.client_settings = settings.ClientSettings.instantiate_singleton('config/defaultSettings.ini', local_settings)
        self.client_settings.set_options_before_engine_start()
        local_settings.write()

    def setup_engine(self) -> None:
        """
        """
        
        super().setup_engine()
        self.client_settings.set_options_after_engine_start()

        # Configure our task threads if configured in the application's runtime configuration
        utilities.create_thread('tile-layer-chain', prc_check='want-threaded-tilemap')
        utilities.create_thread('world-culling-chain', prc_check='want-threaded-world-cull')

    def setup_game(self) -> None:
        """
        """
        
        super().setup_game()
        
        flow.ClientFlowManager.instantiate_singleton('config/flowManager.ini')
        camera.CameraManager.instantiate_singleton('config/cameraManager.ini')
        network.QuestClientNetworkManager.instantiate_singleton()
        #world.WorldManager.instantiate_singleton('config/worldManager.ini')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Questlike MMO client application
    """ 

    return application.main(ClientApplication, *args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
