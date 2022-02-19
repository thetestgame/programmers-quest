from quest.engine import runtime
from direct.gui import DirectGuiGlobals

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def set_default_dialog_geom(model_path: str) -> None:
    """
    Sets the property of DirectGuiGlobals.set_default_dialog_geom with a model
    loaded from the configured model path
    """

    model_inst = runtime.loader.load_model(model_path)
    DirectGuiGlobals.set_default_dialog_geom(model_inst)

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
