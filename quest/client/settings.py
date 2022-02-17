from quest.engine import core, prc
from quest.engine import runtime, vfs
from quest.framework import settings

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class LocalClientSettings(settings.LocalSettings):
    """
    Represents a client application configuration file
    """

    HEADER_COMMENTS = [
        "; ===================================================================================== ;\n",
        "; This file defines the user's settings and engine configuration values.                ;\n",
        "; This file can be reset to defaults by deleting it prior to launching the game client. ;\n",
        "; ===================================================================================== ;\n",
    ]

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClientSettings(settings.ApplicationSettings):
    """
    """

    THREADING_MODELS = ['App/Cull/Draw', 'Cull/Draw', '/Draw', 'Cull']
    PRC_VARIABLES = ['load-display', 'fullscreen', 'win-size', 'sync-video', 'show-frame-rate-meter']
    SUPPORTED_GRAPHICS_LIBRARIES = prc.get_prc_list('gl-display')

    def __init__(self, config_path: str, local_settings: LocalClientSettings):
        super().__init__(config_path, local_settings)
        assert len(self.SUPPORTED_GRAPHICS_LIBRARIES), 'No Graphics library options configured'

    def set_options_before_engine_start(self) -> None:
        """
        Performs application settings changes prior to Showbase
        initialization
        """

        super().set_options_before_engine_start()

        self.set_video_options()

    def set_darwin_options(self) -> None:
        """
        Sets the darwin operation system specific options
        """

        prc.load_prc_file_data("gl-version 3 2", 'darwin-settings')

    def set_win32_options(self) -> None:
        """
        Sets the windows operation system specific options
        """

        self._set_threading_model_is_enabled()

    def set_linux2_options(self) -> None:
        """
        Sets the linux operation system specific options
        """

        self._set_threading_model_is_enabled()

    def _set_threading_model_is_enabled(self) -> None:
        """
        Sets the threading model for the application
        """

        multithreaded = self.get_setting('enable_multithreading', False, self._valdiate_true_or_false)
        threading_model = self.get_setting('multithreading_model', 0, self._validate_threading_model)
        if multithreaded:
            threading_value = self.THREADING_MODELS[threading_model]
            self.notify.debug('Using threading model: %s' % threading_value)
            self.set_engine_setting('threading-model', threading_value)

    def _validate_threading_model(self, val: int) -> bool:
        """
        Validates the value to ensure its a valid threading model
        option
        """

        return val >= 0 and val < len(self.THREADING_MODELS)

    def _validate_display(self, val: str) -> bool:
        """
        Validates the value to ensure its a valid graphics library
        option
        """

        return self._validate_value(val, self.SUPPORTED_GRAPHICS_LIBRARIES)

    def set_video_options(self) -> None:
        """
        Sets the application's video and graphics options
        """

        display_default = None
        fullscreen_default = None
        size_default = None
        sync_video_default = None
        frame_rate_default = False

        if self.config_prc_settings:
            display_default = self.config_prc_settings.get('load-display', '')
            display_default = display_default[5:] if display_default.startswith('panda') else None
            
            sync_video_default = self.config_prc_settings.get('sync-video', 1)
            sync_video_default = sync_video_default == True or sync_video_default == '#t' or sync_video_default == 't'

            frame_rate_default = self.config_prc_settings.get('show-frame-rate-meter', False)
            frame_rate_default = frame_rate_default == True or frame_rate_default == '#t' or frame_rate_default == 't'
            
            #TODO: load the rest of the defaults

        display = self.get_setting('display', display_default, self._validate_display)
        fullscreen = self.get_setting('fullscreen', fullscreen_default, self._valdiate_true_or_false)
        size = self.get_setting('display_size', size_default)
        sync_video = self.get_setting('video_sync', sync_video_default, self._valdiate_true_or_false)
        frame_rate = self.get_setting('show_fps', frame_rate_default, self._valdiate_true_or_false)

        self.set_engine_setting('fullscreen', fullscreen)
        self.set_engine_setting('load-display', 'panda%s' % display) 
        self.set_engine_setting('win-size', size)
        self.set_engine_setting('sync-video', sync_video)
        self.set_engine_setting('show-frame-rate-meter', frame_rate)
 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
