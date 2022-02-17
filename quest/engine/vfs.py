import os
import fnmatch
import logging
from hashlib import md5

import direct.stdpy.file
import glob

from panda3d.core import VirtualFileSystem, Filename, Multifile
from panda3d.core import VirtualFileMountHTTP, VirtualFileMountRamdisk
from panda3d.core import VirtualFileMountSystem, VirtualFileMountMultifile
from panda3d.core import get_model_path, DSearchPath, URLSpec, HTTPClient

from quest.engine import logging, runtime

#----------------------------------------------------------------------------------------------------------------------------------#

__file_notify = logging.get_notify_category('file-system')
__file_notify.setInfo(True)

def os_path_exists(path: str) -> bool:
    """
    OS function for verifying if a file exists
    """

    return os.path.exists(path)

def os_path_is_dir(path: str) -> bool:
    """
    OS function for checking if a path is a 
    directory
    """

    return os.path.isdir(path)

def os_get_file_date(path: str) -> int:
    """
    OS function for retrieving the file
    date from a path
    """

    exists = os.path.exists(path)
    date = 0 

    if exists:
        stat = os.stat(path)
        date = stat.st_mtime

    return date

def os_get_file_size(filehandle: object) -> float:
    """
    OS function for retrieving the file
    size
    """

    stat = os.fstat(filehandle.fileno())
    return stat.st_size

def os_get_matching_files(path: str, pattern: str) -> list:
    """
    OS function for retrieving all
    pattern matching files in the directory
    """

    return glob.glob(os.path.join(path, pattern))

_vfs = VirtualFileSystem.get_global_ptr()

def vfs_path_exists(path: str) -> bool:
    """
    Panda3D VFS function for verifying if a path exists
    """

    return _vfs.exists(Filename(path))

def vfs_path_is_dir(path: str) -> bool:
    """
    Panda3D VFS function for verifying if a path is a 
    directory
    """

    return _vfs.is_directory(path)

def vfs_get_file_date(path: str) -> int:
    """
    Panda3d VFS function for retrieving a file 
    date
    """

    fh = _vfs.get_file(Filename(path), status_only=True)
    date = 0

    if fh:
        date = fh.get_timestamp()

    return date

def vfs_get_file_size(filehandle: object) -> float:
    """
    Panda3D VFS function for retrieving a files
    size
    """

    fh = _vfs.get_file(Filename(filehandle.name), status_only=True)
    if fh == None:
        __file_notify.warning('Failed to retrieve file size for file: %s. Defaulting to -1' % filehandle.name)
        return -1

    return fh.get_file_size(filehandle._file__stream)

def vfs_get_matching_files(path: str, pattern: str) -> list:
    """
    Panda3D VFS function for retrieving all
    files in the directory matching
    the string pattern
    """

    found_files = []
    result = _vfs.scan_directory(Filename(path))
    if result:
        for i in range(result.get_num_files()):
            filename = result.get_file(i).get_filename().get_basename()
            if fnmatch.fnmatch(filename, pattern):
                found_files.append(fixed_join(path, filename))

    return found_files

def fix_path(path: str) -> str:
    """
    Replaces the system path sep with a forward slash
    """

    return path.replace(os.sep, '/')

def fixed_join(lhs: str, rhs: str) -> str:
    """
    Joins two paths together and then runs fix_path on the resulting
    path string
    """

    return fix_path(os.path.join(lhs, rhs))

def get_file_extension(path: str) -> str:
    """
    Returns the path's file extension if present
    """

    parts = path.split('.')
    if len(parts) > 1:
        return parts[-1]
    return None

def file_md5(path: str, blocksize: int = 1024) -> object:
    """
    Returns a files md5 hash from its path
    """

    m = md5()
    if path_exists(path):
        fh = file(path, 'rb')
        data = [1]
        accumulated = 0

        while len(data) > 0:
            data = fh.read(blocksize)
            accumulated += len(data)
            m.update(data)

        fh.close()
    else:
        __file_notify.warning('Failed to compute MD5 has for %s. File does not exist' % path)

    return m.digest()

