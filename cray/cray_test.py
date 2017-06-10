import unittest

from yatest import testpost, testpage

if __name__ == '__main__':
    all_suites = []
    all_suites.append(testpost.get_test_suites())
    all_suites.append(testpage.get_test_suites())

    alltests = unittest.TestSuite(all_suites)

    unittest.TextTestRunner(verbosity=2).run(alltests)
    