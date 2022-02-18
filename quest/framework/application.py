from threading import local
from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs, logging
from quest.engine import http
from quest.framework import localizer

import os
import ctypes
import easygui
import sys
from collections import defaultdict

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestApplication(core.QuestObject):
    """
    """

    showbase_cls = showbase.QuestShowBase

    def __init__(self):
        super().__init__(notify='application')

        self._development = prc.get_prc_bool('want-dev', False)
        self._headless = prc.get_prc_string('window-type', 'onscreen') == 'none'
        self.exit_code = 0
        self._base = None

        runtime.dev = self._development
        runtime.headless = self._headless
        runtime.application = self

    @property
    def base(self) -> showbase.QuestShowBase:
        """
        Represents the application's current ShowBase instance
        """

        return self._base

    def setup_framework(self) -> None:
        """
        Performs framework setup operations
        """

        # Configure our VirtualFileSystem environment
        if self._development:
            self.notify.info('Starting in development mode')
            vfs.vfs_mount_subdirectories('.', 'assets')

            self_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.abspath(os.path.join(self_path, '../configfiles'))
            vfs.vfs_mount_directory('config', config_path)
        else:
            NotImplementedError('Packaged VFS is not yet supported')

        # Load our runtime configuration files
        prc.load_prc_file('config/quest.prc')
        if self._headless:
            prc.load_prc_file('config/quest-server.prc')
        if self._development:
            prc.load_prc_file('config/quest-dev.prc')
            prc.load_prc_file('personal.prc', optional=True)

        # Configure our logging environment
        sentry_dsn = prc.get_prc_string('sentry-dsn', 'none')
        if sentry_dsn == 'none':
            sentry_dsn = None
        logging.configure_logging(sentry_dsn=sentry_dsn)

    def setup_engine(self) -> None:
        """
        Performs engine setup operations
        """

        assert self.showbase_cls != None, 'Showbase Cls is not defined'
        self._base = self.showbase_cls()
        self._base.exitFunc = self.destroy

        vfs.switch_file_functions_to_vfs()
        vfs.switch_io_functions_to_vfs()

        # Instantiate our engine singletons
        http.HttpManager.instantiate_singleton()
        localizer.ApplicationLocalizer.instantiate_singleton()

    def setup_development(self) -> None:
        """
        Performs development setup operations
        """

        self.notify.info('Initializing developer options...')

        if not self._headless:
            self._base.accept('f1', self._base.oobe)
            self._base.accept('f2', self._refresh)
            self._base.accept('f3', lambda: self._base.render.ls())

    def _refresh(self) -> None:
        """
        Refreshes the game source if in development mode
        """

        assert self._development, 'Refresh only available in developer mode'
        try:
            import limeade
        except ModuleNotFoundError:
            self.notify.warning('Failed to refresh source. Limeade not installed')
            return

        self.notify.warning('Refreshing application source')
        limeade.refresh()

    def setup_game(self) -> None:
        """
        Performs game setup operations.
        """

    def destroy(self) -> None:
        """
        Performs shutdown operations on the application
        """

    def handle_exception(self, ex: Exception) -> None:
        """
        Handles uncaught exceptions that reach the application
        root
        """

        # Log the exception internally for developers to fix
        logging.capture_exception(ex)

        # Build our user dialog message box localized 
        # strings using exception details
        error_name = ex.__class__.__name__
        error_message = str(ex)

        if runtime.has_localizer():
            title = self.localizer.get_localization('gui.uncaught_error.title')
            message = self.localizer.get_localization(
                'gui.uncaught_error.message', 
                error_name=error_name,
                error_message=error_message)
        else:
            title = 'Critical Error'
            message = '%s: %s' % (
                error_name, error_message)

        # Display our message to the user
        if os.name == 'nt':
            ctypes.windll.user32.MessageBoxW(0, message, title, 0)
        else:
            easygui.msgbox(message, title=title)

    def start(self) -> int:
        """
        Performs startup operations on the application
        instance
        """

        if self._development:
            self.notify.warning('Starting application (%s) in development mode' % (self.__class__.__name__))

        try:
            self.setup_framework()
            self.setup_engine()

            if self._development:
                self.setup_development()        
            self.setup_game()
            self._base.run()
        except Exception as e:
            self.handle_exception(e)

        return self.exit_code

    def get_command_line_arguments(self) -> dict:
        """
        Retrieves the passed command line arguments as a dictionary. The arguments must
        follow the format of --key=value to be accepted
        """

        d = defaultdict(list)
        for k, v in ((k.lstrip('-'), v) for k,v in (a.split('=') for a in sys.argv[1:])):
            d[k].append(v)

        return d

    def get_startup_variable(self, key: str, default: str) -> str:
        """
        Retrieves the startup variable passed either via command line or via
        the host environment variables
        """

        cmd_args = self.get_command_line_arguments()
        
        # Prefer environment variables first to allow for Docker input
        return_value = cmd_args.get(key, default)
        if os.environ.get(key) is not None:
            return_value = os.environ.get(key)

        return return_value

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(application_cls: object = None, development: bool = False, headless: bool = False, startup_prc: str = '') -> int:
    """
    """ 

    if development: startup_prc += 'want-dev #t\n'
    if headless: startup_prc += 'window-type none\n'
    prc.load_prc_file_data(startup_prc, 'startup-prc')
    
    application_cls = application_cls if application_cls != None else QuestApplication
    application = application_cls()
    exit_code = application.start()

    return exit_code

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#