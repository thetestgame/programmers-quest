"""
This file contains the setuptools commands and code used for Programmer's Quest
distribution and development utilizing custom and Panda3d specific tools
"""

#----------------------------------------------------------------------------------------------------------------------------------#
####################################################################################################################################
#----------------------------------------------------------------------------------------------------------------------------------#

import os
import sys
from setuptools import setup
from tools import command, commands
from tools import utils

#----------------------------------------------------------------------------------------------------------------------------------#
################################################ Setup tools configuration variables ###############################################
#----------------------------------------------------------------------------------------------------------------------------------#

APP_NAME = "Programmer's Quest"
PACKAGES = ['quest']
SOURCE_ROOT = '.'

# Modules to exclude from builds
EXCLUDE_MODULES = [
    'limeade'
]

# Panda3D plugins to include in builds
PLUGINS = [
    'pandagl',
    'p3openal_audio',
]

# Executable icons used by the client application
CLIENT_ICONS = [

]

#
RENAME_PATHS = {

}

#
INCLUDE_PATTERNS = [

]

#----------------------------------------------------------------------------------------------------------------------------------#
################################################# Setup tools script main function #################################################
#----------------------------------------------------------------------------------------------------------------------------------#

def main() -> int:
    """
    Main entry point for the setuptools script
    """

    # Setup our source root if it is not 
    # the same directory as this script file
    if SOURCE_ROOT != '.':
        sys.path.append(SOURCE_ROOT)
        os.chdir(SOURCE_ROOT)

    # Register our commands and call the `setup` function from
    # the setuptools module
    commands.register_commands()
    setup(
        name=APP_NAME,
        packages=PACKAGES,
        version=utils.get_application_version(),
        setup_requires=[
            'pytest-runner',
        ],
        tests_require=[
            'pytest',
            'pylint~=2.6.0',
            'pytest-pylint',
        ],
        cmdclass=command.command_book.get_commands(),
        options={
            'build_apps': {
                'include_patterns': INCLUDE_PATTERNS,
                'rename_paths': RENAME_PATHS,
                'gui_apps': {
                    APP_NAME: 'quest/client/client.py',
                },
                'macos_main_app': APP_NAME,
                'requirements_path': utils.get_doc_file_path('requirements.txt'),
                'log_filename': '$USER_APPDATA/%s/logs/%s.log' % (APP_NAME, APP_NAME),
                'exclude_modules': {
                    '*': EXCLUDE_MODULES
                },
                'plugins': PLUGINS,
                'icons': {
                    APP_NAME: CLIENT_ICONS,
                },
            },
            'bdist_apps': {
                'installers': {
                    'manylinux1_x86_64': 'zip',
                }
            },
    })

    # Return a success exit code
    return 0

# Main entry point for the setuptools script
if __name__ == '__main__':
    sys.exit(main())

#----------------------------------------------------------------------------------------------------------------------------------#
####################################################################################################################################
#----------------------------------------------------------------------------------------------------------------------------------#