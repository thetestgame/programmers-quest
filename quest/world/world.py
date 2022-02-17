"""
 * Copyright (C) Nxt Games 2021
 * All Rights Reserved
 *
 * Written by Jordan Maxwell <jordan.maxwell@nxt-games.com>, January 7th, 2021
 *
 * NXT GAMES CONFIDENTAL
 * _______________________
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Nxt Games and its suppliers,
 * if any. The intellectual and technical concepts contained
 * herein are proprietary to Nxt Games
 * and its suppliers and may be covered by U.S. and Foreign Patents,
 * patents in process, and are protected by trade secret or copyright law.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Nxt Games.
"""

from panda3d import core as p3d

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import singleton, configurable
from quest.framework import runnable
from quest.world import tmx, entity, layer
from quest.world import builder, sheet

from dataclasses import dataclass
import numpy as np
import json
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class GameWorldChunk(core.QuestObject):
    """
    """

    def __init__(self, world: object, data: dict):
        super().__init__()

        self._world = world
        self._world_data = data
        self._filename = data.pop('fileName')
        self._root = p3d.NodePath('Chunk-%s' % self._filename.replace('.tmx', ''))

        tiled_path = os.path.join(self._world.world_directory, self._filename)
        self._tiled_map = tmx.TiledMap(
            tiled_path, image_loader=sheet.load_tiled_image)
        self._builder = builder.WorldChunkBuilder(self)
        self._layers = {}

    @property
    def root(self) -> p3d.NodePath:
        """
        """

        return self._root

    def get_layer_by_name(self, layer_name: str) -> object:
        """
        """

        return self._layers.get(layer_name, None)

    def add_layer(self, layer_name: str, layer_inst: object) -> None:
        """
        """

        if layer_name in self._layers:
            self.notify.warning('Failed to register layer %s. Name already exists' % (
                layer_name))

            return None

        layer_inst.setup()
        layer_inst.root.reparent_to(self._root)
        self._layers[layer_name] = layer_inst

    def setup(self) -> None:
        """
        """

        self._builder.generate(self._tiled_map)      

        tile_width = self._tiled_map.tilewidth
        tile_height = self._tiled_map.tileheight

        chunk_x = self._world_data.get('x', 0)
        chunk_y = self._world_data.get('y', 0)

        self._root.set_pos(
            chunk_x / (tile_width + (tile_width / 2)), 
            -(chunk_y / (tile_height + (tile_height / 2))), 0) 
        self._root.set_two_sided(True)
        self._root.set_hpr(0, 180, 0)    

    def destroy(self) -> None:
        """
        """

        self._root.remove_node()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class GameWorld(configurable.Configurable, runnable.Runnable, core.QuestObject):
    """
    """

    def __init__(self, world_id: int, config_file: str):
        configurable.Configurable.__init__(self, config_file)
        runnable.Runnable.__init__(self, task_chain_name='world-culling-chain')
        core.QuestObject.__init__(self)
        self._chunks = {}

        self._world_id = world_id
        self._world_file = self.pop('world_file')
        self._world_directory = os.path.dirname(self._world_file)
        self._root = p3d.NodePath('World-%d' % world_id)
        self._root.set_scale(self.pop('world_scale', 5))

    @property
    def world_directory(self) -> str:
        """
        """

        return self._world_directory

    def setup(self) -> None:
        """
        """

        if not vfs.path_exists(self._world_file):
            raise IOError('Failed to load world id: %s. Invalid world file (%s)' % (
                self._world_id, self._world_file))

        world_data = {}
        with open(self._world_file, 'r') as f:
            world_data = json.load(f)

        world_type = world_data.get('type', None)
        assert world_type == 'world', '%s is not a valid world file' % self._world_file
        
        maps = world_data.get('maps', [])
        for chunk_data in maps:
            chunk_x = chunk_data.get('x', 0)
            chunk_y = chunk_data.get('y', 0)

            self._chunks[(chunk_x, chunk_y)] = GameWorldChunk(self, chunk_data)
            self._chunks[(chunk_x, chunk_y)].setup()
            self._chunks[(chunk_x, chunk_y)].root.reparent_to(self._root)

        self.activate()
        self._root.reparent_to(runtime.render)

    def destroy(self) -> None:
        """
        """

        self.deactivate()
        for chunk_index, chunk_inst in self._chunks.items():
            chunk_inst.destroy()
        self._chunks = {}

    async def tick(self, dt: float) -> None:
        """
        Performs the tick operation for the runnable object. 
        Shows/Hides chunks as they come into view.
        """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldManager(configurable.Configurable, singleton.Singleton, core.QuestObject):
    """
    """

    def __init__(self, config_path: str):
        self._world_data = {}
        self._active_world = None

        configurable.Configurable.__init__(self, config_path)
        core.QuestObject.__init__(self)
        runtime.world_mgr = self

        self.load_world(1)

    def load_worlds_data(self, data: dict) -> None:
        """
        Loads the [Worlds] data section from the configuration
        file into memory
        """

        self._world_data = data
    
    def load_world(self, world_id: int) -> bool:
        """
        """

        # Verify the requested world id exists
        world_file = self._world_data.get(world_id, None)
        if not world_file:
            self.notify.warning('Failed to load world (%d). World does not exist' % (world_id))
            return False

        # Destroy any active game worlds
        if self._active_world != None:
            self._active_world.destroy()
            self._active_world = None

        # Load the new game world from the VFS
        try:
            game_world = GameWorld(world_id, world_file)
            game_world.setup()
            self._active_world = game_world
        except IOError as e:
            print(str(e))
            return False

        return True

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#