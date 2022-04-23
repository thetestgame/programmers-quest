from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.gui import splash, screen
from quest.framework import singleton, configurable

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

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class TitleScreenStage(Stage, core.QuestObject):
    """
    """

    def __init__(self, *args, **kwargs):
        Stage.__init__(self, *args, **kwargs)
        core.QuestObject.__init__(self)

    def enter(self, data: dict = None) -> None:
        """
        Override this with setup code for entry of this stage.

        data
            Data passed from the exit of the previous :class:`Stage`.
        """

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

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ChooseAvatarStage(Stage, core.QuestObject):
    """
    """

    def __init__(self, *args, **kwargs):
        Stage.__init__(self, *args, **kwargs)
        core.QuestObject.__init__(self)

    def enter(self, data: dict = None) -> None:
        """
        Override this with setup code for entry of this stage.

        data
            Data passed from the exit of the previous :class:`Stage`.
        """

        print('WOW!')

    def exit(self, data: dict = None) -> object:
        """
        Override this with teardwn code for exit from this stage, and
        pass on data for the next stage.

        data
            Data that was passed to :class:`Flow.transition`.

        :returns:
            Arbitrary data for the next active :class:`Stage`.
        """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClientFlowManager(configurable.Configurable, singleton.Singleton, core.QuestObject):
    """
    """

    def __init__(self, config_path: str):
        configurable.Configurable.__init__(self, config_path)
        core.QuestObject.__init__(self)

        self._flow = self._create_client_flow()
        runtime.base.flow = self._flow
        runtime.flow_mgr = self

        initial_stage = self.pop('starting_stage')
        if runtime.dev:
            dev_initial_stage = prc.get_prc_string('flow-initial-stage', initial_stage)
            if dev_initial_stage != initial_stage:
                initial_stage = dev_initial_stage
        self._flow.transition(initial_stage)

    def _create_client_flow(self) -> ClientFlow:
        """
        """

        stages = dict(
            splash=splash.Panda3dEngineSplash(exit_stage='titleScreen'),
            titleScreen=TitleScreenStage(),
            chooseAvatar=ChooseAvatarStage(),
            quit=prefab.Quit())

        flow = ClientFlow(stages=stages)
        return flow

    def transition(self, *args, **kwargs) -> None:
        """
        """

        self._flow.transition(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#