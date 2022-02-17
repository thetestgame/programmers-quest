from six import with_metaclass

from panda3d.core import ConfigVariable, ConfigVariableList, ConfigVariableString
from panda3d.core import ConfigVariableFilename, ConfigVariableBool, ConfigVariableInt
from panda3d.core import ConfigVariableDouble, ConfigVariableColor, ConfigVariableInt64
from panda3d.core import ConfigVariableSearchPath, ConfigFlags, Filename
from panda3d.core import load_prc_file as _load_prc_file
from panda3d.core import load_prc_file_data as _load_prc_file_data

from quest.engine import runtime
from quest.engine.logging import get_notify_category as __get_notify_category
from quest.engine.vfs import path_exists

#----------------------------------------------------------------------------------------------------------------------------------#

__prc_notify = __get_notify_category('prc')
__prc_notify.setInfo(True)

def load_prc_file_data(data: str, label: str = '') -> None:
    """
    Loads the requested string of PRC data into the Panda3D
    runtime configuration under the requested label if 
    provided. Otherwise empty string
    """

    assert data != None
    assert label != None

    # Check if the base has already been defined
    # if it has been defined warn the user.
    if runtime.has_base():
        __prc_notify.warning('Showbase has already been defined. PRC changes may be ignored')

    if label != '' and label.isspace() == False:
        __prc_notify.info('Setting PRC data for label: %s' % label)
    _load_prc_file_data(label, data)

def load_prc_file(path: str, optional: bool = False) -> bool:
    """
    Attempts to load a prc file into the application. Returns
    True if succesful otherwise False
    """

    # Check if the base has already been defined
    # if it has been defined warn the user.
    if runtime.has_base():
        __prc_notify.warning('Showbase has already been defined. PRC changes may be ignored')

    if not path_exists(path) and not optional:
        __prc_notify.error('Failed to load prc file: %s. File does not exist' % path)
        return False
    
    # Return if the path does not exist and we are optional
    if not path_exists(path) and optional:
        __prc_notify.warning('Skipping optional prc: %s' % path)
        return False

    if optional:
        __prc_notify.info('Loading optional runtime config: %s' % path)
    else:
        __prc_notify.info('Loading runtime config: %s' % path)
    
    _load_prc_file(Filename.from_os_specific(path))
    return True

def get_prc_list(key: str) -> list:
    """
    Retrieves a int variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    return ConfigVariableList(key)

def get_prc_search_path(key: str, default: int = 0) -> object:
    """
    Retrieves a search path variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableSearchPath(key, default)
    return variable.get_value()

def get_prc_color(key: str, default: int = 0) -> object:
    """
    Retrieves a color variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableColor(key, default)
    return variable.get_value()

def get_prc_filename(key: str, default: int = 0) -> object:
    """
    Retrieves a filename variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableFilename(key, default)
    return variable.get_value()

def get_prc_double(key: str, default: int = 0) -> float:
    """
    Retrieves a double variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableDouble(key, default)
    return variable.get_value()

def get_prc_int64(key: str, default: int = 0) -> int:
    """
    Retrieves a int64 variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableInt64(key, default)
    return variable.get_value()

def get_prc_int(key: str, default: int = 0, list_result: bool = False) -> object:
    """
    Retrieves a int variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    if default is None:
        default = 0

    variable = ConfigVariableInt(key, default)
    num_words = variable.get_num_words()
    if num_words > 0 and list_result:
        return [variable.get_word(i) for i in range(num_words)]
    else:
        return variable.get_value()

def get_prc_string_value(key: str, default: str = '') -> str:
    """
    Retrieves a string variable from the Panda3D
    runtime configuration if present using the
    get_string_value method. Otherwise returns 
    the default value
    """

    variable = ConfigVariableString(key)
    value = variable.get_string_value()
    if not value:
        value = default

    return value

def get_prc_string(key: str, default: str = '') -> str:
    """
    Retrieves a string variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableString(key, default)
    return variable.get_value()

