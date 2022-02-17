import sys
import pkgutil
import traceback
import importlib

#----------------------------------------------------------------------------------------------------------------------------------#

def register_commands() -> None:
    """
    Imports all files inside the commands module
    """

    # Import module commands
    package = sys.modules[__name__]
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg:
            continue

        import_path = 'tools.commands.%s' % modname
        try:
            module = importlib.import_module(import_path)
        except:
            print('Failed to import command module: %s (%s)' % (modname, import_path))
            print(traceback.format_exc())

#----------------------------------------------------------------------------------------------------------------------------------#