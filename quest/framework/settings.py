from quest.engine import core, prc
from quest.engine import runtime, vfs
from quest.framework import configurable
from quest.framework import singleton

import copy
import sys
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class LocalSettings(dict, configurable.Configurable):
    """
    Represents a local application configuration file
    """

    HEADER_COMMENTS = []

    def __init__(self, config_path: str):
        dict.__init__(self)
        self.path = config_path

        self._child_dicts = {}
        self._first_time = True
        self._dirty = False

        if os.path.exists(config_path):
            self._first_time = False

        configurable.Configurable.__init__(self, config_path)
        self.update(self.configuration)
        del self.configuration

    def is_first_time(self) -> bool:
        """
        Returns true if the local settings is a newly created
        file
        """

        return self._first_time

    def is_dirty(self) -> bool:
        """
        Returns true if the application settings are currently dirty
        """

        return self.__dirty

    def write(self) -> None:
        """
        Writes the application settings to file
        """

        f = open(self.path, 'w')
        if len(self.HEADER_COMMENTS):
            for line in self.HEADER_COMMENTS:
                f.write(line)
            f.write('\n')

        f.write('[Configuration]\n')
        for key, value in list(self.items()):
            if type(value) == bool:
                f.write('%s=%s\n' % (str(key), str(value).lower()))
            else:
                f.write('%s=%s\n' % (str(key), str(value)))

        for key, value in self._child_dicts.items():
            f.write('\n[%s]\n' % str(key))
            if type(value) == dict:
                for sub_key, sub_value in value.items():
                    if type(sub_value) == type(''):
                        f.write("%s='%s'\n" % (str(sub_key), str(sub_value.encode('utf8'))))
                    elif type(sub_value) == str:
                        f.write("%s='%s'\n" % (str(sub_key), str(sub_value)))
                    elif type(sub_value) == bool:
                        f.write("%s='%s'\n" % (str(sub_key), str(sub_value).lower()))
                    else:
                        f.write('%s=%s\n' % (str(sub_key), str(sub_value)))

        f.close()     
        self._dirty = False     

    def load_data(self, section: str, data: dict) -> None:
        """
        Loads the data from the local application settings file
        """

        if data is None:
            data = {}

        self._child_dicts[section] = data

    def reset(self) -> None:
        """
        Resets the local settings
        """

        if os.path.exists(self.path):
            os.remove(self.path)

        if os.path.exists(self.path):
            os.remove(self.path)

        self._first_time = True
        self.clear()

    def set_value_in_child_dict(self, child_dict_name: object, key: str, value: object) -> None:
        """
        """

        temp_dict = self._child_dicts.get(child_dict_name, {})
        temp_dict[key] = value
        self._child_dicts[child_dict_name] = temp_dict

    def get_value_in_child_dict(self, child_dict_name: object, key: str, value: object, default: object = None) -> None:
        """
        """

        return self._child_dicts.get(child_dict_name, {}).get(key, default)

    def get_child_dicts_copy(self) -> object:
        """
        """

        return copy.deepcopy(self.__child_dicts)

    def replace_child_dict(self, new_dict: dict) -> None:
        """
        """

        self._child_dicts = dict(new_dict)

    def on_setting_changed(self, key: str, new_value: object, old_value: object) -> None:
        """
        Called on setting changed
        """

        self._dirty = True

    def __setitem__(self, key: str, item: object) -> None:
        """
        Custom item setter for calling on_setting_changed
        """

        old_value = dict.get(self, key, None)
        dict.__setitem__(self, key, item)
        self.on_setting_changed(key, item, old_value)    

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ApplicationSettings(configurable.Configurable, singleton.Singleton, core.QuestObject):
    """
    Base class for all application settings inside the quest module
    """

    def __init__(self, config_path: str, local_settings: LocalSettings):
        vfs.switch_io_functions_to_vfs()
        configurable.Configurable.__init__(self, config_path)
        vfs.switch_io_functions_to_os()
        core.QuestObject.__init__(self)

        self.local_settings = local_settings
        self.config_prc_settings = None

    def set_options_before_engine_start(self) -> None:
        """
        Performs application settings changes prior to Showbase
        initialization
        """

        self.config_prc_settings = self.get_settings_from_prc(self.PRC_VARIABLES)
        self._set_platform_specific_options()

    def set_options_after_engine_start(self) -> None:
        """
        Sets the application's options post Panda3D setup
        """

    def _set_platform_specific_options(self) -> None:
        """
        Sets the platform specific options for the application
        """

        platform_name = sys.platform
        setter_name = 'set_%s_options' % platform_name
        if hasattr(self, setter_name):
            self.notify.info('Setting platform options for: %s' % platform_name)
            getattr(self, setter_name)()
        else:
            self.notify.warning('No platform options setter found for: %s' % platform_name)

    def set_engine_setting(self, key: str, value: object) -> None:
        """
        Sets the Panda3D engine prc configuration value
        """

        if runtime.has_base():
            self.notify.warning('Attempting to set engine setting "%s" after ShowBase startup. Setting may not take effect' % (
                key))
        
        final = ''
        if isinstance(value, bool):
            final = '#t' if value else '#f'
        elif isinstance(value, tuple) or isinstance(value, list):
            parts = []
            for v in value:
                parts.append(str(v))
            final = ' '.join(parts)
        else:
            final = value
        
        self.notify.debug('Setting engine setting "%s" to "%s"' % (key, final))
        prc.load_prc_file_data('%s %s' % (key, final), label='application-setting')

    def _validate_value(self, val: object, options: list) -> bool:
        """
        Validates the value and returns true if the value is 
        contained in the options list
        """

        return val in options

    def _validate_type(self, val: str, val_type: object) -> bool:
        """
        Validates the value's type and returns true if it matches the
        type provided in val_type
        """

        return type(val) == val_type

    def _validate_between_zero_and_one(self, val: int) -> bool:
        """
        Returns true if the valie is between 0 and 1
        """

        return val >= 0 and val <= 1

    def _valdiate_true_or_false(self, val: bool) -> bool:
        """
        Returns true if the value is a valid boolean
        """

        return type(val) is bool

    def _validate_string(self, val: str) -> bool:
        """
        Returns true if the value is a valid string type
        """

        return self._validate_type(val, str)

    def get_setting(self, setting_name: str, default_fallback: object = None, valdiation_callback: object = None) -> object:
        """
        Retrieves an application setting value and runs it against a validation
        callback if present.
        """

        if setting_name in self.local_settings:
            val = self.local_settings.get(setting_name)
            is_ok = True

            if valdiation_callback is not None:
                is_ok = valdiation_callback(val)

            if is_ok:
                return val
            else:
                self.notify.warning('Invalid value %s for option %s found in application settings' % (
                    val, setting_name))

        if setting_name in self.configuration:
            ret = self.configuration.get(setting_name)
            self.local_settings[setting_name] = ret

            return ret

        if default_fallback is not None:
            self.notify.info('Setting default setting for "%s": %s' % (setting_name, default_fallback))
            self.local_settings[setting_name] = default_fallback

        self.notify.warning('No default setting for "%s". Defaulting to %s' % (
            setting_name, default_fallback))
        
        return default_fallback

    def get_settings_from_prc(self, setting_name_list: list) -> dict:
        """
        Retrieves the required settings from the Panda3D runtime config
        """

        values = {}
        for setting_name in setting_name_list:
            result = prc.get_prc_value(setting_name, None)
            if result:
                values[setting_name] = result
            else:
                self.notify.warning('Failed to retrieve prc value for "%s"' % setting_name)

        return values

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#