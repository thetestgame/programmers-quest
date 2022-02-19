"""
Constains all the constant identifiers used to talk about Distributed Objects across the system.
"""

import enum

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

APPLICATION_VERSION = 'quest-dev' #TODO: handle properly

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkGlobalObjectIds(enum.IntEnum):
    """
    Constant network identifiers for all DOG instances within the quest module. These ids should
    match the ids present in the development and production Astron cluster configuration files.
    """

    GLOBAL_GAME_ROOT  = 4000
    DOG_LOGIN_MANAGER = 4100

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkChannels(enum.IntEnum):
    """
    Constant network channel identifiers used to talk within the Astron server cluster.
    """

    UBERDOG_DEFAULT_CHANNEL         = 300000
    AI_DEFAULT_CHANNEL              = 300001
    
    STATE_SERVER_DEFAULT_CHANNEL    = 402000
    DATABASE_SERVER_DEFAULT_CHANNEL = 403000
    DB_STATE_SERVER_DEFAULT_CHANNEL = 404000

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkZones(enum.IntEnum):
    """
    Represents constant network zone identifiers. These identifiers are indepndent of 
    the distributed object IDs
    """

    QUEST_ZONE_ID_INVALID       = 0 # Represents an invalid zone id. (NONE)
    QUEST_ZONE_ID_SHARDS        = 1 # Contains all the registered shard server instances
    QUEST_ZONE_ID_MANAGEMENT    = 2 #

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#