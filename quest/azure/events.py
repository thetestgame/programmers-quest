from quest.engine import runtime, core, prc
from quest.framework import singleton, configurable
from quest.distributed import objects, constants
from quest.engine import runtime

from playfab import PlayFabClientAPI, PlayFabServerAPI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed import MsgTypes

import enum

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestReportReasons(enum.IntEnum):
    """
    """

    QRR_FOUL_LANGUAGE = 1
    QRR_PERSONAL_INFO = 2
    QRR_INAPPROPRIATE_BEHAVIOUR = 3
    QRR_INAPPROPRIATE_NAME = 4
    QRR_SUSPECTED_BOT = 5

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class SessionTracker(core.QuestObject):
    """
    """

    # Session based tracker for monitoring the amount of times
    # a player reported during this play session.
    players_reported = {}

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestEventManager(objects.QuestDistributedObjectGlobal):
    """
    """


    def __init__(self, cr):
        super().__init__(cr)
        self.notify.setInfo(True)

        self._session_tracker = SessionTracker()

    @property
    def session_tracker(self) -> SessionTracker:
        """
        """

        return self._session_tracker

    def report_player(self, category: QuestReportReasons, player_id: str, avatarId: str, description: str = None) -> bool:
        """
        """

        #TODO

    def has_reported_player(self, player_id: str, avatar_id: str) -> bool:
        """
        """

        return (player_id, avatar_id) in self.session_tracker.players_reported

    def write_player_event(self, event_name: str, body: str) -> None:
        """
        """

    def write_character_event(self, event_name: str, body: str, avatar_id: str) -> None:
        """
        """

    def write_title_event(self, event_name: str, body: str) -> None:
        """
        """

 #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestEventManagerAI(objects.QuestDistributedObjectGlobalAI):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestEventManagerUD(objects.QuestDistributedObjectGlobalUD):
    """
    """

    def __init__(self, air: object):
        super().__init__(air)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#