def correct_path_case(path: str) -> str:
    """
    """

    if path and os_path_exists(path):
        path = fix_path(path)
        path_components = path.split('/')
        
        current_path = ''
        fixed_path = ''

        for pc in path_components:
            current_path = os.path.join(current_path, pc)
            dirpath = os.path.split(os.path.realpath(current_path))[0]
            if os_path_exists(dirpath):
                files = os.listdir(dirpath)
                if pc in files or pc == '.' or pc == '..':
                    fixed_path = os.path.join(fixed_path, pc)
                else:
                    files_lower = [filename.lower() for filename in files]
                    pc_lower = pc.lower()

                    if pc_lower in files_lower:
                        idx = files_lower.index(pc_lower)
                        fixed_path = os.path.join(fixed_path, files[idx])
            else:
                return path

        return fix_path(fixed_path)

    return path

def check_file_path(path: str) -> str:
    """
    """

    if not path:
        return

    return correct_path_case(path)

__path_exists_func = os_path_exists
__path_is_dir_func = os_path_is_dir
__get_file_date_func = os_get_file_date
__get_file_size_func = os_get_file_size
__get_matching_files_func = os_get_matching_files

def path_exists(path: str) -> bool:
    """
    Returns true if the requested path exists in the applications
    file system
    """

    global __path_exists_func
    return __path_exists_func(path)

def path_is_dir(path: str) -> bool:
    """
    Returns true if the requested path is a directory
    in the applications file system
    """

    global __path_exists_func
    return __path_exists_func(path)

def get_file_date(path: str) -> int:
    """
    Returns the date information from
    a file in the applications file system
    """

    global __get_file_date_func
    return __get_file_date_func(path)

def get_file_size(path: str) -> float:
    """
    Returns the size information from
    a file in the applications file system
    """

    global __get_file_size_func
    return __get_file_size_func(path)

def get_matching_files(path: str, pattern: str) -> list:
    """
    Returns all files in the directory
    matching the requested pattern
    """

    global __get_matching_files_func
    return __get_matching_files_func(path, pattern)

def switch_file_functions_to_vfs() -> None:
    """
    Switches the file access functions to use the Panda3D
    Virtual File System
    """

    global __path_exists_func
    global __path_is_dir_func
    global __get_file_size_func
    global __get_file_date_func
    global __get_matching_files_func

    __path_exists_func = vfs_path_exists
    __path_is_dir_func = vfs_path_is_dir
    __get_file_size_func = vfs_get_file_size
    __get_file_date_func = vfs_get_file_date
    __get_matching_files_func = vfs_get_matching_files

def switch_file_functions_to_os() -> None:
    """
    Switches the file access functions to use the Operating
    System's IO functions
    """

    global __path_exists_func
    global __path_is_dir_func
    global __get_file_size_func
    global __get_file_date_func
    global __get_matching_files_func

    __path_exists_func = os_path_exists
    __path_is_dir_func = os_path_is_dir
    __get_file_size_func = os_get_file_size
    __get_file_date_func = os_get_file_date
    __get_matching_files_func = os_get_matching_files

def switch_io_functions_to_vfs() -> None:
    """
    """

    from direct.stdpy import file
    __builtins__['open'] = file.open
    __builtins__['file'] = file.open

def switch_io_functions_to_os() -> None:
    """
    """

    from io import open
    __builtins__['open'] = open
    __builtins__['file'] = open

def vfs_get_mount_count() -> int:
    """
    Returns the number of individual mounts in the Virtual
    File System
    """

    return _vfs.get_num_mounts()

def vfs_get_mount(index: int) -> object:
    """
    Returns the nth mount in the Virtual File System
    """

    return _vfs.get_mount(index)

def vfs_unmount_all_directories() -> None:
    """
    Unmounts all directories from the virtual file system
    """

    _vfs.unmount_all()

