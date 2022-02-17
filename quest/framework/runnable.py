from quest.engine import core, prc
from quest.engine import runtime, performance
from quest.framework import utilities

import traceback

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Runnable(object):
    """
    """

    def __init__(self, priority: int = 0, task_chain_name: str = None, collector: str = None):
        self._task = None
        self._priority = priority
        self._task_chain_name = task_chain_name

        collector = collector if collector else 'Runnables:%s' % self.__class__.__name__
        self._collector = performance.get_collector('App:%s' % collector)
        self._collect = prc.get_prc_bool('time-runnables', False)

    @property
    def activated(self) -> bool:
        """
        Returns true if the runnable object is active
        """

        return self.is_activated()

    def activate(self) -> None:
        """
        Activates the runnable object's updates
        """

        if self._task == None:
            self._task = utilities.create_task(
                self._do_tick, 
                priority=self._priority,
                task_chain_name=self._task_chain_name)

            return True

        return False

    def deactivate(self) -> None:
        """
        Deactivates the runnable object's updates
        """

        if self._task != None:
            self._task = utilities.remove_task(self.__task)

            return True

        return False

    def is_activated(self) -> bool:
        """
        Returns true if the runnable object is active
        """

        return self._task != None

    async def tick(self, dt: float) -> None:
        """
        Performs the tick operation for the runnable object
        """

        raise NotImplementedError('%s.tick does not implement tick!' % self.__class__.__name__)

    async def _do_tick(self, task: object) -> int:
        """
        Performs the task tick operation
        """

        if self._collect:
            self._collector.start()

        try:
            await self.tick(runtime.globalClock.get_dt())
        except Exception as e:
            traceback.print_exc()
        
        if self._collect:
            self._collector.stop()

        return task.cont

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#