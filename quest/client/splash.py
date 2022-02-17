import sys
from enum import Enum

from panda3d import core as p3d
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs

from stageflow.panda3d import Cutscene

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class EngineSplash(object):
    """
    """

    def setup(self) -> None:
        """
        Performs setup operations of the splash intro
        object
        """

        x_size, y_size = runtime.base.win.get_x_size(), runtime.base.win.get_y_size()
        bg_buffer = runtime.base.win.make_texture_buffer("Background Scene", x_size, y_size)
        bg_buffer.set_clear_color_active(True)
        bg_buffer.set_clear_color(p3d.VBase4(0, 1, 0, 1))
        bg_buffer.set_sort(-100)  # Render buffer before main scene.

        bg_texture = bg_buffer.get_texture()
        self.bg_texture = bg_texture
        bg_camera = runtime.base.make_camera(bg_buffer)
        self.setup_background_scene(bg_camera)

        # Foreground Scene
        runtime.base.win.set_clear_color((0, 0, 0, 1))
        cam_dist = 2
        runtime.base.cam.set_pos(0, -2.2 * cam_dist, 0)
        runtime.base.cam.node().get_lens().set_fov(45/cam_dist)

        self.logo_animation = Actor("models/splash/panda3d_logo.bam")
        self.logo_animation.reparent_to(runtime.render)
        self.logo_animation.set_two_sided(True)

        shader = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex="shaders/splash_window.vert",
            fragment="shaders/splash_window.frag")
        self.logo_animation.set_shader(shader)
        self.logo_animation.set_shader_input("background", bg_texture)
        self.logo_animation.set_shader_input("fade", 0.0)
        self.logo_sound = runtime.loader.load_sfx('audio/panda3d_logo.ogg')

        # Build interval
        def fade_background_to_white(t: object) -> None:
            """
            """

            runtime.base.win.set_clear_color((t,t,t,1))
            self.logo_animation.set_shader_input("fade", t)
        
        def set_background_texture(t: object) -> None:
            """
            """

            self.logo_animation.set_shader_input(
                "background",
                self.bg_texture)
                    
        effects = Parallel(
            self.logo_animation.actorInterval(
                "splash",
                loop=False,
            ),
            SoundInterval(
                self.logo_sound,
                loop=False,
            ),
            Sequence(
                LerpFunc(
                    set_background_texture,
                    fromData=0,
                    toData=1,
                    duration=3.878,
                ),
                LerpFunc(
                    fade_background_to_white,
                    fromData=0,
                    toData=1,
                    duration=1.0,
                ),
            ),
        )
        return effects

    def teardown(self) -> None:
        """
        Performs destruction teardown operations on the
        splash object
        """

        self.teardown_background_scene()
        self.logo_animation.cleanup()
        runtime.base.win.set_clear_color((0, 0, 0, 1))
        
        # FIXME: Destroy self.logo_sound
        # FIXME: Destroy the extra buffer stuff

    def setup_background_scene(self, bg_camera: object) -> None:
        """
        set up the scene that will be seen through the
        splash's shards.

        bg_camera
          The camera watching the background scene
        """
        
        # The scene to be rendered to texture
        bg_scene = p3d.NodePath("SplashScene")
        bg_camera.reparent_to(bg_scene)
        bg_camera.set_pos(0, -100, 50)
        bg_camera.look_at(0, 0, 0)

        model = runtime.loader.loadModel('models/splash/environment')
        model.reparent_to(bg_scene)
        model.set_scale(0.25)

    def teardown_background_scene(self) -> None:
        """
        Performs destruction teardown operations on the
        splash background scene
        """
       
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Panda3dEngineSplash(Cutscene):
    """
    A generic splash screen advertising Panda3D.
    """

    def __init__(self, *args, splash_args: dict = None, **kwargs):
        super().__init__(*args, **kwargs)
        if splash_args is None:
            splash_args = {}
        self.splash_args = splash_args

    def setup_credits(self, data: object) -> object:
        """
        """
 
        self.splash = EngineSplash(**self.splash_args)
        interval = self.splash.setup()
        runtime.transitions.fadeIn(0)

        return interval

    def destroy_credits(self) -> None:
        """
        """

        self.splash.teardown()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#