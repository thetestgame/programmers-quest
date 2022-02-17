from quest.engine import logging as _logging
import importlib as _importlib

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

_bootstrap_notify = _logging.get_notify_category('bootstrap')

def create_class_entry(object_path: str, meta: dict = {}) -> tuple:
    """
    Creates a class entry for use with the bootstrap function
    """

    parts = object_path.split('.')
    class_name = parts[-1]

    return (class_name, object_path, meta)

def create_singleton_entry(object_path: str, meta: dict = {}) -> tuple:
    """
    Creates a singleton entry for use with the bootstrap function
    """

    parts = object_path.split('.')
    class_name = parts[-1]
    path = '.'.join(parts[:-1])

    return (path, class_name, meta)

def get_class_registry() -> object:
    """
    Retrieves the environments class registry
    singleton object
    """

    from quest.framework.registry import ClassRegistry
    return ClassRegistry.instantiate_singleton()

def _import_module(module_name: str) -> object:
    """
    Imports the requested module by its module
    name import path
    """

    assert module_name != ''
    assert module_name != None

    components = module_name.split('.')
    module_path = '.'.join(components[:-1])
    module = _importlib.import_module(module_path)

    return module

def batch_instantiate_singletons(singleton_list: list) -> None:
    """
    Batch instantiates singletons from a list
    """

    for singleton in singleton_list:
        module_name, class_name, args = singleton
        module_path = '%s.%s' % (module_name, class_name)
        singleton_module = _import_module(module_path)
        if singleton_module is None:
            _bootstrap_notify.warning('Failed to setup singleton: %s. Invalid import' % class_name)
            continue

        singleton_cls = getattr(singleton_module, class_name)
        singleton_cls.instantiate_singleton(*args)

def bootstrap_module(class_list: list = [], meta_list: list = [], singleton_list: list = []) -> None:
    """
    Performs initial boostrap operations on a module
    """

    class_registry = get_class_registry()
    batch_instantiate_singletons(singleton_list)
    class_registry.batch_register_classes(class_list, meta_list)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#