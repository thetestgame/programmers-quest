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

    DOG_LOGIN_MANAGER = 1000

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkChannels(enum.IntEnum):
    """
    Constant network channel identifiers used to talk within the Astron server cluster.
    """

    UBERDOG_DEFAULT_CHANNEL         = 300000
    AI_DEFAULT_CHANNEL              = 300001
    STATE_SERVER_DEFAULT_CHANNEL    = 402000

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class NetworkZones(enum.IntEnum):
    """
    Represents constant network zone identifiers. These identifiers are indepndent of 
    the distributed object IDs
    """

    QUEST_ZONE_ID_INVALID   = 0 # Represents an invalid zone id. (NONE)
    QUEST_ZONE_ID_SHARDS    = 1 # Contains all the registered shard server instances

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#