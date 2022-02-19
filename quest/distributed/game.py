from quest.distributed import objects
from quest.engine import runtime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedGame(objects.QuestDistributedObject):
    """
    This object has no attributes or methods and is never actually created by the game client. However
    it is required for the distributed objects system to work properly. It serves as the object tree root
    for the entire game inside the Astron server. Everything owned by the game is parented under this object
    """
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class DistributedGameAI(objects.QuestDistributedObjectAI):
    """
    This object has no attributes or methods and is never actually created by the game client. However
    it is required for the distributed objects system to work properly. It serves as the object tree root
    for the entire game inside the Astron server. Everything owned by the game is parented under this object
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#