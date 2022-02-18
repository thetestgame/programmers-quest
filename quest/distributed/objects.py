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
from quest.framework import singleton
import datetime

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestDistributedObjectMixin(core.QuestObject):
    """
    Mixin object for implementing share quest module based DO features
    """

    def send_update(self, field: str, params: list) -> None:
        """
        Sends a distributed object update over the network. Serves as a snake case
        wrapper for code uniformity
        """

        self.sendUpdate(field, params)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Global Objects

class QuestDistributedObjectGlobalMixin(singleton.Singleton, QuestDistributedObjectMixin):
    """
    """

    def generate(self) -> None:
        """
        Custom generate instance for handling automatic logging
        """

        super().generate()

        generate_time = datetime.now().strftime("%H:%M:%S")
        do_name = type(self).__name__
        self.notify.info("%s %.generate for %s" % (generate_time, do_name, self.doId))

class QuestDistributedObjectGlobal(DistributedObjectGlobal, singleton.Singleton, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObjectGlobal class.
    """

class QuestDistributedObjectGlobalAI(DistributedObjectGlobalAI, singleton.Singleton, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObjectGlobalAI class.
    """

class QuestDistributedObjectGlobalUD(DistributedObjectGlobalUD, singleton.Singleton, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObjectGlobalUD class.
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Objects

class QuestDistributedObject(DistributedObject, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObject class.
    """

class QuestDistributedObjectOV(DistributedObjectOV, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObjectOV class.
    """

class QuestDistributedObjectAI(DistributedObjectAI, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObjectAI class.
    """

class QuestDistributedObjectUD(DistributedObjectUD, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedObjectUD class.
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Distributed Node Objects

class QuestDistributedNode(DistributedNode, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedNode class.
    """

class QuestDistributedNodeAI(DistributedNodeAI, QuestDistributedObjectMixin):
    """
    Custom quest module wrapper for the Panda3D direct tree DistributedNodeAI class.
    """

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #