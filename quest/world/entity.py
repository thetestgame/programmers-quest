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
from quest.framework import runnable

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Entity(runnable.Runnable, core.QuestObject):
    """
    """

    def __init__(self, *args, **kwargs):
        if 'collector' not in kwargs:
            kwargs['collector'] = 'App:Entity:Update'
        
        runnable.Runnable.__init__(self, *args, **kwargs)
        core.QuestObject.__init__(self)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class EntityCollection(core.QuestObject):
    """
    """

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#