import re
import os
import sys
import datetime
import itertools
import datetime
import types
import gc
import functools

from math import floor, ceil
from functools import reduce

from panda3d.core import Filename, Point2, Point3
from panda3d.core import Vec3

from quest.engine import runtime
from quest.engine.logging import get_notify_category

__utility_notify = get_notify_category('utilities')

_SNAKE_NAME_RE = re.compile('(?<!^)(?=[A-Z])')

def get_snake_case(text: str, splitter='_') -> str:
    """
    Returns the snake case version of the requested string
    """

    return _SNAKE_NAME_RE.sub(splitter, text).lower()

def get_camel_case(text: str, splitter='_') -> str:
    """
    Returns the camel case version of the requested string
    """

    return ''.join(x.capitalize() or splitter for x in text.split(splitter))

def open_web_url(url: str) -> bool:
    """
    Attempts to open the website url. Returning true on sucess
    otherwise False on failure.
    """

    success = False
    if sys.platform == 'darwin':
        os.system('/usr/bin/open %s' % url)
    elif system.platform == 'linux':
        import webbrowser
        webbrowser.open(url)
        success = True
    else:
        try:
            import webbrowser
            webbrowser.open(url)
            success = True
        except:
            os.system('explorer "%s"' % url)

    return success

def get_time_as_string(seconds: bool = False) -> str:
    """
    Returns the current time as a string
    """

    now = datetime.datetime.now()
    output = None
    if seconds:
        output = '%02d:%02d:%02d' % (now.hour, now.minute, now.second)
    else:
        output = '%02d:%02d' % (now.hour, now.minute)

    return output

def is_awaitable_function(func: object) -> bool:
    """
    Returns true if the function is awaitable
    """

    assert func != None
    assert callable(func)

    import inspect
    return inspect.iscoroutinefunction(func)

def run_func_async(func: object, name: str = None) -> None:
    """
    Runs a the requested function under a coroutine
    """

    assert func != None
    assert callable(func)

    if name is None:
        name = '%s-async-task' % func.__name__

    async def async_wrapper(task) -> int:
        """
        Async wrapper for the callback
        """

        await func()
        return task.done

    create_task(async_wrapper, name)

def perform_callback_on_condition(condition: bool, callback: object, *args, **kwargs) -> None:
    """
    Performs the required callback if the condition is True
    """

    assert callback != None
    assert callable(callback)

    # Check if the condition is true
    if not condition:
        return

    if is_awaitable_function(callback):
        run_func_async(callback, '%s-callback-async' % callback.__name__)
    else:
        callback(*args, **kwargs)

def perform_dependency_check(library_name: str, import_path: str = None) -> None:
    """
    Performs a check to ensure the required dependency is installed.
    If the dependency is not found a MissingThirdpartySupportError 
    is thrown to inform the user
    """

    if import_path is None:
        import_path = library_name

    import importlib
    found = False
    try:
        module = importlib.import_module(import_path)
        found = True
    except:
        pass

    if not found:
        raise exceptions.MissingThirdpartySupportError(library_name)

def __create_task_name(obj, task):
    """
    Creates a name for a task based on the obj its being used on
    """

    cls_name = obj.__class__.__name__
    if hasattr(obj, 'get_name'):
        name = obj.get_name()
        return '%s.%s(%s)' % (cls_name, task, name)

    return '%s.%s(<%d>)' % (cls_name, task, id(obj))

def create_task(task_func, task_name = '', priority = 0, task_chain_name: str = None):
    """
    Creates a new task with the task manager
    """

    task_name = __create_task_name(task_func.__self__, task_name or task_func.__name__)
    return runtime.task_mgr.add(task_func, task_name, priority, taskChain=task_chain_name)

def create_delayed_task(task_func, delay, task_name = '', priority = 0):
    """
    Creates a new delayed task with the task manager
    """

    task_name = __create_task_name(task_func.__self__, task_name or task_func.__name__)
    return runtime.task_mgr.do_method_later(task_func, task_name, priority)

def remove_task(task):
    """
    Removes a task from the task manager
    """

    runtime.task_mgr.remove(task)

