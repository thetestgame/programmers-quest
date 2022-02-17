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

from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import registry, utilities
from quest.world import layer as layers

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class WorldChunkBuilder(core.QuestObject):
    """
    """

    def __init__(self, chunk: object):
        super().__init__()

        self._chunk = chunk

    def generate(self, tiled_map: object) -> None:
        """
        """

        #
        for layer in tiled_map.visible_layers:
            self.generate_layer(layer)

    def generate_layer(self, layer: object) -> None:
        """
        """

        layer_types = {
            'TiledTileLayer': layers.TiledTileLayerNode
        }

        if layer.__class__.__name__ not in layer_types:
            self.notify.warning('Failed to load layer <%s:%s>. Handler does not exist' % (
                layer.name, layer.__class__.__name__))

            return

        layer_cls = layer_types.get(layer.__class__.__name__, None)
        layer_inst = layer_cls(layer)
        self._chunk.add_layer(layer.name, layer_inst)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
