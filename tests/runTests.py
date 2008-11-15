#!/usr/bin/env python
#
#   hostmap
#
#   Author:
#    Alessandro `jekil` Tanasi <alessandro@tanasi.it>
#
#   License:
#    This program is private software; you can't redistribute it and/or modify
#    it. All copies, included printed copies, are unauthorized.
#    
#    If you need a copy of this software you must ask for it writing an
#    email to Alessandro `jekil` Tanasi <alessandro@tanasi.it>



import sys
sys.path.append("../")

import unittest

# Importing tests
from testCommon import *
from testOptionParser import *



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testCommon))
    suite.addTest(unittest.makeSuite(testOptionParser))
    unittest.TextTestRunner(verbosity=4).run(suite)
