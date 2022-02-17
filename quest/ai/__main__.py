import sys
from quest.ai import application

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main() -> int:
    """
    Main entry point into the Programmer's Quest MMO AI server application
    """

    return application.main(development=True)

# Main entry point into the Programmer's Quest MMO AI server application
if __name__ == '__main__':
    sys.exit(main())

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
