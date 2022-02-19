from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.gui import stages, dialog
from quest.framework import singleton, configurable
from quest.distributed import repository, authentication

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkStatusScreen(stages.GameScreenStage):
    """
    """

    def __init__(self, config_path: str, *args, **kwargs):
        super().__init__(config_path, *args, **kwargs)

        self._status_popup = dialog.PopupDialog()
        self._status_popup.hide()

    def enter(self, data: dict = None) -> None:
        """
        Override this with setup code for entry of this stage.

        data
            Data passed from the exit of the previous :class:`Stage`.
        """

        super().enter(data)

        #if data != None:
        #    message = data['message']
        #    title = data['title']
        #    callback = data['callback']
#
        #    self._current_popup = dialog.PopupDialog(message=message, title=title, callback=callback)
        #    self._current_popup.show()

        # Testing
        #from quest.audio import music
        #test = music.ClientMusicManager.get_singleton()
        #test.play_sound('screen_login_theme')
        #test.set_sound_loop('screen_login_theme', True)

    def exit(self, data: dict = None) -> object:
        """
        Override this with teardwn code for exit from this stage, and
        pass on data for the next stage.

        data
            Data that was passed to :class:`Flow.transition`.

        :returns:
            Arbitrary data for the next active :class:`Stage`.
        """

        super().exit(data)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkLoginScreen(stages.GameScreenStage):
    """
    """

    def __init__(self, config_path: str, *args, **kwargs):
        super().__init__(config_path, *args, **kwargs)

        self._status_popup = dialog.PopupDialog()
        self._status_popup.hide()

    def enter(self, data: dict = None) -> None:
        """
        Override this with setup code for entry of this stage.

        data
            Data passed from the exit of the previous :class:`Stage`.
        """

        super().enter(data)

        client_agent_address = runtime.application.get_startup_variable('CA_HOST', '127.0.0.1')
        client_agent_port = int(runtime.application.get_startup_variable('CA_PORT', '6667'))
        runtime.cr.connect(client_agent_address, client_agent_port)

    def exit(self, data: dict = None) -> object:
        """
        Override this with teardwn code for exit from this stage, and
        pass on data for the next stage.

        data
            Data that was passed to :class:`Flow.transition`.

        :returns:
            Arbitrary data for the next active :class:`Stage`.
        """

        super().exit(data)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#