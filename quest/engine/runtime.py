import builtins
import sys as __sys

#----------------------------------------------------------------------------------------------------------------------------------#

def __get_module() -> object:
    """
    Returns the runtime module's object instance
    """

    return __sys.modules[__name__]

def __has_variable(variable_name: str) -> bool:
    """
    Returns true if the runtime module has the requested variable name defined.
    Is served out via the custom __getattr__ function as has_x() method names
    """

    module = __get_module()
    defined = hasattr(module, variable_name)
    found = False

    if defined:
        attr = getattr(module, variable_name)
        found = attr != None

    return found

def __get_variable(variable_name: str) -> object:
    """
    Returns the requested variable from the runtime module if it exists.
    Otherwise returning NoneType
    """

    if not __has_variable(variable_name):
        return None

    module = __get_module()
    return getattr(module, variable_name)

def __getattr__(key: str) -> object:
    """
    Custom get attribute handler for allowing access to the has_x method names
    of the engine runtime module. Also exposes the builtins module
    for the legacy Panda3d builtins provided by the ShowBase instance
    """

    result = None
    is_has_method = key.startswith('has_')
    is_get_method = key.startswith('get_')

    if len(key) > 4:
        variable_name = key[4:]
    else:
        variable_name = key

    if is_has_method:
        result = lambda: __has_variable(variable_name)
    elif is_get_method:
        result = lambda: __get_variable(variable_name)
    elif hasattr(builtins, key):
        result = getattr(builtins, key)

    if not result:
        raise AttributeError('runtime module has no attribute: %s' % key)

    return result

#----------------------------------------------------------------------------------------------------------------------------------#