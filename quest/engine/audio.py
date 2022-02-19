from quest.engine import runtime
from quest.engine.core import QuestObject
from quest.engine.vfs import path_exists
from quest.framework.singleton import Singleton

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class SoundSource(QuestObject):
    """
    Represents a sound source in the quest module
    """

    BAD = 0
    READY = 1
    PLAYING = 2

    def __init__(self):
        QuestObject.__init__(self)
        self._sound_manager = SoundManager.get_singleton()

    @property
    def source_id(self) -> object:
        """
        Returns this sound source's source id
        """

        return id(self)

    def get_sound(self, name: str) -> object:
        """
        Retrieves a sound from the sound manager by name
        """

        return self._sound_manager.get_sound(self.source_id, name)

    def sound_exists(self, name: str) -> bool:
        """
        Returns true if the sound name exists in the 
        current sound manager singleton instance
        """

        return self.get_sound(name) != None

    def __has_default_volume(self) -> bool:
        """
        Returns true if the sound source
        has a default volume
        """

        return hasattr(self, 'default_volume')

    def __get_default_volume(self, name: str, default: object = None) -> float:
        """
        Retrieves the sources default volume for a given sound name. Otherwise NoneType
        """

        if not self.__has_default_volume():
            return None

        return self.default_volume.get(name, default)

    def __attempt_set_sound_volume(self, name: str, volume: float) -> None:
        """
        Attempts to set a sonds volume if it exists
        """

        if volume is None:
            return

        sound_obj = self.get_sound(name)
        if sound_obj:
            sound_obj.set_volume(volume)

    def play_sound(self, name: str) -> None:
        """
        Plays a sound from the current sound source
        """

        volume = self.__get_default_volume(name)
        self.__attempt_set_sound_volume(name, volume)
        self._sound_manager.play(self.source_id, name)

    def stop_sound(self, name: str) -> None:
        """
        Stops the requested sound name
        """

        self._sound_manager.stop(self.source_id, name)

    def pause_sound(self, name: str) -> None:
        """
        Pauses the requested sound name
        """

        self._sound_manager.pause(self.source_id, name)

    def resume_sound(self, name: str) -> None:
        """
        Resumes the requested sound name
        """

        self._sound_manager.resume(self.source_id, name)

    def set_sound_loop(self, name: str, flag: bool) -> None:
        """
        Sets the loop flag of the requested sound name
        """

        self._sound_manager.set_loop(self.source_id, name, flag)

    def set_sound_loop_count(self, name: str, count: int) -> None:
        """
        Sets the loop count of the requested sound name
        """

        self._sound_manager.set_loop_count(self.source_id, name, count)

    def get_sound_status(self, name: str) -> int:
        """
        Returns the sound status of the requested sound name and sound source
        """

        self._sound_manager.status(self.source_id, name)

    def is_sound_playing(self, name: str) -> bool:
        """
        Returns the sound playing status of the requested sound name from this sound source
        """

        self.get_sound_status(name) == SoundSource.PLAYING

    def is_sound_ready(self, name: str) -> bool:
        """
        Returns the sound ready status of the requested sound name from this sound source
        """

        self.get_sound_status(name) == SoundSource.READY

    def is_sound_bad(self, name: str) -> bool:
        """
        Returns the sound bad status of the requested sound name from this sound source
        """

        self.get_sound_status(name) == SoundSource.BAD

    def add_sound(self, name: str, filename: str) -> None:
        """
        Registers a new sound with the sound manager for this
        sound source
        """

        self._sound_manager.register(self.source_id, name, filename)

    def add_music(self, name: str, filename: str) -> None:
        """
        Registers a new music with the sound manager for this
        sound source
        """

        self._sound_manager.register_music(self.source_id, name, filename)

    def remove_sound(self, name: str) -> None:
        """
        Removes the requested sound name from the sound source
        """

        self._sound_manager.unregister(self.source_id, name)

    def remove_all_sounds(self) -> None:
        """
        Removes all sounds from the sound source
        """

        self._sound_manager.unregister(self.source_id)

    def copy_sounds(self, new_source: object) -> None:
        """
        Copys all registered sound sources from this sound source to a new source instance
        """

        assert isinstance(new_source, SoundSource)
        self._sound_manager.copy_sounds(self.source_id, new_source.source_id)

        if self.__has_default_volume():
            if not hasattr(new_source, 'default_volume'):
                new_source.default_volume = {}
            new_source.default_volume.update(self.default_volume)

    def load_sound_data(self, data: dict) -> None:
        """
        Loads sound data from configurable variants
        """

        self.default_volume = {}
        for name, param in list(data.items()):
            if type(param) == type(''):
                self.add_sound(name, param)
            elif type(param) == tuple:
                self.add_sound(name, param[0])

                sound_obj = self.get_sound(param[0])
                self.default_volume[name] = param[1]

                if sound_obj:
                    sound_obj.set_volume(param[1])
                    if len(param) > 1:
                        sound_obj.set_loop(param[2])
            else:
                self.notify.error('%s.load_sound_data: Unknown param type: %s' % (
                    self.__class__.__name__, param))

    def load_music_data(self, data: dict) -> None:
        """
        Loads music data from configurable variants
        """

        self.default_volume = {}
        for name, param in list(data.items()):
            if type(param) == type(''):
                self.add_music(name, param)
            elif type(param) == tuple:
                self.add_music(name, param[0])

                sound_obj = self.get_sound(param[0])
                self.default_volume[name] = param[1]

                if sound_obj:
                    sound_obj.set_volume(param[1])
                    if len(param) > 1:
                        sound_obj.set_loop(param[2])
            else:
                self.notify.error('%s.load_music_data: Unknown param type: %s' % (
                    self.__class__.__name__, param))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class SoundManager(Singleton, QuestObject):
    """
    Manages all sound sources in the quest module
    """

    def __init__(self):
        Singleton.__init__(self)
        QuestObject.__init__(self)

        self._sound_off = False
        self._sound_sources = {}

    @property
    def sound_off(self):
        """
        Returns the managers currently "off" state as a 
        property
        """

        return self.is_sound_off()

    @sound_off.setter
    def sound_off(self, state):
        """
        Sets the managers current off state
        as a setter
        """

        self.set_sound_off(state)

    def destroy(self):
        """
        Destroys the sound manager singleton instance
        """

        for source_id in self._sound_sources:
            self.unregister(source_id)

        self._sound_sources = {}
        QuestObject.destroy(self)

    def __destroy_sound(self, sounds: list, name: str) -> None:
        """
        Destroys a sound name instance from a sounds list.
        """

        if name in sounds:
            del sounds[name]

    def __load_sfx_file(self, path: str) -> object:
        """
        Loads the requested sfx file path from the Panda3d
        Virtual File System
        """

        return runtime.loader.load_sfx(path)

    def __load_music_file(self, path: str) -> object:
        """
        Loads the requested music file path from the Panda3d
        Virtual File System
        """

        return runtime.loader.load_music(path)

    def is_sound_off(self):
        """
        Returns the managers currently "off" state as
        a method.
        """

        return self._sound_off

    def set_sound_off(self, sound_off):
        """
        Sets the managers current sound off state
        """
    
        self._sound_off = sound_off

        # If the state is sound off stop all sound sources
        if sound_off:
            for sounds in list(self._sound_sources.values()):
                for sound_obj, sound_pos in list(sounds.values()):
                    sound_obj.stop()

    def pause_all(self):
        """
        Pauses all sound sources
        """

        for source_id in self._sound_sources:
            sounds = self._sound_sources[source_id]

            for name in sounds:
                self.pause(source_id, name)

    def resume_all(self):
        """
        Resumes all sound sources
        """

        for source_id in self._sound_sources:
            sounds = self._sound_sources[source_id]

            for name in sounds:
                self.resume(source_id, name)

    def register(self, source_id: object, name: str, filename: str) -> None:
        """
        Registers the sound with its respective source and loads it into 
        memory
        """

        # Verify the sound file exists
        if not path_exists(filename):
            self.notify.error('%s.load: Failed to load sound file %s. Does not exist' % (self.__class__.__name__, filename))
            return

        if source_id not in self._sound_sources:
            self._sound_sources[source_id] = {}

        sounds = self._sound_sources[source_id]
        self.__destroy_sound(sounds, name)
        sounds[name] = (self.__load_sfx_file(filename), -1)

    def unregister(self, source_id: object, name: str = None) -> None:
        """
        """

        # Verify the sound source exists
        if not self.has_sound_source(source_id):
            return

        if name is None:
            sounds = self.get_sound_source(source_id)
            for name in list(sounds.items()):
                sounds[name] = None

            del self._sound_sources[source_id]
        else:
            self.__destroy_sound(self._sound_sources[source_id], name)

    def register_music(self, source_id: object, name: str, filename: str) -> None:
        """
        """

        # Verify the sound file exists
        if not path_exists(filename):
            self.notify.error('%s.load: Failed to load sound file %s. Does not exist' % (self.__class__.__name__, filename))
            return

        if source_id not in self._sound_sources:
            self._sound_sources[source_id] = {}

        sounds = self._sound_sources[source_id]
        self.__destroy_sound(sounds, name)
        sounds[name] = (self.__load_music_file(filename), -1)

    def set_music_volume(self, volume: float) -> None:
        """
        Sets the music playback volume
        """

        runtime.base.musicManager.set_volume(volume)

    def set_sound_effects_volume(self, volume: float) -> None:
        """
        Sets the sound effects playback volume
        """

        base = runtime.base
        for i in range(len(base.sfxManagerList)):
            if base.sfxManagerIsValidList[i]:
                base.sfxManagerList[i].setVolume(volume)

    def enable_music(self, state: bool) -> None:
        """
        Sets the music playback enabled state
        """

        runtime.base.enable_music(state)

    def enable_sound_effects(self, state: bool) -> None:
        """
        Sets the sound effects playback enabled state
        """

        runtime.base.enable_sound_effects(state)

    def pause(self, source_id: object, name: str) -> None:
        """
        Pauses the sound from the requested sound source
        """

        if not self.has_sound_source(source_id):
            return

        sounds = self.get_sound_source(source_id)
        if name not in sounds:
            return

        sound_obj, sound_pos = sounds[name]
        if sound_obj.status() == 2:
            sounds[name] = (sound_obj, sound_obj.get_time())
            sound_obj.stop()

    def resume(self, source_id: object, name: str) -> None:
        """
        Resumes the sound from the requested sound source
        """

        if not self.has_sound_source(source_id):
            return

        sounds = self.get_sound_source(source_id)
        if name not in sounds:
            return

        sound_obj, sound_pos = sounds[name]
        if sound_pos != -1:
            sound_obj.set_time(sound_pos)
            sounds[name] = (sound_obj, -1)

    def has_sound_source(self, source_id: object) -> bool:
        """
        Returns true if the given sound source id exists
        """

        return source_id in self._sound_sources

    def get_sound_source(self, source_id: object) -> object:
        """
        Returns the sound source by id if it exists. Otherwise NoneType
        """

        if not self.has_sound_source(source_id):
            return None

        return self._sound_sources[source_id]

    def get_sound(self, source_id: object, name: str) -> object:
        """
        Attempts to retrieve a sound name for a given sound source by
        its identifier
        """

        if not self.has_sound_source(source_id):
            return None

        sounds = self.get_sound_source(source_id)
        if name in sounds:
            sound_obj, sound_pos = sounds[name]
            return sound_obj
        
        return None

    def copy_sounds(self, source_id: object, new_id: object) -> None:
        """
        Copys the sounds from one sound source id to another.
        """

        if not self.has_sound_source(source_id):
            return

        sounds = self.get_sound_source(source_id)
        if not self.has_sound_source(new_id):
            self._sound_sources[new_id] = {}

        self._sound_sources[new_id].update(sounds)

    def __getattr__(self, name) -> object:
        """
        Custom attribute getter for delegating missing function calls
        to the Panda3D sound object for the respective sound name and source
        """

        return lambda *args: self.__delegate_to_audio_object(name, *args)

    def __delegate_to_audio_object(self, func_name: str, source_id: object, name: str, *args) -> object:
        """
        Delegates the function call from the custom __getattr__ handler to the Panda3D native sound
        object.
        """

        if not self.has_sound_source(source_id):
            self.notify.warning('Failed to delegate audio. Sound source does not exist')
            return

        if self._sound_off:
            self.notify.debug('Delgation ignored. Sound is currently off')
            return

        if len(self._sound_sources) == 0:
            self.notify.warning('Failed to delegate audio. No sound sources defined')
            return

        sounds = self.get_sound_source(source_id)
        if name in sounds:
            sound_obj, sound_pos = sounds[name]
            func = getattr(sound_obj, func_name)
            return func(*args)

        raise AttributeError('Count not find attribute "%s" for sound "%s" from source %s.' % (
            func_name, name, source_id))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#