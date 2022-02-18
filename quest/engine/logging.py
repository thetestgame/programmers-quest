import traceback
from logging import StreamHandler

#----------------------------------------------------------------------------------------------------------------------------------#

def get_notify_categories() -> object:
    """
    Retrieves all Panda3D notifier categories
    """

    from direct.directnotify.DirectNotifyGlobal import directNotify
    return directNotify.getCategories()

def get_notify_category(name: str, create: bool = True) -> object:
    """
    Returns the requested Panda3D notifier category. Creating a new
    one if create is set to True
    """

    assert name != None
    assert name != ''

    from direct.directnotify.DirectNotifyGlobal import directNotify

    category = None
    if create:
        category = directNotify.newCategory(name)
    else:
        category = directNotify.getCategory(name)
    return category

def log(message: str, name: str = 'global', type: str = 'info') -> None:
    """
    Writes a message to the requested logger name
    """

    category = get_notify_category(name)
    assert hasattr(category, type), '%s is not a valid notify log type' % type
    getattr(category, type)(message)

def log_error(message: str, name: str = 'global') -> None:
    """
    Writes an error message to the requested logger name
    """

    log(message, name, 'error')

def log_warn(message: str, name: str = 'global') -> None:
    """
    Writes an warn message to the requested logger name
    """

    log(message, name, 'warning')

def log_info(message: str, name: str = 'global') -> None:
    """
    Writes an info message to the requested logger name
    """

    log(message, name, 'info')

def log_debug(message: str, name: str = 'global') -> None:
    """
    Writes an debug message to the requested logger name
    """

    log(message, name, 'debug')

def condition_error(logger: object, condition: bool, message: str) -> None:
    """
    Writes a error message to the logging object if the provided
    condition is true
    """

    condition_log(logger, condition, message, 'error')

def condition_warn(logger: object, condition: bool, message: str) -> None:
    """
    Writes a warning message to the logging object if the provided
    condition is true
    """

    condition_log(logger, condition, message, 'warning')

def condition_info(logger: object, condition: bool, message: str) -> None:
    """
    Writes a info message to the logging object if the provided
    condition is true
    """

    condition_log(logger, condition, message, 'info')

def condition_debug(logger: object, condition: bool, message: str) -> None:
    """
    Writes a debug message to the logging object if the provided
    condition is true
    """

    condition_log(logger, condition, message, 'debug')

def condition_log(logger: object, condition: bool, message: str, type: str = 'info') -> None:
    """
    Writes a message to the logging object if the provided
    condition is true using the supplied type attribute function name
    """

    assert hasattr(logger, type)
    if condition:
        getattr(logger, type)(message)

#----------------------------------------------------------------------------------------------------------------------------------#

try:
    import sentry_sdk
    has_sentry = True
except ImportError:
    has_sentry = False

_sentry_configured = False

def sentry_log_exception(ex: Exception) -> None:
    """
    Handles application exceptions and logs them to Sentry.io if enabled
    """

    assert has_sentry == True
    sentry_sdk.capture_exception(ex)

def install_sentry(dsn: str, **kwargs) -> None:
    """
    Installs the Sentry.io logging cabilities if available
    """

    notify = get_notify_category('sentry')
    if not has_sentry:
        notify.warn('Failed to install sentry.io support. sentry_sdk not found. It is recommended sentry be used in production.')
        return
    
    sentry_sdk.init(dsn, **kwargs)

    global _sentry_configured
    _sentry_configured = True

def add_sentry_breadcrumb(*args, **kwargs) -> None:
    """
    """

    if not has_sentry: return
    sentry_sdk.add_breadcrumb(*args, **kwargs)

def set_sentry_context(label: str, data: dict = {}) -> None:
    """
    """

    if not has_sentry: return
    sentry_sdk.set_context(label, data)

def set_sentry_user(details: dict = None) -> None:
    """
    """

    if not has_sentry: return
    sentry_sdk.set_user(details)

#----------------------------------------------------------------------------------------------------------------------------------#

class NotifyHandler(StreamHandler):
    """
    Custom StreamHandler for bridging Python logging to Panda3D notify
    """

    def emit(self, record: object) -> None:
        """
        Passes a Python LogRecord instance through to the Panda3D Notify category 
        """

        notify_cat = get_notify_category(record.name)
        log_level = record.level

        notify_funcs = {
            0: 'debug',
            1: 'info',
            2: 'warn',
            3: 'error',
            4: 'error'
        }
        func_name = notify_funcs.get(log_level, 'warn')
        getattr(notify_cat, func_name)(record.message)

#----------------------------------------------------------------------------------------------------------------------------------#

def configure_logging(sentry_dsn: str = None) -> None:
    """
    """

    #TODO: finish this

def capture_exception(ex: Exception) -> None:
    """
    """

    # Log our exception with Sentry if currently configured
    if _sentry_configured:
        sentry_log_exception(ex)

    # Print out our stack trace for developers
    print(traceback.format_exc())

#-----------------------------------------------------------------------------------------