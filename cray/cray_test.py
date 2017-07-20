# -*- coding: utf-8 -*-
'''module for unit test and task for CI'''

import unittest

from yatest import testpost, testpage

if __name__ == '__main__':
    all_test_suites = []
    all_test_suites.append(testpost.get_test_suites())
    all_test_suites.append(testpage.get_test_suites())

    alltests = unittest.TestSuite(all_test_suites)

    unittest.TextTestRunner(verbosity=2).run(alltests)
    