from distutils.command.config import config
from quest.engine import prc, runtime, core
from quest.framework import singleton, configurable
from quest.gui import elements

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestClientGuiManager(singleton.Singleton, configurable.Configurable, core.QuestObject):
    """
    """

    def __init__(self, config_path):
        singleton.Singleton.__init__(self)
        core.QuestObject.__init__(self)
        configurable.Configurable.__init__(self, config_path)
        self.notify.setInfo(True)

        runtime.gui_manager = self
        self._status_dialog = elements.QuestStatusDialog()

    def set_status_message(self, message: str = None) -> None:
        """
        Sets the currently displayed status message to the user. Setting this 
        to a value of NoneType hides the message from the screen
        """

        if message != None:
            self.notify.info('Displaying Status: %s' % message)
            self._status_dialog.set_message(message)
            self._status_dialog.show()
        else:
            self._status_dialog.hide()

    def load_gui_settings_data(self, data: dict) -> None:
        """
        Loads the global settings data from the configuration file
        """

        # Iterate over our loaded settings data and apply it to DirectGuiGlobals
        for dgg_key in data:
            setter_name = 'set_%s' % dgg_key
            if not hasattr(elements, setter_name):
                self.notify.warning('Failed to set DDG setting (%s). Setting does not exist' % dgg_key)
                continue

            value = data[dgg_key]
            self.notify.info('Setting gui_settings value %s to %s' % (dgg_key, value))
            setter_method = getattr(elements, setter_name)
            setter_method(value)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
