"""
Test cases for the prc module found in Quest/Engine
"""

#----------------------------------------------------------------------------------------------------------------------------------#

from quest.engine import prc

#----------------------------------------------------------------------------------------------------------------------------------#

# Test PRC data used for PyTest
test_data = """
test-bool #t
test-int 1
test-double 2.0
test-string hello
"""

#----------------------------------------------------------------------------------------------------------------------------------#

def test_prc_file_data() -> None:
    """
    Loads the requested string of PRC data into the Panda3D
    runtime configuration under the pytest label and verifies
    the values was properly set
    """

    prc.load_prc_file_data(test_data, 'pytest')
    assert prc.get_prc_bool('test-bool', False) == True

#----------------------------------------------------------------------------------------------------------------------------------#