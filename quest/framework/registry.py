import logging
import importlib

from quest.framework.singleton import Singleton
from quest.engine.core import QuestObject

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClassRegistry(Singleton, QuestObject):
    """
    Singleton registry containing all classes used for networking, configuration
    and casting within the quest module's framework.
    """

    def __init__(self):
        Singleton.__init__(self)
        QuestObject.__init__(self)
        
        self._classes = {}

    @property
    def classes(self) -> dict:
        """
        Getter for retrieving the registry
        classes.
        """

        return self._classes

    def __iter__(self):
        """
        Allows iteration through our known class data
        in async form.
        """

        for class_name, class_data in list(self._classes.items()):
            yield (class_name, class_data)

    def _import_module(self, module_name: str) -> object:
        """
        Imports the requested module by its module
        name import path
        """

        assert module_name != ''
        assert module_name != None

        components = module_name.split('.')
        module_path = '.'.join(components[:-1])
        module = importlib.import_module(module_path)

        return module
    
    def is_registered(self, class_name: str) -> bool:
        """
        Returns true if the class name is already registered
        with the class registry singleton
        """

        return class_name in self._classes

    def batch_register_classes(self, class_list: list, meta_list: list = []) -> None:
        """
        Batch registers classes for module setups
        """

        self.notify.debug('Batch registering %d classes...' % len(class_list))
        for class_info in class_list:
            class_name, module_name, meta = class_info
            self.notify.debug('Registering %s from module (%s) with meta (%s)' % (
                class_name, module_name, str(meta)))
            self.register_class(class_name, module_name, **meta)

        self.notify.debug('Setting %d meta key/values' % (len(meta_list)))
        for meta_info in meta_list:
            class_name, meta_key, meta_value = meta_info
            self.set_class_meta(class_name, meta_key, meta_value)

    def register_class(self, class_name: str, module_name: str, **meta) -> None:
        """
        Registers a new class with the class registry singleton
        """   

        return self.register_class_alias(class_name, class_name, module_name, **meta)    

    def register_class_alias(self, class_alias: str, class_name: str, module_name: str, **meta) -> None:
        """
        Registers a new class using an alias with the class registry singleton
        """

        # Verify the class does not already exist
        if self.is_registered(class_name):
            self.notify.warning('Failed to register class. Class "%s" already exists in the registry' % (
                class_alias))
            
            return

        self.notify.debug('Registering class (%s) as "%s"' % (class_name, class_alias))
        self._classes[class_alias] = (class_name, module_name, None, meta)

    def unregister_class(self, class_name: str) -> None:
        """
        Attempts to unregister a class from the class registry singleton
        """

        # Verify the class exists
        if not self.is_registered(class_name):
            self.notify.warning('Failed to unregister class. Class "%s" is not registered with the singleton!' % (
                class_name))

            return

        # Remove the class from the registry
        self._classes.pop(class_name)

    def get_class(self, class_name: str) -> object:
        """
        Attempts to retrieve a class from the class registry
        if it exists
        """

        # Verify the class exists
        if not self.is_registered(class_name):
            self.notify.warning('Class "%s" is not registered with the %s singleton!' % (
                class_name, self.__class__.__name__))

            return

        # Retrieve our known information about the class
        cls_name, module_name, module, meta = self._classes[class_name]

        # Update the registry if a module instance does not already exist
        if not module:
            module = self._import_module(module_name)
            self._classes[class_name] = (cls_name, module_name, module, meta)

        # Attempt to retrieve the class instance and return it to
        # the requester
        cls = getattr(module, cls_name, None)
        if not cls:
            self.notify.warning('Failed to retrieve class. Class unable to be imported: %s' % (
                class_name))

            return

        return cls

    def get_class_meta(self, class_name: str, meta_tag: str = None, default: object = None)-> object:
        """
        Attempts to retrieve the requested meta value from 
        a registered class 
        """

        # Verify the class exists
        if not self.is_registered(class_name):
            self.notify.warning('Failed to get meta. Class "%s" is not registered with the singleton!' % (
                class_name))

            return

        # Retrieve the requested tag from our known class
        # in the registry
        cls_name, module_name, module, meta = self._classes[class_name]

        if meta_tag is None:
            return meta
        else:
            return meta.get(meta_tag, default)

    def set_class_meta(self, class_name: str, meta_tag: str, meta_value: object) -> None:
        """
        Attempts to set a meta value on a class within the class registry
        """

        # Verify the class exists
        if not self.is_registered(class_name):
            self.notify.warning('Failed to set meta. Class "%s" is not registered with the singleton!' % (
                class_name))

            return

        # Set the meta key/value for the requested class
        cls_name, module_name, module, meta = self._classes[class_name]
        self.notify.debug('Setting class meta for %s. %s = %s' % (
            cls_name, meta_tag, meta_value))
        meta[meta_tag] = meta_value
    
    def query_meta(self, **meta) -> list:
        """
        Queries the class registry for all class meta data 
        matching the requested query
        """

        classes = []

        # Iterate over all known classes 
        # to compare meta data. Returning all known
        # classes that match the query data
        for class_name in self._classes:
            cls_name, module_name, module, meta = self._classes[class_name]

            for meta_tag, meta_value in list(meta.items()):
                if meta_tag in meta and meta[meta_tag] == meta_value:
                    cls = self.get_class(class_name)
                    if cls:
                        classes.append(cls)

        return classes

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#