def vfs_mount_directory(mount_point: str, directory: str) -> bool:
    """
    Mounts the directory to the requested mount point.
    Returning the result of the mounting operation
    """

    result = _vfs.mount(
        Filename(directory),
        Filename(mount_point),
        VirtualFileSystem.MF_read_only)

    if not result:
        __file_notify.warning('Failed to mount directory (%s) to (%s)!' % (
            directory, mount_point))

    get_model_path().append_directory(directory)
    switch_file_functions_to_vfs()
    return result

def vfs_mount_multifile(mount_point: str, multifile: str) -> bool:
    """
    Mounts the multifile to the requested mount point
    if it exists. Returning the result of the mounting
    operation
    """

    if not os_path_exists(multifile):
        return False

    m = Multifile()
    m.openReadWrite(multifile)

    __file_notify.info('Mounting MF "%s" at "%s"' % (multifile, mount_point))
    result = _vfs.mount(m, mount_point, VirtualFileSystem.MFReadOnly)
    if not result:
        __file_notify.warning('Failed to mount multifile (%s) to (%s)!' % (
            multifile, mount_point))

    get_model_path().append_directory(mount_point)
    switch_file_functions_to_vfs()
    return result

def vfs_mount_url(mount_point: str, url: str) -> bool:
    """
    Mounts a http directory to the requested mount point.
    Returning the result of the mounting operation. Best used with
    CDN or download like servers
    """

    m = VirtualFileMountHTTP('%s%s' % (url, mount_point))
    __file_notify.info('Mounting remote directory (%s) to (%s)' % (url, mount_point))
    result = _vfs.mount(m, mount_point, VirtualFileSystem.MFReadOnly)
    if not result:
        __file_notify.warning('Failed to mount url (%s) to (%s)!' % (
            url, mount_point))

    get_model_path().append_directory(mount_point)
    switch_file_functions_to_vfs()
    return result

def vfs_mount_subdirectories(mount_point: str, root_dir: str, mount_root: bool = True) -> bool:
    """
    Walks through a root directory and mounts all subdirectorys
    to the requested mount point. Generally used for development
    source version of an application or servers.
    """

    folders = [os.path.join(root_dir, o) for o in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir,o))]
    if mount_root:
        if not root_dir.endswith('/'):
            root_dir += '/'
        folders.append(root_dir)

    for folder in folders:
        
        # Ignore invalid folders
        base_name = os.path.basename(folder)
        if base_name.startswith('.'):
            continue

        folder = Filename.from_os_specific(os.path.abspath(folder))
        __file_notify.debug('Mounting (%s) to (%s)' % (folder, mount_point))
        vfs_mount_directory(mount_point, folder)

def append_subdirectories_to_search(root_dir: str, mount_root: bool = True) -> None:
    """
    Walks through a root directory and mounts all subdirectorys
    to the search path. Generally used for development
    source version of an application or servers.
    """

    model_path = get_model_path()
    folders = [os.path.join(root_dir, o) for o in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir,o))]
    if mount_root:
        if not root_dir.endswith('/'):
            root_dir += '/'
        folders.append(root_dir)

    for folder in folders:

        # Ignore invalid folders
        base_name = os.path.basename(folder)
        if base_name.startswith('.'):
            continue

        folder = Filename.from_os_specific(os.path.abspath(folder))
        __file_notify.debug('Mounting (%s) to search path' % (folder)) 
        model_path.append_directory(folder)

def reload_vfs_mount_urls() -> None:
    """
    Reads all of the vfs-mount-url lines in the Config.prc file and replaces the mount settings to match them.
    This will mount any url’s mentioned in the config file, and unmount any url’s no longer mentioned in the config file. 
    Normally, it is called automatically at startup, and need not be called again, unless you have fiddled with some config settings.
    """

    VirtualFileMountHTTP.reload_vfs_mount_url()

def is_path_multifile(path: str) -> bool:
    """
    Returns true if the requested path is a multifile
    """

    dir_exists = path_exists(path)
    if dir_exists:
        return False

    return path_exists('%s.mf' % path)

def get_search_path() -> DSearchPath:
    """
    Returns the configured panda3d model search path
    """

    search_path = get_model_path().value
    search_path.append_directory('.')

    return search_path

#----------------------------------------------------------------------------------------------------------------------------------#