from panda3d import core as p3d

from quest.engine import runtime, core
from quest.framework import configurable
from quest.audio import music
from quest.gui import elements, manager

from direct.gui.OnscreenImage import OnscreenImage

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class GuiScreen(core.QuestObject, configurable.Configurable):
    """
    """

    def __init__(self, config_path: str = None):
        self._background_layer_image_data = {}
        self._background_layer_speed_data = {}

        configurable.Configurable.__init__(self, config_path)
        core.QuestObject.__init__(self)

        self._background_layers = []
        self._background_root = None

        self._music_name = self.pop('music', None)
        if self._music_name != None:
            music_mgr = music.ClientMusicManager.get_singleton()
            music_mgr.play_sound(self._music_name)
            music_mgr.set_sound_loop(self._music_name, True)

        self._background_shader = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex="shaders/screen_background.vert.glsl",
            fragment="shaders/screen_background.frag.glsl")

    @property
    def gui_manager(self) -> manager.QuestClientGuiManager:
        """
        Returns the current client gui manager as a property
        """

        return manager.QuestClientGuiManager.get_singleton()

    def setup(self) -> None:
        """
        Performs setup operations on this screen instance
        """

        self._create_background_layers()

    def destroy(self) -> None:
        """
        Performs destruction operations on this screen instance
        """

        if self._background_root != None:
            self._background_root.remove_node()

        if self._music_name != None:
            music_mgr = music.ClientMusicManager.get_singleton()
            music_mgr.stop_sound(self._music_name)  

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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
