from distutils.command.config import config
from quest.engine import prc, runtime, core
from quest.framework import singleton, configurable
from quest.gui import settings as gui_settings
from quest.gui import dialog

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestClientGuiManager(singleton.Singleton, configurable.Configurable, core.QuestObject):
    """
    """

    def __init__(self, config_path):
        singleton.Singleton.__init__(self)
        core.QuestObject.__init__(self)
        configurable.Configurable.__init__(self, config_path)

        runtime.gui_manager = self
        self._current_popup = None

    def load_gui_settings_data(self, data: dict) -> None:
        """
        """

        # Iterate over our loaded settings data and apply it to DirectGuiGlobals
        for dgg_key in data:
            setter_name = 'set_%s' % dgg_key
            if not hasattr(gui_settings, setter_name):
                self.notify.warning('Failed to set DDG setting (%s). Setting does not exist' % dgg_key)
                continue

            value = data[dgg_key]
            self.notify.info('Setting gui_settings value %s to %s' % (dgg_key, value))
            setter_method = getattr(gui_settings, setter_name)
            setter_method(value)

    def show_popup_message(self, message: str, title: str = None, callback: object = None) -> None:
        """
        """

        self._current_popup = dialog.PopupDialog(message=message, title=title, callback=callback)
        self._current_popup.show()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
