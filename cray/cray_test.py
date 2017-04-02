import unittest

from yatest import testpost

if __name__ == '__main__':
    all_suites = []
    post_suites = testpost.get_test_suites()
    all_suites.append(post_suites)


    alltests = unittest.TestSuite(all_suites)
    
    unittest.TextTestRunner(verbosity=2).run(alltests)
    