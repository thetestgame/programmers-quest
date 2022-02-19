from panda3d import core as p3d
from direct.gui.DirectGui import *

from quest.engine import runtime, core
from quest.gui import settings as gui_settings

import enum

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class PopupDialog(DirectDialog, core.QuestObject):
    """
    """

    def __init__(self, message: str = None, title: str = None, parent: object = None, callback: object = None, **kw: dict):

        if parent == None:
            parent = runtime.base.aspect2d
        self.callback = callback

        # TODO: properly handle styling and button options
        card_models = gui_settings.get_default_dialog_button_geoms()
        button_image_data = (card_models.find('**/btn_green_relief'), card_models.find('**/btn_green_pressed'), card_models.find('**/btn_green_pressed'))

        button_values = [DGG.DIALOG_OK]
        button_text = ['OK']
        button_images = [button_image_data]

        options = (
            ('buttonImageList',     button_images,          DGG.INITOPT),
            ('buttonTextList',      button_text,            DGG.INITOPT),
            ('buttonValueList',     button_values,          DGG.INITOPT),
            ('topPad',              0.2,                    DGG.INITOPT),
            ('midPad',              0.10,                   DGG.INITOPT),
            ('sidePad',             0.2,                    DGG.INITOPT),
            ('button_pad',          (0,0),                  None),
            ('button_relief',       None,                   None),
            ('button_text_pos',     (0,-0.01),              None),
            ('text_align',          p3d.TextNode.ACenter,   None),
            ('text_font',           DGG.getDefaultFont(),   None),
            ('text_wordwrap',       12,                     None),
            ('text_scale',          0.07,                   None),
            ('fadeScreen',          0.5,                    None),
            ('image_color',         (1, 1, 1, 1),           None),
            ('bgBuffer',            0.025,                  None),
            ('relief',              None,                   None),
            ('frameSize',           (-0.5, 0.5, -0.5, 0.5), None),
            ('cornerWidth',         0.15,                   None), 
            ('draggable',           0,                      None),
            ('flatten',             1,                      None),
            ('text',                message,                None),
            ('command',             self.handle_button,     None))

        # Merge keyword options with default options
        self.defineoptions(kw, options)
        DirectDialog.__init__(self, parent)
        core.QuestObject.__init__(self)
        self.initialiseoptions(PopupDialog)

    def handle_button(self, value: object) -> None:
        """
        """

        if self.callback != None:
            self.callback(value)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #