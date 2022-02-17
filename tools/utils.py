import datetime
import sys
import os

from setuptools import setup
from tools import command, commands

#----------------------------------------------------------------------------------------------------------------------------------#

def get_application_version() -> None:
    """
    Retrieves the application version string based
    on the current datetime and short git sha value
    """

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime('%m.%d.%Y')

    try:
        import git

        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.commit.hexsha
        short_sha = repo.git.rev_parse(sha, short=4)

        version = '%s.%s' % (timestamp, short_sha)
    except Exception:
        version = timestamp
    
    return version

#----------------------------------------------------------------------------------------------------------------------------------#

def get_doc_file_path(filename: str) -> str:
    """
    Returns the requested filename's quest docs absolute path
    """

    root = os.getcwd()
    docs_folder = os.path.join(root, 'quest%sdocs' % os.sep)
    return os.path.join(docs_folder, filename)

#----------------------------------------------------------------------------------------------------------------------------------#
