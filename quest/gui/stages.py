from panda3d import core as p3d

from quest.engine import core, prc
from quest.engine import runtime, vfs
from quest.framework import configurable

from stageflow import Flow, Stage
from direct.gui.OnscreenImage import OnscreenImage

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

class GameScreenStage(Stage, core.QuestObject, configurable.Configurable):
    """
    Base class for all game UI screen stages
    """

    def __init__(self, config_path: str):
        self._background_layer_image_data = {}
        self._background_layer_speed_data = {}

        configurable.Configurable.__init__(self, config_path)
        Stage.__init__(self)
        core.QuestObject.__init__(self)

        self._background_layers = []
        self._background_root = None

        self._background_shader = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex="shaders/screen_background.vert.glsl",
            fragment="shaders/screen_background.frag.glsl")

    def enter(self, data: dict = None) -> None:
        """
        Override this with setup code for entry of this stage.

        data
            Data passed from the exit of the previous :class:`Stage`.
        """

        if self._background_root == None:
            self._create_background_layers()
        self._background_root.show()

    def exit(self, data: dict = None) -> object:
        """
        Override this with teardwn code for exit from this stage, and
        pass on data for the next stage.

        data
            Data that was passed to :class:`Flow.transition`.

        :returns:
            Arbitrary data for the next active :class:`Stage`.
        """

        if self._background_root != None:
            self._background_root.hide()

    def load_background_image_data(self, data: dict) -> None:
        """
        """

        self._background_layer_image_data = data

    def load_background_speed_data(self, data: dict) -> None:
        """
        """

        self._background_layer_speed_data = data

    def _create_background_layer(self, index: int, image: str, speed_x: float = 0, speed_y: float = 0) -> None:
        """
        """

        assert self._background_root != None

        layer_node = OnscreenImage(image=image, parent=self._background_root)
        layer_node.set_y(index * -0.1)
        layer_node.set_shader(self._background_shader)
        layer_node.set_shader_input('pq_panning_rate_x', speed_x)
        layer_node.set_shader_input('pq_panning_rate_y', speed_y)
        layer_node.set_transparency(p3d.TransparencyAttrib.MAlpha)

        self._background_layers.append(layer_node)

    def _create_background_layers(self) -> None:
        """
        """

        if self._background_root != None:
            return

        self._background_root = p3d.NodePath('%s-background' % self.__class__.__name__)
        self._background_root.reparent_to(runtime.render2d)

        for layer_index_str in self._background_layer_image_data.keys():
            layer_index = int(layer_index_str)
            layer_image = self._background_layer_image_data[layer_index_str]
            layer_speed_data = self._background_layer_speed_data[layer_index_str]
            layer_speeds = layer_speed_data.split(',')

            self._create_background_layer(layer_index, layer_image, float(layer_speeds[0]), float(layer_speeds[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class GameplayStage(Stage, core.QuestObject):
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