from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import configurable
from quest.world import tmx

from dataclasses import dataclass
import json

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@dataclass
class TileVisualData(object):
    """
    """

    tile_x: int
    tile_y: int

    tile_count_x: int
    tile_count_y: int

    sheet: object

    rect: object
    flags: object

def quest_image_loader(filename: str, colorkey: object, **kwargs) -> object:
    """
    """

    filename = filename.replace('\\', '/')
    if not vfs.path_exists(p3d.Filename(filename)):
        raise IOError('Tiled image "%s" does not exist in VFS' % filename)

    image_buffer = p3d.PNMImage(filename)

    def get_tile_coord(pixel_start: int, pixel_size: int, tile_count: int, invert: bool = False) -> int:
        """
        """

        tile_coord = int(pixel_start / pixel_size)
        if invert: 
            tile_coord = abs(tile_count - (tile_coord + 1))
        
        return int(tile_coord)

    def extract_image(rect: object = None, flags: object = None) -> object:
        """
        rect is a (x, y, width, height) area where a particular tile is located
        flags is a named tuple that indicates how tile is flipped or rotated

        use the rect to specify a region of the image file loaded in the function
        that encloses this one.
        return an object to represent the tile
        what is returned here will populate TiledMap.images, be returned by
        TiledObject.Image and included in TiledTileLayer.tiles()
        """

        x, y, w, h = rect
        tile_count_x = image_buffer.get_x_size() / w
        tile_count_y = image_buffer.get_y_size() / h

        tile_x = get_tile_coord(x, w, tile_count_x)
        tile_y = get_tile_coord(y, h, tile_count_y, invert=True)

        visual_data = TileVisualData(
            tile_x, tile_y, tile_count_x, tile_count_y,
            image_buffer, rect, flags)

        return visual_data

    return extract_image

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldCreatorBase(core.QuestObject):
    """
    Base class for all world creators
    """

    def load_tmx_file(self, filename: str, *args, **kwargs) -> tmx.TiledMap:
        """
        """

        kwargs['image_loader'] = quest_image_loader
        return tmx.TiledMap(filename, *args, **kwargs)

    def _load_world_data_file(self, filename: str) -> dict:
        """
        """

        if not vfs.path_exists(self._world_file):
            raise IOError('Failed to load world id: %s. Invalid world file (%s)' % (
                self._world_id, self._world_file))

        world_data = {}
        with open(self._world_file, 'r') as f:
            world_data = json.load(f)

        return world_data

    def generate_world_file(self, world_file: str) -> None:
        """
        """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldCreator(WorldCreatorBase):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldCreatorAI(WorldCreatorBase):
    """
    """

    def __init__(self, air: object):
        WorldCreatorBase.__init__(self)

        self._air = air

        test = self.load_tmx_file('zones/devplanet/001-1-1.tmx')
        print(test)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
