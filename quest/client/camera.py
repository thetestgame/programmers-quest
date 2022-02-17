from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import configurable, singleton
from quest.framework import runnable

from enum import Enum

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class CameraMode(Enum):
    """
    """

    CM_FOLLOW = 0

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class CameraManager(configurable.Configurable, singleton.Singleton, runnable.Runnable, core.QuestObject):
    """
    """

    def __init__(self, config_path: str):
        configurable.Configurable.__init__(self, config_path)
        runnable.Runnable.__init__(self, collector='App:CameraUpdate')
        core.QuestObject.__init__(self)
        runtime.base.disableMouse()
        runtime.camera_mgr = self

        self._camera = runtime.base.camera
        self._camera_mode = CameraMode.CM_FOLLOW
        self.camera_follow_target = None
        self.camera_follow_distance = 100
        self.activate()

    def destroy(self) -> None:
        """
        """

        self.deactivate()

    async def tick(self, dt: float) -> None:
        """
        Performs the tick operation for the runnable object
        """

        if self._camera_mode == CameraMode.CM_FOLLOW:
            await self._follow_target(dt)
        else:
            self.notify.warning('Failed to update %s. Unsupported camera mode %d' % (
                self.__class__.__name__, self._camera_mode))
            
            return

    async def _follow_target(self, dt: float) -> None:
        """
        """

        if self.camera_follow_target is None:
            return

        follow_position = self.camera_follow_target.get_pos()
        follow_position.set_z(self.camera_follow_distance)

        self._camera.set_pos(follow_position)
        self._camera.look_at(self.camera_follow_target)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
