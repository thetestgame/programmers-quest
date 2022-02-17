from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import configurable

from panda3d_sprite import sprite as spritesheet

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Sprite(configurable.Configurable):
    """
    """

    def __init__(self, config_path: str):
        self._animation_data = {}
        configurable.Configurable.__init__(self, config_path)
        self._sprite = None

    @property
    def root(self) -> p3d.NodePath:
        """
        """

        return self._root

    @property
    def sprite(self) -> spritesheet.Sprite2D:
        """
        """

        return self._sprite

    def load_animation_data(self, data: dict) -> None:
        """
        """

        self._animation_data = data

    def setup(self) -> None:
        """
        """

        self._sprite = spritesheet.Sprite2D(
            file_path=self.get('sprite_sheet'),
            rows=self.get('sheet_rows'),
            cols=self.get('sheet_cols'))
        
        for anim_key, frame_str in self._animation_data.items():
            frames = [int(s) for s in frame_str.split(',')]
            self._sprite.create_animation(anim_key, frames=frames)

        del self._animation_data
        self._root = self._sprite.node

    def destroy(self) -> None:
        """
        """

    def has_animation(self, key: str) -> bool:
        """
        """

        return key in self._sprite.animations

    def play_animation(self, key: str, loop: bool = False) -> None:
        """
        """

        if not self.has_animation(key):
            return

        self._sprite.play_animation(key, loop)

    def __getattr__(self, key: str) -> object:
        """
        """

        result = None
        if len(key) > 4:
            type_name = key[:3]
            state_name = key[4:].replace('_animation', '')
            if type_name == 'has':
                result = lambda: self.has_animation(state_name)
            if len(key) > 5:
                type_name = key[:4]
                state_name = key[5:]
                if type_name == 'play':
                    result = lambda loop=False: self.play_animation(state_name, loop)

        if not result:
            raise AttributeError('%s does not have attribute %s' % (
                self.__class__.__name__, key))
        
        return result

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#