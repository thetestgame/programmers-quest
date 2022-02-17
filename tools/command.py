"""
Contains tools for populating the setuptools script with console
command objects
"""

#----------------------------------------------------------------------------------------------------------------------------------#

class CommandBook(object):
    """
    Book object containing all commands known by the tools system
    """

    def __init__(self):
        super().__init__()
        self.__commands = {}

    def get_command(self, cmd: str) -> object:
        """
        Retrieves the requested command if it exists
        """

        return self.__commands.get(cmd, None)

    def get_commands(self) -> dict:
        """
        Retrieves all registered commands
        """

        return self.__commands

    def register_command(self, cmd: str, cls: object) -> None:
        """
        Registers a new command with the book if the command does not
        already exist
        """

        if self.get_command(cmd) != None:
            print('Failed to register command (%s). Command already in use' % cmd)

            return

        self.__commands[cmd] = cls

command_book = CommandBook()

#----------------------------------------------------------------------------------------------------------------------------------#

class CommandDecorator(object):
    """
    Custom decorator for registering setuptool commands
    """

    def __init__(self, cmd: str):
        super().__init__()
        self.__cmd = cmd

    def __call__(self, cls: object) -> object:
        """
        Registers the decorated object with the CommandBook instance
        """

        command_book.register_command(self.__cmd, cls)
        return cls

command = CommandDecorator

#----------------------------------------------------------------------------------------------------------------------------------#