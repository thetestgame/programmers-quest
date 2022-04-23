from panda3d import core as p3d

from quest.engine import runtime, core
from quest.framework import configurable
from quest.gui import elements, screen

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectEntry import DirectEntry

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class ClientLoginScreen(screen.GuiScreen):
    """
    """

    def __init__(self, config_path: str, complete_event: str):
        super().__init__(config_path)

        self._complete_event = complete_event

    def setup(self) -> None:
        """
        Performs setup operations on this screen instance
        """

        super().setup()

        self._frame = elements.QuestParchmentFrame()
        self._frame.createcomponent(
            'username', (), 'entry', 
            DirectEntry, (self._frame,),
            scale=0.05)

    def destroy(self) -> None:
        """
        Performs destruction operations on this screen instance
        """

        super().destroy()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
