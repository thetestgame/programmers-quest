from numpy import single
from quest.engine import audio
from quest.framework import singleton, configurable

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ClientMusicManager(singleton.Singleton, audio.SoundSource, configurable.Configurable):
    """
    """

    def __init__(self, config_file: str):
        singleton.Singleton.__init__(self)
        audio.SoundSource.__init__(self)
        configurable.Configurable.__init__(self, config_file)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#