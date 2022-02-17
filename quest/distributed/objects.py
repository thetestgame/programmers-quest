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
from quest.framework import singleton

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Global Objects

class QuestDistributedObjectGlobal(DistributedObjectGlobal, singleton.Singleton, core.QuestObject):
    """
    """

class QuestDistributedObjectGlobalAI(DistributedObjectGlobalAI, singleton.Singleton, core.QuestObject):
    """
    """

class QuestDistributedObjectGlobalUD(DistributedObjectGlobalUD, singleton.Singleton, core.QuestObject):
    """
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Objects


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #