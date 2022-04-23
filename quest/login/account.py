from quest.distributed import objects
import dataclasses

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@dataclasses.dataclass
class QuestAccount(objects.QuestDistributedObject):
    """
    Stub object to fulfill the requirements of the DC system. This is used internally to bridge the PlayFab account details to the details stored
    within the Astron cluster database.
    """

@dataclasses.dataclass
class QuestAccountAI(objects.QuestDistributedObjectAI):
    """
    Stub object to fulfill the requirements of the DC system. This is used internally to bridge the PlayFab account details to the details stored
    within the Astron cluster database.
    """

@dataclasses.dataclass
class QuestAccountUD(objects.QuestDistributedObjectUD):
    """
    Stub object to fulfill the requirements of the DC system. This is used internally to bridge the PlayFab account details to the details stored
    within the Astron cluster database.
    """

    playfab_account_id: str

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
