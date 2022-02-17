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
from quest.world import entity

import numpy as np
import collections

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class TiledLayerNode(entity.Entity):
    """
    """

    def __init__(self, layer: object):
        super().__init__(
            task_chain_name='tile-layer-chain',
            collector='App:World:TileLayersUpdate')

        self._layer = layer
        self._root = p3d.NodePath(layer.name)

    @property
    def name(self) -> str:
        """
        """

        return self._layer.name

    @property
    def layer(self) -> object:
        """
        """

        return self._layer

    @property
    def root(self) -> p3d.NodePath:
        """
        """

        return self._root

    def setup(self) -> None:
        """
        """

        raise NotImplementedError('%s does not implement setup!' % self.__class__.__name__)

    def destroy(self) -> None:
        """
        """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class TiledTileLayerNode(TiledLayerNode):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._change_queue = collections.deque()
        self._vertex_format = self._make_vertex_format()
        self._vertex_data = p3d.GeomVertexData(
            self.name, self._vertex_format, p3d.Geom.UHStatic)
        self._vertex_data.set_num_rows(self.tile_count * 4)

        self._triangles = p3d.GeomTriangles(p3d.Geom.UH_static)
        self._triangles.set_index_type(p3d.Geom.NT_uint32)
        triangle_data = self._triangles.modify_vertices()
        triangle_data.set_num_rows(self.tile_count * 6)
        self._mesh = p3d.Geom(self._vertex_data)
        self._sheets = []

    @property
    def tile_count(self) -> int:
        """
        """

        return self._layer.width * self._layer.height

    def _make_vertex_format(self) -> None:
        """
        """

        vertex_format         = p3d.GeomVertexArrayFormat("vertex", 3, p3d.Geom.NT_float32, p3d.Geom.C_point)
        normal_format         = p3d.GeomVertexArrayFormat("normal", 3, p3d.Geom.NT_float32, p3d.Geom.C_normal)
        texcoord_format       = p3d.GeomVertexArrayFormat("texcoord", 2, p3d.Geom.NT_float32, p3d.Geom.C_texcoord)

        tile_position_format  = p3d.GeomVertexArrayFormat("frct_tilePosition", 2, p3d.Geom.NT_float32, p3d.Geom.C_point)
        tile_count_format     = p3d.GeomVertexArrayFormat("frct_tileCount", 2, p3d.Geom.NT_float32, p3d.Geom.C_point)
        tile_sheet_format     = p3d.GeomVertexArrayFormat("frct_tileSheet", 1, p3d.Geom.NT_float32, p3d.Geom.C_point)

        geom_vertex_format = p3d.GeomVertexFormat()
        geom_vertex_format.add_array(vertex_format)
        geom_vertex_format.add_array(normal_format)
        geom_vertex_format.add_array(texcoord_format)

        geom_vertex_format.add_array(tile_position_format)
        geom_vertex_format.add_array(tile_count_format)
        geom_vertex_format.add_array(tile_sheet_format)
        
        return_geom_vertex_format = \
            p3d.GeomVertexFormat.register_format(geom_vertex_format)
        
        return return_geom_vertex_format

    def setup(self) -> None:
        """
        """

        self.activate()
        self._change_queue.append((self._draw_initial_geometry, []))

        for x, y, tile_vis_data in self.layer.tiles():
            self._change_queue.append((
                self._handle_tile_draw, (x, y, tile_vis_data)))

    async def tick(self, dt: float) -> None:
        """
        """

        # Apply any remaining changes
        if self._change_queue:
            change_func, change_data = self._change_queue.pop()
            change_func(*change_data)

    def destroy(self) -> None:
        """
        """

        self.destroy()

    def _get_tile_index(self, index: tuple) -> int:
        """
        """

        return index[1] * self.layer.width + index[0]

    def _draw_initial_geometry(self) -> None:
        """
        """

        self._mesh.add_primitive(self._triangles)

        p3d.Thread.consider_yield()
        assert self._mesh.check_valid(), 'A meshing error occured and the geometry was invalid'
        geom_node = p3d.GeomNode(self.name)
        geom_node.add_geom(self._mesh)
        geom_node.set_attrib(
            p3d.TransparencyAttrib.make(p3d.TransparencyAttrib.MAlpha))
        node = self.root.attach_new_node(geom_node)

        sheet_collection = p3d.Texture()
        sheet_collection.setup_2d_texture_array(len(self._sheets))
        for sheet_index in range(len(self._sheets)):
            sheet = self._sheets[sheet_index]
            sheet_collection.load(sheet, z=sheet_index, n=0)

        sheet_collection.set_magfilter(p3d.Texture.FTNearest)
        sheet_collection.set_minfilter(p3d.Texture.FTNearest)
        sheet_collection.set_wrap_u(p3d.Texture.WMClamp)
        sheet_collection.set_wrap_v(p3d.Texture.WMClamp)
        node.set_texture(sheet_collection, 0)

        layer_shader = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex="shaders/tile_layer.vert.glsl", 
            fragment="shaders/tile_layer.frag.glsl")
        node.set_shader(layer_shader)

    def _handle_tile_draw(self, x: int, y: int, tile_vis_data: object) -> None:
        """
        """
        
        # Grab our memoryview handles
        vertex_view        = memoryview(self._vertex_data.modify_array(0)).cast('B').cast('f')
        normal_view        = memoryview(self._vertex_data.modify_array(1)).cast('B').cast('f')
        texcoord_view      = memoryview(self._vertex_data.modify_array(2)).cast('B').cast('f')
        tile_position_view = memoryview(self._vertex_data.modify_array(3)).cast('B').cast('f')
        tile_count_view    = memoryview(self._vertex_data.modify_array(4)).cast('B').cast('f')
        tile_sheet_view    = memoryview(self._vertex_data.modify_array(5)).cast('B').cast('f')
        triangle_view      = memoryview(self._triangles.modify_vertices()).cast('B').cast('L')
        p3d.Thread.consider_yield()

        # Calculate our vertex positions from tile position
        x1 = x + 1
        y1 = y + 1
        z1 = 0

        x2 = x
        y2 = y
        z2 = 0

        def build_normals() -> np.array:
            """
            """

            inputs = [
                [2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1],
                [2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1],
                [2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1],
                [2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1],
            ]

            normalized = []
            for vec_input in inputs:
                norm_vec = p3d.LVector3(*vec_input)
                norm_vec.normalize()

                normalized.append(norm_vec.get_x())
                normalized.append(norm_vec.get_y())
                normalized.append(norm_vec.get_z())
    
            return np.array(normalized, dtype='f4')

        # Store the tile's tile set image for later use
        # and determine our list index
        if tile_vis_data.sheet not in self._sheets:
            self._sheets.append(tile_vis_data.sheet)
            sheet_index = len(self._sheets)
        else:
            sheet_index = self._sheets.index(tile_vis_data.sheet)

        # Caculate our cursor start positions
        face_id = self._get_tile_index((x, y))
        vertex_id = face_id * 12
        texcoord_id = face_id * 8

        # Assign our geometry data
        tile_x, tile_y = tile_vis_data.tile_x, tile_vis_data.tile_y
        tile_count_x, tile_count_y, = tile_vis_data.tile_count_x, tile_vis_data.tile_count_y

        vertex_view[vertex_id:vertex_id + 12] = np.array([x1, y1, z1, x2, y1, z1, x2, y2, z2, x1, y2, z2], dtype='f4')
        normal_view[vertex_id:vertex_id + 12] = build_normals()
        texcoord_view[texcoord_id:texcoord_id + 8] = np.array([
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,  
            1.0, 1.0], dtype = "f4")
        p3d.Thread.consider_yield()

        tile_position_view[texcoord_id:texcoord_id + 8] = np.array([tile_x, tile_y, tile_x, tile_y, tile_x, tile_y, tile_x, tile_y], dtype = "f4")
        tile_count_view[texcoord_id:texcoord_id + 8] = np.array([tile_count_x, tile_count_y, tile_count_x, tile_count_y, tile_count_x, tile_count_y, tile_count_x, tile_count_y], dtype = "f4")
        tile_sheet_view[int(texcoord_id/2)] = np.array([0], dtype = "f4")
        p3d.Thread.consider_yield()

        # Assign our triangle indexes
        i1, i2 = 6 * face_id, 4 * face_id
        indexes = np.array([i2, i2 + 1, i2 + 3, i2 + 1, i2 + 2, i2 + 3], dtype = "u4")
        triangle_view[i1: i1 + 6] = indexes
        p3d.Thread.consider_yield()

        del vertex_view
        del normal_view
        del texcoord_view

        del tile_position_view
        del tile_count_view
        del tile_sheet_view

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
