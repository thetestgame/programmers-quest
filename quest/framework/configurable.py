from panda3d import core as p3d

from quest.engine import performance, logging
from quest.engine import core, vfs
from quest.framework import utilities

import configparser
import copy

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

_config_notify = logging.get_notify_category('configurable')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def _boolify(s: str) -> bool:
    """
    """

    s = s.lower()
    if s == 'true': return True
    if s == 'false': return False
    raise ValueError('Invalid Boolean')

def _nullify(s: str) -> object:
    """
    """

    s = s.lower()
    if s == 'none': return None
    raise ValueError('Invalid NoneType')

def _cast_to_type(var: object) -> object:
    """
    """

    var = str(var)
    caster_types = [_boolify, _nullify, int, float]

    for caster in caster_types:
        try: 
            return caster(var)
        except ValueError:
            pass

    return var

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Configurable(object):
    """
    """

    __include_str = '__include__'

    def __init__(self, filename: str, section: str = 'Configuration', auto_configure: bool = False):
        self._config = None
        self._included_config = None

        self._filename = filename
        self._section = section

        self.configuration = {}
        if self._filename != None:
            self.load(self._filename, self._section)

    @property
    def config(self) -> object:
        """
        Returns this configurables working config value
        """

        self._config

    def _prepare_data(self, data: dict) -> dict:
        """
        Prepares the incoming data
        by casting it to its respective type
        """

        new_data = {}
        for key, value in data:
            key = _cast_to_type(key)
            new_data[key] = _cast_to_type(value)

        return new_data

    def load(self, opath: str = None, osection: str = None) -> None:
        """
        """

        # Read the data from the cache and begin processing
        path = opath if opath else self._filename
    
        self._config = configparser.RawConfigParser()
        self._config.read(path)

        processed_sections = []
        main_section = osection or self._section
        if self._config.has_section(main_section):
            data = self._config.items(main_section)

            # Process include path if present
            include_path = dict(data).get(Configurable.__include_str)
            if include_path:
                included_configurable = Configurable(path=include_path)
                self._included_config = included_configurable.config
                self.configuration = copy.copy(included_configurable.configuration)
                processed_sections.append(main_section)
        
            # Populate section data in configuration dict
            for key, value in data:
                if key != Configurable.__include_str:
                    key = _cast_to_type(key)
                    self.configuration[key] = _cast_to_type(value)

        # Load all sections in our configuration object
        for section in self._config.sections():
            if section != main_section:
                data = self._config.items(section)
                if self._included_config and self._included_config.has_section(section):
                    included_data = self._included_config.items(section)
                    included_data.extend(data)
                    data = included_data

                    self.__config.remove_section(section)
                    self.__copy_section(section, data)
                    processed_sections.append(section)
                
                self._load_section(section, data)       

        # Process any included configurations
        if self._included_config:
            for section in self._included_config.sections():
                if section not in processed_sections:
                    data = self._included_config.items(section)
                    self._load_section(section, data)
                    self._copy_section(section, data)

        self._included_config = None

    def _copy_section(self, section: str, data: object) -> None:
        """
        Copys a section of data to the current configuration
        object instance
        """

        temp = dict(data)
        self._config.add_section(section)

        # Population section with data
        for key, value in temp.items():
            self._config.set(section, key, value)


    def _get_loader_name(self, section: str) -> str:
        """
        Returns the loader name for the
        requested config section
        """

        snake_case = utilities.get_snake_case(section)
        return 'load_%s_data' % snake_case

    def _load_section(self, section: str, data: object) -> None:
        """
        Loads the requested section into the
        configurable object
        """

        # Retrieve the loader function if present
        loader_name = self._get_loader_name(section)

        # Process the section's data
        if hasattr(self, loader_name):
            loader = getattr(self, loader_name)
            loader(self._prepare_data(data))
        else:
            self.load_data(section, self._prepare_data(data))

    def load_data(self, section: str, data: dict) -> None:
        """
        Processes the incoming data from a config section. 
        Intended to be overridden by child objects
        """

        _config_notify.warning('%s does not implement general section loader "load_data"' % (
            self.__class__.__name__))

    def _get_setter_name(self, key: str) -> str:
        """
        Returns the attributes setter name
        from its configuration key
        """

        setter_name = 'set_%s' % utilities.get_snake_case(key)
        return setter_name

    def initialize(self) -> None:
        """
        Performs inintialization operations
        on the configurable object
        """

        if not isinstance(self.configuration, dict):
            _config_notify.warning('Failed to initialize %s. Configuration is not a valid type (%s) expected dict' % (
                self.__class__.__name__, self.configuration.__class__.__name__))
            
            return

        for key, value in list(self.configuration.items()):
            setter_name = self._get_setter_name(key)
            setter = getattr(self, setter_name, None)

            if setter:
                _config_notify.debug('(Setter) %s: %s' % (setter_name, str(value)))
                if isinstance(value, tuple):
                    setter(*value)
                else:
                    setter(value)
            elif self.auto_configure:
                setattr(self, key, value)
            else:
                _config_notify.warning('%s does not implement setter: %s' % (
                    self.__class__.__name__, setter_name))

        self.configuration = {}
        self._config = None
        self._included_config = None
    
    def load_data(self, section: str, data: object) -> None:
        """
        Processes the incoming data from a config section. 
        Intended to be overridden by child objects
        """

    def pop(self, attr: str, default: object = None) -> object:
        """
        Pops the requested attribute from the 
        configuration dictionary
        """

        return self.configuration.pop(attr, default)

    def pop_as(self, attr: str, cls: object, default: object = None) -> object:
        """
        Pops the requested attribute from the 
        configuration dictionary and passes it as the first argument
        into the provided cls object
        """

        assert cls != None

        variable = self.pop(attr, default)
        assert variable != None

        return cls(variable)

    def pop_call(self, attr: str, func: object, default: object = None, **kwargs) -> object:
        """
        Pops the requested attribute from the configuration dictionary
        and passes it into the function callback returning the result
        """

        assert func != None
        assert callable(func)

        variable = self.pop(attr, default)
        assert variable != None

        return func(variable, **kwargs)

    def get(self, attr: str, default: object = None) -> object:
        """
        Retrieves the requested attribute from
        the configuration dictionary
        """

        return self.configuration.get(attr, default)

    def get_as(self, attr: str, cls: object, default: object = None) -> None:
        """
        Retrieves the requested attribute from the configuration
        dictionary and passes it as the first argument in the cls 
        object
        """

        assert cls != None

        variable = self.get(attr, default)
        assert variable != None

        return cls(variable)

    def get_call(self, attr: str, func: object, default: object = None, **kwargs) -> None:
        """
        Retrieves the requested attribute from the configuration
        dictionary and passes it as the first argument into the function 
        returning the results
        """

        assert func != None
        assert callable(func)

        variable = self.get(attr, default)
        assert variable != None

        return func(variable)

    def reload(self) -> None:
        """
        Reloads the configuration object
        """

        self.load()
        self.initialize()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
