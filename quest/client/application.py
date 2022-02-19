from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import application, utilities
from quest.distributed import repository
from quest.client import flow, settings, camera
from quest.gui import manager as gui_manager

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClientApplication(application.QuestApplication):
    """
    Primary QuestApplication instance for the Programmer's Quest! MMO client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_framework(self) -> None:
        """
        Performs framework setup operations on the client application
        """
        
        super().setup_framework()

        # Load our user defined settings into memory and apply them to the application and engine runtime
        local_settings = settings.LocalClientSettings('user_settings.ini' if runtime.dev else utilities.get_local_data_path('user_settings.ini'))
        self.client_settings = settings.ClientSettings.instantiate_singleton('config/defaultSettings.ini', local_settings)
        self.client_settings.set_options_before_engine_start()
        local_settings.write()

    def setup_engine(self) -> None:
        """
        Performs engine setup operations on the client application
        """
        
        super().setup_engine()
        self.client_settings.set_options_after_engine_start()

        # Configure our task threads if configured in the application's runtime configuration
        utilities.create_thread('tile-layer-chain', prc_check='want-threaded-tilemap')
        utilities.create_thread('world-culling-chain', prc_check='want-threaded-world-cull')

    def setup_game(self) -> None:
        """
        Performs game setup operations on the client application
        """
        
        super().setup_game()
    
        # Instantiate our singletons
        flow.ClientFlowManager.instantiate_singleton('config/flowManager.ini')
        camera.CameraManager.instantiate_singleton('config/cameraManager.ini')
        #world.WorldManager.instantiate_singleton('config/worldManager.ini')
        repository.QuestClientRepository.instantiate_singleton()
        gui_manager.QuestClientGuiManager.instantiate_singleton('config/guiManager.ini')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Questlike MMO client application
    """

    return application.main(ClientApplication, *args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
