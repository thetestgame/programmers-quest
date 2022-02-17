from quest.engine import logging as _logging
from quest.engine import runtime as _runtime

from panda3d.core import PStatCollector as _PStatCollector
from panda3d.core import PStatClient as _PStatClient

#----------------------------------------------------------------------------------------------------------------------------------#

_notify = _logging.get_notify_category('performance')
_client = None

def get_profile_client() -> _PStatClient:
    """
    Returns the application's profiler client instance
    """

    global _client
    if _client is None:
        _client = _PStatClient()
    
    return _client

def is_profiling() -> bool:
    """
    Returns true if the application is currently being
    profiled
    """

    client = get_profile_client()
    return client.is_connected()

def connect_profiler(*args, **kwargs) -> bool:
    """
    Connects the application to a profiler server
    """

    if is_profiling():
        _notify.warning('Failed to connect profiler. A profiler is already connected')
        return False

    client = get_profile_client()
    client.connect(*args, **kwargs)

def disconnect_profiler() -> None:
    """
    Disconnects the application from a profiler server if it
    is currently connected
    """

    if not is_profiling():
        return

    client = get_profile_client()
    client.disconnect()

def toggle_profiling() -> None:
    """
    Toggles the current application profiling setting. Connecting
    to a server available at localhost
    """

    if is_profiling():
        connect_profiler()
    else:
        disconnect_profiler()

def resume_profiling_after_pause() -> None:
    """
    Resumes the profiling client after the simuilation has been paused for a while.
    This allows stats to continue exactly where it left off, instead of leaving a big gap that would represent
    a chug in the application's performance
    """

    client = get_profile_client()
    client.resume_after_pause()

def get_collector(label: str) -> _PStatCollector:
    """
    Creates and returns a new pstats collector instance
    """

    return _PStatCollector(label)

def _has_custom_collectors() -> bool:
    """
    Returns true if the custom_collectors dictionary
    is defined on our runtime instance
    """

    return hasattr(_runtime, 'custom_collectors')

def _has_custom_collector(name: str) -> bool:
    """
    Returns true if the custom collector currently
    exists
    """

    return name in _get_custom_collectors()

def _get_custom_collector(name: str) -> _PStatCollector:
    """
    Returns the custom collector if it exists
    """

    return _get_custom_collectors().get(name, None)

def _get_custom_collectors() -> list:
    """
    Returns a complete list of custom collectors
    """

    if not _has_custom_collectors():
        return []

    return _runtime.custom_collectors

def _create_custom_collector(collector_name: str) -> object:
    """
    Creates and returns a custom PStatCollector
    instance
    """

    if not _has_custom_collectors():
        _runtime.custom_collectors = {}

    if _has_custom_collector(collector_name):
        _notify.warning('Attempted to create a new collector when it already exists! Name: %s' % collector_name)
        return _runtime.custom_collectors[collector_name]

    _runtime.custom_collectors[collector_name] = _PStatCollector(collector_name)
    return _runtime.custom_collectors[collector_name]

def stat_collection(func: object) -> object:
    """
    Wraps a function with a Panda3D PStatCollector object
    for timing its performance
    """

    collector_name = 'Debug:%s' % func._name_
    if _has_custom_collector(collector_name):
        pstat = _get_custom_collector(collector_name)
    else:
        pstat = _create_custom_collector(collector_name)

    def do_pstat(*args, **kwargs) -> object:
        """
        Performs the timing operations for the
        wrapped function
        """

        pstat.start()
        results = func(*args, **kwargs)
        pstat.stop()

        return results

    do_pstat._name_ = func._name_
    do_pstat._dict_ = func._dict_
    do_pstat._doc_ = func._doc_

    return do_pstat

# Simplified decorator alias
pstat = stat_collection

#----------------------------------------------------------------------------------------------------------------------------------#