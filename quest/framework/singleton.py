from quest.engine import logging

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

_notify = logging.get_notify_category('singleton')

class Singleton(object):
    """
    """

    _singleton_instance = None

    def __init__(self):
        if not self.__class__.is_instantiated():
            self.__class__.reset_singleton(self)
        else:
            raise RuntimeError('%s singleton already exists!' % self.__class__.__name__)

    @classmethod
    def instantiate_singleton(cls, *args, **kwargs):
        """
        Instantiates a new singleton instance
        """

        if not cls.is_instantiated():
            cls.reset_singleton(cls(*args, **kwargs))

        return cls.get_singleton()

    @classmethod
    def reset_singleton(cls, inst: object = None) -> None:
        """
        Resets the singleton instance
        """

        # Destroy existing singleton if one exists
        if cls._singleton_instance is not None and id(inst) != id(cls._singleton_instance):
            if hasattr(cls, 'destroy'):
                cls.destroy(cls._singleton_instance)

        # Setup new singleton
        cls._singleton_instance = inst

    @classmethod
    def get_singleton(cls, silent: bool = False) -> object:
        """
        Returns the current singleton instance
        """

        instance = cls._singleton_instance
        if not instance and not silent:
            _notify.warning('Failed to get singleton. %s is not instantiated' % (
                cls.__name__))

        return instance

    @classmethod
    def is_instantiated(cls) -> bool:
        """
        Returns true if the current singleton has an instance
        """

        return cls._singleton_instance != None

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#