from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs, sprite
from quest.framework import configurable, utilities
from quest.world import entity

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NPCCharacter(configurable.Configurable, entity.Entity):
    """
    """

    def __init__(self, config_path: str):
        self._character_stats = {}
        self._states = {}
        self._state_animation = {}

        configurable.Configurable.__init__(self, config_path)
        entity.Entity.__init__(self)

        self._root = p3d.NodePath(self.__class__.__name__)
        self._root.set_hpr(0, -90, 0)
        self._root.set_pos(10, -50, 1)

        self._sprite = None
        self._weapon = None

        self._looking_left = False
        self._active_state = None
        self._default_state = self.get('default_state')

    @property
    def root(self) -> p3d.NodePath:
        """
        """

        return self._root

    @property
    def look_left(self) -> bool:
        """
        """

        return self._looking_left

    @look_left.setter
    def look_left(self, flag: bool) -> None:
        """
        """

        if flag == self._looking_left:
            return

        self._looking_left = flag
        if self._sprite != None:
            self._sprite.sprite.flip_x(flag)
        
        if self._weapon != None:
            self._weapon.sprite.flip_x(flag)

    ##############################################
    ##### Character active weapon management #####
    ##############################################

    def set_weapon(self, weapon: object) -> None:
        """
        """

    def has_weapon(self) -> bool:
        """
        """

        return self._weapon != None

    def get_weapon(self) -> object:
        """
        """

        return self._weapon

    ##############################################
    ##### Character active sprite management #####
    ##############################################

    def set_sprite(self, config_file: str) -> None:
        """
        """
        
        self.remove_sprite()
        self._sprite = sprite.Sprite(config_file)
        self._sprite.setup()
        self._sprite.root.reparent_to(self._root)
        self.request_state(self._default_state)

    def get_sprite(self) -> sprite.Sprite:
        """
        """

        return self._sprite

    def has_sprite(self) -> bool:
        """
        """

        return self._sprite != None

    def remove_sprite(self) -> None:
        """
        """

        if self._sprite is None:
            return

        self._sprite.destroy()
        self._sprite = None

    ##############################################
    ######## Character setup/destruction #########
    ##############################################

    def setup(self) -> None:
        """
        """

    def destroy(self) -> None:
        """
        """

    ##############################################
    ###### Character stats/Buffs management ######
    ##############################################

    def load_stats_data(self, data: dict) -> None:
        """
        """

        self._character_stats = data

    def get_stat(self, section: str, key: str, default: object) -> object:
        """
        """

        stat_path = '%s.%s' % (section, key)
        return self._character_stats.get(stat_path, default)

    ##############################################
    ######### Character states management ########
    ##############################################

    def load_character_state_data(self, data: dict) -> None:
        """
        """

        self._states = data

    def load_state_animation_data(self, data: dict) -> None:
        """
        """

        self._state_animation = data

    def request_state(self, state_name: str, *args, **kwargs) -> None:
        """
        """

        if state_name == self._active_state:
            return

        if self._active_state != None:
            exit_handler = self._get_state_handler_name('exit', state_name)
            if hasattr(self, exit_handler):
                getattr(self, exit_handler)(*args, **kwargs)

        self._active_state = state_name
        enter_handler = self._get_state_handler_name('enter', state_name)
        if hasattr(self, enter_handler):
            getattr(self, enter_handler)(*args, **kwargs)

        if self._sprite != None:
            state_animation = self._state_animation.get(state_name, None)
            if self._sprite.has_animation(state_animation) and state_animation != None:
                self._sprite.play_animation(state_animation, loop=True)            

    def _get_state_handler_name(self, type: str, state: str) -> str:
        """
        """

        snake_name = utilities.get_snake_case(state)
        return '%s_%s' % (snake_name, type)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
