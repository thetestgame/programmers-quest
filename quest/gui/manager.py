from distutils.command.config import config
from quest.engine import prc, runtime, core
from quest.framework import singleton, configurable
from quest.gui import settings as gui_settings
from quest.gui import dialog, splash, stages
from quest.gui.screens import network

from stageflow import Flow, prefab, Stage

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClientFlow(Flow):
    """
    Primary flow and control for the Quest MMO client. Handles the
    clients required intro attributions and initial main menu sequence
    controls
    """

    def transition(self, stage_name: str, data: dict = None) -> None:
        """
        Exit the current stage and enter another. This can only be done
        if no substage is active.
        stage_name
            Name of the stage to transition to
        data
            Arbitrary data that will be passed to the current stage's
            :class:`Stage.exit`
        """

        fade_time = prc.get_prc_double('flow-fade-time', 0.5)
        transitions = runtime.transitions
        if not transitions.fadeOutActive():
            transitions.fadeOut(fade_time)

        super().transition(stage_name, data)
        transitions.fadeIn(fade_time)


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestClientGuiManager(singleton.Singleton, configurable.Configurable, core.QuestObject):
    """
    """

    def __init__(self, config_path):
        singleton.Singleton.__init__(self)
        core.QuestObject.__init__(self)
        configurable.Configurable.__init__(self, config_path)

        self._flow = self._create_client_flow()
        runtime.base.flow = self._flow
        runtime.gui_manager = self
        self._current_popup = None

        initial_stage = self.pop('starting_stage')
        if runtime.dev:
            dev_initial_stage = prc.get_prc_string('flow-initial-stage', initial_stage)
            if dev_initial_stage != initial_stage:
                initial_stage = dev_initial_stage
        self._flow.transition(initial_stage)

    def transition(self, stage_name: str, **kwargs: dict) -> None:
        """
        """

        self._flow.transition(stage_name, data = kwargs)

    def _create_client_flow(self) -> stages.ClientFlow:
        """
        Creates the global client flow object and returns the instance
        """

        configured_stages = dict(
            splash=splash.Panda3dEngineSplash(exit_stage='login_screen'),
            login_screen=network.NetworkLoginScreen(config_path='ui/screens/screen_network_status.ini'),
            network_error=network.NetworkStatusScreen(config_path='ui/screens/screen_network_status.ini'),
            gameplay=stages.GameplayStage(),
            quit=prefab.Quit())

        flow = ClientFlow(stages=configured_stages)
        return flow

    def load_gui_settings_data(self, data: dict) -> None:
        """
        Loads the global settings data from the configuration file
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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
