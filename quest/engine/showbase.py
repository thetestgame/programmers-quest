from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions

from quest.engine import logging, runtime
from quest.engine import prc

#----------------------------------------------------------------------------------------------------------------------------------#

class QuestShowBase(ShowBase):
    """
    Base class for all ShowBase based applications inside the quest Python module
    """

    notify = logging.get_notify_category('showbase')

    def __init__(self, *args, **kwargs):
        prc.load_prc_file_data('window-title Programmers Quest', 'locale-information') #TODO: pull from localizer

        super().__init__(*args, **kwargs)
        self._headless = self.windowType == 'none'

        runtime.task_mgr = self.task_mgr
        if not self._headless:
            self.transitions = Transitions(self.loader)
            self.transitions.IrisModelName = 'models/ui/iris'
            self.transitions.fadeOut(0)
            runtime.transitions = self.transitions

    @property
    def headless(self) -> bool:
        """
        """

        return self._headless

#----------------------------------------------------------------------------------------------------------------------------------#