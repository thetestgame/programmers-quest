"""
Quest module wrapper for the native Panda3D distributed object classes
"""

from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.distributed.DistributedObjectOV import DistributedObjectOV
from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.DistributedNodeAI import DistributedNodeAI

from quest.engine import core
from quest.framework import singleton, configurable

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestDistributedObjectMixin(core.QuestObject):
    """
    Mixin object for implementing share quest module based DO features
    """

    def send_update(self, field: str, params: list) -> None:
        """
        """

        self.sendUpdate(field, params)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Global Objects

class QuestDistributedObjectGlobal(DistributedObjectGlobal, singleton.Singleton, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedObjectGlobalAI(DistributedObjectGlobalAI, singleton.Singleton, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedObjectGlobalUD(DistributedObjectGlobalUD, singleton.Singleton, QuestDistributedObjectMixin):
    """
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Objects

class QuestDistributedObject(DistributedObject, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedObjectOV(DistributedObjectOV, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedObjectAI(DistributedObjectAI, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedObjectUD(DistributedObjectUD, QuestDistributedObjectMixin):
    """
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Node Objects

class QuestDistributedNode(DistributedNode, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedNodeAI(DistributedNodeAI, QuestDistributedObjectMixin):
    """
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Configurable Objects

class QuestDistributedConfigurableObject(DistributedObject, configurable.Configurable, QuestDistributedObjectMixin):
    """
    """

    def __init__(self, cr: object):
        DistributedObject.__init__(self, cr)
        QuestDistributedObjectMixin.__init__(self)

    def set_configuration(self, filepath: str) -> None:
        """
        """

class QuestDistributedConfigurableObjectOV(DistributedObjectOV, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedConfigurableObjectAI(DistributedObjectAI, QuestDistributedObjectMixin):
    """
    """

class QuestDistributedConfigurableObjectUD(DistributedObjectUD, QuestDistributedObjectMixin):
    """
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #