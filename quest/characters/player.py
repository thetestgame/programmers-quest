from panda3d import core as p3d
from panda3d_sprite import sprite as spritesheet

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.characters import npc

import math

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class PlayerCharacter(npc.NPCCharacter):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._local = False

    def is_local(self) -> bool:
        """
        """

        return self._local

    def set_local(self, flag: bool) -> None:
        """
        """

        self._local = flag

    ##############################################
    ######## Character setup/destruction #########
    ##############################################

    def setup(self) -> None:
        """
        """

        super().setup()
        self.activate()

        # TEMP
        self.weapon = spritesheet.Sprite2D(
            file_path='textures/testsword.png',
            rows=1, cols=1)
        self.weapon.node.reparent_to(self.root)
        self.weapon.node.set_r(90)
        self.set_sprite('textures/sprites/TV_bb.ini')

    ##############################################
    ########### Character update loop ############
    ##############################################

    async def tick(self, dt: float) -> None:
        """
        Performs the tick operation for the runnable object
        """

        if self.is_local():
            await self._proccess_user_input(dt)

    async def _proccess_user_input(self, dt: float) -> None:
        """
        """

        await self._process_weapon_aim(dt)
        await self._process_user_movement(dt)

    async def _process_user_movement(self, dt: float) -> None:
        """
        """

        mouse_watcher = runtime.base.mouseWatcherNode
        moving = False

        movement_speed = self.get_stat('movement', 'walk_speed', 20)
        movement_speed *= dt

        if mouse_watcher.is_button_down(p3d.KeyboardButton.ascii_key('d')):
            self.root.set_x(self._root.get_x() + movement_speed)
            moving = True
        elif mouse_watcher.is_button_down(p3d.KeyboardButton.ascii_key('a')):
            self.root.set_x(self._root.get_x() - movement_speed)
            moving = True

        if mouse_watcher.is_button_down(p3d.KeyboardButton.ascii_key('w')):
            self.root.set_y(self._root.get_y() + movement_speed)
            moving = True
        elif mouse_watcher.is_button_down(p3d.KeyboardButton.ascii_key('s')):
            self.root.set_y(self._root.get_y() - movement_speed)
            moving = True

        if moving:
            self.request_state('walking')
        else:
            self.request_state('idling')

    async def _process_weapon_aim(self, dt: float) -> None:
        """
        """

        mouse_watcher = runtime.base.mouseWatcherNode
        if mouse_watcher.has_mouse():
            x = mouse_watcher.get_mouse_x()
            y = -mouse_watcher.get_mouse_y()

            self.look_left = x < 0
            self.weapon.node.set_r(math.atan2(y,x)* 57.29578 + 90)        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
