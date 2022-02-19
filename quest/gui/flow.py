from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.gui import splash
from quest.framework import singleton, configurable
from quest.distributed import repository

from stageflow import Flow, prefab, Stage

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ConnectingState(Stage, core.QuestObject):
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

        # Testing
        from quest.audio import music
        test = music.ClientMusicManager.get_singleton()
        test.play_sound('screen_login_theme')
        test.set_sound_loop('screen_login_theme', True)

        from direct.gui.OnscreenImage import OnscreenImage
        from panda3d import core as p3d
        sky_image = OnscreenImage(
            image='textures/ui/screen_bg_sky.png', 
            parent=runtime.render2d)
        background_image = OnscreenImage(
            image='textures/ui/screen_bg_background.png', 
            parent=runtime.render2d)
        foreground_image = OnscreenImage(
            image='textures/ui/screen_bg_foreground.png', 
            parent=runtime.render2d)

        foreground_image.set_transparency(p3d.TransparencyAttrib.MAlpha)
        background_image.set_transparency(p3d.TransparencyAttrib.MAlpha)

        sky_image.set_y(0)
        background_image.set_y(-0.1)
        foreground_image.set_y(-0.2)

        shader = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex="shaders/panning.vert.glsl",
            fragment="shaders/panning.frag.glsl")

        background_image.set_shader(shader)
        foreground_image.set_shader(shader)
        background_image.set_shader_input('pq_panning_rate', 0.2)
        foreground_image.set_shader_input('pq_panning_rate', 0.4)

    def exit(self, data: dict = None) -> object:
        """
        Override this with teardwn code for exit from this stage, and
        pass on data for the next stage.

        data
            Data that was passed to :class:`Flow.transition`.

        :returns:
            Arbitrary data for the next active :class:`Stage`.
        """