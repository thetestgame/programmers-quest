from xml.dom.minidom import CharacterData
from numpy import character
from quest.engine import runtime, core, prc
from quest.framework import singleton, configurable
from quest.distributed import objects, constants
from quest.engine import runtime

from playfab import PlayFabClientAPI, PlayFabServerAPI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed import MsgTypes

import dataclasses

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@dataclasses.dataclass
class PotentialCharacter(object):
    """
    Represents a potential selectable character retrieved from PlayFab's server
    for the authenticated player
    """

    character_id: str
    character_name: str
    character_type: str

    character_data: dict
    character_readonly_data: dict

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAvatarManager(objects.QuestDistributedObjectGlobal):
    """
    """

    def __init__(self, cr):
        super().__init__(cr)
        self.notify.setInfo(True)

        self.potential_characters = []

    def has_characters(self) -> bool:
        """
        Returns true if the authenticated account owns any characters
        """

        return len(self.potential_characters) > 0

    def retrieve_potential_characters(self, callback: object = None) -> None:
        """
        """

        PlayFabClientAPI.GetAllUsersCharacters({}, lambda result, error: self.handle_potential_characters_callback(callback, result, error))

    def create_new_character(self, character_type_item: int, catalog_version: str, character_data: dict, callback: object = None) -> None:
        """
        """

        request = {
            "CharacterName": "dbChar",
            "ItemId": character_type_item,
            "CatalogVersion": catalog_version
        }

        def character_grant_callback(result: dict, error: dict) -> None:
            """
            """

            #
            if error != None:
                if callback != None:
                    callback(result, error)

                return

            #
            if character_data != None:
                data_request = {
                    "CharacterId": result["CharacterId"],
                    "Data": character_data
                }

                def update_data_callback(result: dict, error: dict) -> None:
                    """
                    """

                    print(result)
                    print(error)

                PlayFabClientAPI.UpdateCharacterData(data_request, update_data_callback)

            #
            if callback != None:
                callback(result, error)

        PlayFabClientAPI.GrantCharacterToUser(request, character_grant_callback)

    def handle_potential_characters_callback(self, callback: object = None, result: dict = None, error: dict = None) -> None:
        """
        """

        # Check if there was an error from PlayFab. If an error was detected convert that into the standard
        # failure callback format used by the QuestAvatarManager system and inform our callback
        if error != None:
            code = error['errorCode']
            reason = error['errorMessage']

            self.handle_internal_error(callback, code, reason)
            return

        characters = result["Characters"]
        #TODO: handle characters

        #TEMP
        if len(characters) == 0:
            self.create_new_character("CharacterSlot", "develop", character_data={
                "Skin": "TV",
                "Level": 1,
                "Weapon": ""
            })
        else:
            self.choose_character(characters[0]["CharacterId"])

        if callback != None:
            callback(True, 200, 'Success')

    def handle_internal_error(self, callback: object = None, code: int = 0, reason: str = "") -> None:
        """
        """

    def choose_character(self, character_id: str) -> None:
        """
        """

        self.send_update('choose_character', [character_id])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAvatarManagerAI(objects.QuestDistributedObjectGlobalAI):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAvatarManagerUD(objects.QuestDistributedObjectGlobalUD):
    """
    """

    def kick_account(self, account_id: int, reason: str, code: int = 100) -> None:
        """
        """

        self.air.eject(account_id, code, reason)

    def choose_character(self, character_id: str) -> None:
        """
        """

        current_character_id = self.air.get_character_id_from_sender()
        account_id = self.air.get_account_id_from_sender()

        if current_character_id and character_id:
            self.kick_account(account_id, 'A character was already selected') #TODO: localize properly
        elif not current_character_id and not character_id:
            return

        print('READY TO LOAD!')
        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#