def create_thread(thread_name, thread_priority=0, prc_check: str = None):
    """
    Creates a new task manager thread
    """

    threads=0
    if prc_check != None:
        from quest.engine import prc
        if prc.get_prc_bool(prc_check, False):
            threads=1

    runtime.task_mgr.setupTaskChain(
        thread_name, 
        numThreads=threads, 
        threadPriority=thread_priority)

def diffs(lst1, lst2):
    """
    """

    return reduce(lambda x, y: x + y, itertools.starmap(lambda e1, e2: int(not e1 == e2), list(zip(lst1, lst2))))

def delegate(self, call) -> None:
    """
    """

    func_name = call.__func__.__name__
    setattr(self, func_name, call)

def null_generator():
    """
    Defines a null yield generator
    """

    if False:
        yield

def open_os_directory(path: str) -> bool:
    """
    Opens a directory path in the operation system's file explorer.
    Returning true on success, otherwise false.
    """

    success = False
    if sys.platform == 'darwin':
        __utility_notify.warning('open_os_directory is not supported on platform: %s' % sys.platform)
    elif sys.platform == 'linux2' or sys.platform == 'linux':
        __utility_notify.warning('open_os_directory is not supported on platform: %s' % sys.platform)
    else:
        os.system('explorer "%s"' % path)
        success = True

    return success

def get_local_data_directory() -> str:
    """
    Returns the application's local data directory
    """

    from quest.engine import prc
    folder_name = prc.get_prc_string('data-folder', 'Quest')

    if sys.platform in ['win32', 'cygwin', 'msys']:
        return os.path.join(os.getenv('LOCALAPPDATA'), folder_name)
    else:
        __utility_notify.warning('get_local_data_directory is not supported on platform: %s. Defaulting to install directory' % sys.platform)
        return '.'

def get_local_data_path(path: str) -> str:
    """
    Returns the path relative to the application's local data directory
    """

    return os.path.join(get_local_data_directory(), path)
 
def get_screenshot_directory(absolute: bool = False) -> str:
    """
    Returns the application's screenshot directory
    """
    
    return get_local_data_path('screenshots')

def open_screenshot_directory() -> bool:
    """
    Opens the application's screenshot directory in the operation system's
    file browser window. Returning true on success, otherwise false.
    """

    return open_os_directory(get_screenshot_directory(True))

def build_screenshot_filename(basename: str = 'screenshot', directory: str = None, format: str = 'png') -> str:
    """
    Builds the file path for a newly created screenshot
    """

    if directory is None:
        directory = get_screenshot_directory()

    now = datetime.datetime.now()
    filename = now.strftime(basename + '_%y%m%d_%H%M%S')
    path = os.path.join(directory, filename +' .' + format)
    appendix = 0

    while os.path.exists(path):
        appendix += 1
        path = os.path.join(directory, filename + '_' + str(appendix) + '.' + format)

    return path

def save_screenshot(directory: str = None, format: str = 'png', win: object = None):
    """
    Saves a screenshot of the current render output to file
    """

    if not win:
        win = runtime.base.win

    path = build_screenshot_filename(directory=directory, format=format)
    win.save_screenshot(Filename(path))
    __utility_notify.info('Saved Screenshot: %s' % path)

def foreach(sequence: list, callable: object, *args, **kwargs) -> None:
    """
    Iterates through a sequence performing a callback on each element
    """

    for element in sequence:
        callable(element, *args, **kwargs)

def foreach_call_method_by_name(sequence: list, method_name: str, *args, **kw) -> list:
    """
    """

    results = []
    for element in sequence:
        callable = getattr(element, method_name, None)
        if callable:
            results.append(callable(*args, **kw))

    return results

BACKGROUND_THREAD_NAME = 'background-tasks'

def start_background_thread() -> None:
    """
    Starts a background thread chain in the Panda3D
    task manager
    """

    runtime.task_mgr.setupTaskChain(
        BACKGROUND_THREAD_NAME, 
        numThreads = 1,
        threadPriority = 0)

