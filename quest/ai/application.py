from quest.engine import core, prc, showbase
from quest.engine import runtime, vfs
from quest.framework import application

import argparse

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestAIApplication(application.QuestApplication):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main(*args, **kwargs) -> int:
    """
    Main entry point into the Programmer's Quest MMO AI server application
    """ 

    parser = argparse.ArgumentParser(description="Programmer's Quest AI server")
    #parser.add_argument('-p', '--port', type=int, default=9099, help='Port to listen for incoming connections against')

    #parsed_args = parser.parse_args()
    #startup_prc = 'server-port %d\n' % parsed_args.port

    kwargs['headless'] = True
    #kwargs['startup_prc'] = startup_prc
    kwargs['application_cls'] = QuestAIApplication

    return application.main(*args, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#