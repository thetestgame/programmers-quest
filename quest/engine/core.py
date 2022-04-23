from direct.showbase.DirectObject import DirectObject
from quest.engine import logging

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestObject(DirectObject):
    """
    Base class for all objects inside the quest module
    """

    def __init__(self, notify: str = None):
        DirectObject.__init__(self)
        
        notify = notify if notify != None else self._get_notify_name()
        self._notify = logging.get_notify_category(notify)

        if self._is_server_object():
            self._notify.setInfo(True)

    @property
    def notify(self) -> object:
        """
        Object's Notify instance
        """

        return self._notify

    def _get_notify_name(self) -> str:
        """
        Returns the object's notifier name
        """

        return type(self).__name__

    def _is_server_object(self) -> bool:
        """
        Returns true if this is a server object
        """

        name = self._get_notify_name().lower()
        return name.endswith('ai') or name.endswith('ud')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#