def map_point_to_screen(nodepath: object, point: object) -> object:
    """
    """

    p3 = runtime.cam.get_relative_point(nodepath, point)
    p2 = Point2()

    if not runtime.base.camlens.project(p3, p2):
        return None

    r2d = Point3(p2[0], 0, p2[1])
    a2d = runtime.base.aspect2d.get_relative_point(runtime.base.render2d, r2d)

    return a2d

def snap_to_grid(node_path: object, grid_size: object) -> tuple:
    """
    """

    x, y, z = node_path[0], node_path[1], node_path[2]
    return (floor(x / grid_size[0]) * grid_size[0], floor(y / grid_size[1]) * grid_size[1], floor(z / grid_size[2]) * grid_size[2])

def get_bounds_of_model(model: object, rotation: float = 0.0) -> tuple:
    """
    """

    h = model.get_h()
    model.set_h(rotation)
    min_corner, max_corner = model.get_tight_bounds()
    model.set_h(h)
    delta = max_corner - min_corner

    return (min_corner, max_corner, Vec3(int(ceil(round(delta.get_x(), 1))), int(ceil(round(delta.get_y(), 1))), int(ceil(round(delta.get_z(), 1)))))

def write_ini_file(filepath: str, input: object, output: object, template: str = '[Configuration]\n\n[Model]\n%(output)s: %(input)s\n') -> None:
    """
    Writes a new ini file to the requested output path location
    """

    __utility_notify.info('write_ini_file: Creating ini file for "%s"... ' % input)
    fh = open(filepath, 'w')
    fh.write(template % {'input': input, 'output': output})
    fh.close()

def has_attributes(object: object, attributes: list) -> list:
    """
    """

    return reduce(bool.__and__, [ hasattr(object, attr) for attr in attributes ])

def get_refcounts() -> list:
    """
    Returns a list of all references in the application
    """

    d = {}
    import sys.modules
    for m in list(sys.modules.values()):
        for sym in dir(m):
            o = getattr(m, sym)
            if type(o) is type:
                d[o] = sys.getrefcount(o)

    pairs = [(refcount, cls) for cls, refcount in list(d.items())]
    pairs.sort(reverse=True)

    return pairs

def get_all_references_of_type(t: object) -> list:
    """
    """

    result = []
    for r in gc.get_referrers(t):
        if isinstance(r, t):
            result.append(r)

    return result

def print_refcounts(max_refcounts: int = None) -> None:
    """
    """

    refcount_list = get_refcounts()
    if max_refcounts is not None:
        refcount_list = refcount_list[max_refcounts]
    
    for n, c in refcount_list:
        print('%10d %s (%s) instances: %d' % (
            n, c.__name__, str(c), len(get_all_references_of_type(c))))

def print_unreachable_garbage() -> None:
    """
    """

    garbage_list = gc.garbage
    if len(garbage_list) == 0:
        print('No garbage found')
    else:
        print('%d object in garbage found: ' % len(garbage_list))
        for garbage in garbage_list:
            print(str(garbage))

def to_unicode(string: str) -> str:
    """
    """

    if type(string) == str:
        return string

    try:
        return str(string.decode('utf-8'))
    except UnicodeError:
        return ''

def utf8_capitalize(string: str) -> str:
    """
    """

    return to_unicode(string).capitalize().encode('utf-8')

def utf8_lower(string: str) -> str:
    """
    """

    return to_unicode(string).lower().encode('utf-8')

class _DoMethodAfterNFrames(object):
    """
    """

    def __init__(self, frames_to_wait: int, method: object, args: list):
        self.__frames_to_wait = frames_to_wait
        self.__method = method
        self.__args = args

    def task_function(self, task: object) -> int:
        """
        """

        self.__frames_to_wait -= 1
        
        if self.__frames_to_wait <= 0:
            self.__method(*self.__args)

            return task.done

        return task.cont

def do_method_after_n_frames(frames_to_wait: int, method: object, args: list = [], priority: int = 0) -> None:
    """
    """

    if frames_to_wait > 0:
        create_task(_DoMethodAfterNFrames(frames_to_wait, method, args).task_func, priority=priority)
    else:
        __utility_notify.error('Invalid request. do_method_after_n_frames received a frames wait of 0')