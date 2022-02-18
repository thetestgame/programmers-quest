from quest.engine import runtime, core, prc
from quest.framework import singleton, configurable
from playfab import PlayFabSettings

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class PlayFabManager(singleton.Singleton, configurable.Configurable, core.QuestObject):
    """
    Singleton manager for initializing and interacting with our PlayFab environment
    """

    def __init__(self, config_path: str):
        configurable.Configurable.__init__(self, config_path)
        core.QuestObject.__init__(self)
        runtime.playfab_mgr = self

        PlayFabSettings.ProductionEnvironmentURL = self.pop('production_environment_url')
        PlayFabSettings.TitleId = self.pop('title_id')

        personal_secret_key = prc.get_prc_string('playfab-secret-key')
        PlayFabSettings.DeveloperSecretKey = runtime.application.get_startup_variable('PLAYFAB_SECRET_KEY', personal_secret_key)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
