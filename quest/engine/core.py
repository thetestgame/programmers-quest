from direct.showbase.DirectObject import DirectObject
from quest.engine import logging

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestObject(DirectObject):
    """
    Base class for all objects inside the quest module
    """

    def __init__(self, notify: str = None):
        super().__init__()
        
        notify = notify if notify != None else self.get_notify_name()
        self._notify = logging.get_notify_category(notify)

    @property
    def notify(self) -> object:
        """
        Object's Notify instance
        """

        return self._notify

    def get_notify_name(self) -> str:
        """
        Returns this objects class name as a notify friendly name
        """

        name = self.__class__.__name__ 
        res = [name[0].lower()] 
        for c in name[1:]: 
            if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'): 
                res.append('-') 
                res.append(c.lower()) 
            else: 
                res.append(c) 

        full =  ''.join(res) 
        full = full.replace('t-m-x', 'tmx')
        full = full.replace('h-t-t-p', 'http')

        return full

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#