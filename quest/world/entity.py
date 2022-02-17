from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import runnable

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Entity(runnable.Runnable, core.QuestObject):
    """
    """

    def __init__(self, *args, **kwargs):
        if 'collector' not in kwargs:
            kwargs['collector'] = 'App:Entity:Update'
        
        runnable.Runnable.__init__(self, *args, **kwargs)
        core.QuestObject.__init__(self)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class EntityCollection(core.QuestObject):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#