def get_prc_bool(key: str, default: bool = False) -> bool:
    """
    Retrieves a boolean variable from the Panda3D
    runtime configuration if present. Otherwise
    the default value
    """

    variable = ConfigVariableBool(key, default)
    return variable.get_value()

def get_prc_value_type(key: str) -> object:
    """
    Returns the value type of the Panda3D runtime configuration
    key if it exists
    """

    return ConfigVariable(key).get_value_type()

def set_prc_string_value(key: str, value: str) -> None:
    """
    Sets the requested string key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariable(key).set_string_value(value)

def set_prc_string(key: str, value: str) -> None:
    """
    Sets the requested string key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableString(key).set_value(value)

def set_prc_filename(key: str, value: object) -> None:
    """
    Sets the requested filename key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableFilename(key).set_value(value)

def set_prc_bool(key: str, value: bool) -> None:
    """
    Sets the requested boolean key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableBool(key).set_value(value)

def set_prc_int(key: str, value: int) -> None:
    """
    Sets the requested int key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableInt(key).set_value(value)

def set_prc_double(key: str, value: float) -> None:
    """
    Sets the requested double/float key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableDouble(key).set_value(value)

def set_prc_search_path(key: str, value: str) -> None:
    """
    Sets the requested search path key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableSearchPath(key).set_value(value)

def set_prc_int64(key: str, value: str) -> None:
    """
    Sets the requested int64 key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableInt64(key).set_value(value)

def set_prc_color(key: str, value: str) -> None:
    """
    Sets the requested color key and value inside the Panda3D runtime
    configuration.
    """

    ConfigVariableColor(key).set_value(value)

__prc_type_map = {
    ConfigVariable.VT_undefined: (get_prc_string_value, set_prc_string_value),
    ConfigVariable.VT_list: (get_prc_list, None),
    ConfigVariable.VT_string: (get_prc_string, set_prc_string),
    ConfigVariable.VT_filename: (get_prc_filename, set_prc_filename),
    ConfigVariable.VT_bool: (get_prc_bool, set_prc_bool),
    ConfigVariable.VT_int: (get_prc_int, set_prc_int),
    ConfigVariable.VT_double: (get_prc_double, get_prc_double),
    ConfigVariable.VT_enum: (get_prc_string_value, set_prc_string_value),
    ConfigVariable.VT_search_path: (get_prc_search_path, set_prc_search_path),
    ConfigVariable.VT_int64: (get_prc_int64, set_prc_int64),
    ConfigVariable.VT_color: (get_prc_color, set_prc_color)
}

def get_prc_value(key: str, default: object = None) -> object:
    """
    Attempts to retrieve the Panda3D runtime configuration key
    using its predicted value type. Returns the retrieved
    value or default if its invalid or not found
    """

    value_type = get_prc_value_type(key)
    type_info = __prc_type_map.get(value_type, None)
    if type_info is None:
        raise ValueError('PRC type (%s) is not a valid prc value type.' % value_type)

    getter, setter = type_info
    if getter is None:
        __prc_notify.warning('PRC type (%s) does not support value retrieval' % value_type)
        return

    value = getter(key, default)
    return value

def set_prc_value(key: str, value: object) -> None:
    """
    Sets the value of the Panda3D runtime configuration key
    if its supported by the value type
    """

    value_type = get_prc_value_type(key)
    type_info = __prc_type_map.get(value_type, None)
    if type_info is None:
        raise ValueError('PRC type (%s) is not a valid prc value type.' % value_type)

    getter, setter = type_info
    if setter is None:
        __prc_notify.warning('Failed to set key: %s. PRC type (%s) does not support value setting' % (key, value_type))
        return

    setter(key, value)

def has_prc_key(key: str) -> bool:
    """
    Returns true if the requested key was defined in the Panda3d
    engine configuration
    """

    return ConfigVariable(key).has_value()

def get_config_manager() -> object:
    """
    Returns the Panda3D ConfigVariableManager object
    """

    from panda3d.core import ConfigVariableManager
    return ConfigVariableManager.get_global_ptr()

#--------------------------------------------------------------------------------------------------------------------