from panda3d import core as p3d
from direct.gui.DirectGui import *

from quest.engine import runtime, core

import enum

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def set_default_dialog_geom(model_path: str) -> None:
    """
    Sets the property of DirectGuiGlobals.set_default_dialog_geom with a model
    loaded from the configured model path
    """

    model_inst = runtime.loader.load_model(model_path)
    DGG.set_default_dialog_geom(model_inst)

def set_default_font(font_path: str) -> None:
    """
    Sets the property of DirectGuiGlobals.set_default_font with a font
    loaded from the configured font path
    """

    font_inst = runtime.loader.load_font(font_path)
    DGG.set_default_font(font_inst)

def set_default_click_sound(sound_path: str) -> None:
    """
    Sets the property of DirectGuiGlobals.set_default_click_sound with a audio
    loaded from the configured sound path
    """

    sound_inst = runtime.loader.load_sfx(sound_path)
    DGG.set_default_click_sound(sound_inst)

def set_default_rollover_sound(sound_path: str) -> None:
    """
    Sets the property of DirectGuiGlobals.set_default_rollover_sound with a audio
    loaded from the configured sound path
    """

    sound_inst = runtime.loader.load_sfx(sound_path)
    DGG.set_default_rollover_sound(sound_inst)

default_dialog_button_geom = None

def set_default_dialog_button_geoms(model_path: str) -> None:
    """
    Sets the default dialog button geometry model used for querying button stylings from
    """

    global default_dialog_button_geom
    default_dialog_button_geom = runtime.loader.load_model(model_path)

def get_default_dialog_button_geoms() -> object:
    """
    Returns the configured global dialog button geometry models
    """

    return default_dialog_button_geom

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestParchmentFrame(DirectFrame, core.QuestObject):
    """
    """

    def __init__(self, parent: object = None, **kw):

        if parent == None:
            parent = runtime.base.aspect2d

        options = (
            ('relief',          None,                           None),
            ('geom',            DGG.get_default_dialog_geom(),  None), 
            ('draggable',       0,                              None),
            ('state',           DGG.NORMAL,                     None), 
            ('flatten',         1,                              None),
            ('textMayChange',   0,                              None))

        # Merge keyword options with default options
        self.defineoptions(kw, options)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(QuestParchmentFrame)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestStatusDialog(DirectDialog, core.QuestObject):
    """
    Custom implementation of the Panda3D DirectDialog object for displaying status messages to the user. 
    """

    def __init__(self, message: str = None, parent: object = None, fade_screen: float = 0, **kw: dict):

        if parent == None:
            parent = runtime.base.aspect2d

        options = (
            ('topPad',              0.15,                   DGG.INITOPT),
            ('midPad',              0.10,                   DGG.INITOPT),
            ('sidePad',             0.1,                    DGG.INITOPT),
            ('button_pad',          (0,0),                  None),
            ('button_relief',       None,                   None),
            ('button_text_pos',     (0,-0.01),              None),
            ('text_align',          p3d.TextNode.ACenter,   None),
            ('text_font',           DGG.getDefaultFont(),   None),
            ('text_wordwrap',       15,                     None),
            ('text_scale',          0.05,                   None),
            ('fadeScreen',          fade_screen,            None),
            ('image_color',         (1, 1, 1, 1),           None),
            ('bgBuffer',            0.025,                  None),
            ('relief',              None,                   None),
            ('frameSize',           (-0.5, 0.5, -0.5, 0.5), None),
            ('cornerWidth',         0.15,                   None), 
            ('draggable',           0,                      None),
            ('flatten',             1,                      None),
            ('text',                message,                None))

        # Merge keyword options with default options
        self.defineoptions(kw, options)
        DirectDialog.__init__(self, parent)
        core.QuestObject.__init__(self)
        self.initialiseoptions(QuestDirectDialog)
        self.hide()

    def set_message(self, message: str = None) -> None:
        """
        Sets the currently displayed status message
        """

        self.setMessage(message = message)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class QuestDirectDialog(DirectDialog, core.QuestObject):
    """
    """

    def __init__(self, message: str = None, parent: object = None, callback: object = None, fade_screen: float = 0, **kw: dict):

        if parent == None:
            parent = runtime.base.aspect2d
        self._callback = callback

        # TODO: properly handle styling and button options
        card_models = get_default_dialog_button_geoms()
        button_image_data = (card_models.find('**/btn_green_relief'), card_models.find('**/btn_green_pressed'), card_models.find('**/btn_green_pressed'))

        button_values = [DGG.DIALOG_OK]
        button_text = ['OK']
        button_images = [button_image_data]

        options = (
            ('buttonImageList',     button_images,          DGG.INITOPT),
            ('buttonTextList',      button_text,            DGG.INITOPT),
            ('buttonValueList',     button_values,          DGG.INITOPT),
            ('topPad',              0.15,                   DGG.INITOPT),
            ('midPad',              0.10,                   DGG.INITOPT),
            ('sidePad',             0.1,                    DGG.INITOPT),
            ('button_pad',          (0,0),                  None),
            ('button_relief',       None,                   None),
            ('button_text_pos',     (0,-0.01),              None),
            ('text_align',          p3d.TextNode.ACenter,   None),
            ('text_font',           DGG.getDefaultFont(),   None),
            ('text_wordwrap',       15,                     None),
            ('text_scale',          0.05,                   None),
            ('fadeScreen',          fade_screen,            None),
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
        self.initialiseoptions(QuestDirectDialog)
        self.hide()

    def set_message(self, message: str = None) -> None:
        """
        Sets the currently displayed dialog message
        """

        self.setMessage(message = message)

    def set_callback(self, callback: object = None) -> None:
        """
        """

        self._callback = callback

    def handle_button(self, value: object) -> None:
        """
        """

        if self._callback != None:
            self._callback(value)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #