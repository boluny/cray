# -*- coding: utf-8 -*-
'''test cases for utility module'''

import unittest
import os
import cray.craylib.utility as test_module

ROOT_DIR = os.path.join(os.path.dirname(__file__), "test_site")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(UtilityIsValidSiteTestCase())
    suite.addTest(UtilityTrimDoubleQuotationMarkTestCase())
    suite.addTest(UtilityFullGeneratePathTestCase())
    suite.addTest(UtilityNameConflictTestCase())
    suite.addTest(UtilityFileNameNoExtTestCase())
    suite.addTest(UtilityTryConvertDateStrTestCase())
    suite.addTest(UtilityIsYesTestCase())

    return suite

class UtilityIsValidSiteTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        self.assertTrue(test_module.is_valid_site(ROOT_DIR))
        self.assertFalse(test_module.is_valid_site("test"))

class UtilityTrimDoubleQuotationMarkTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        self.assertEqual('', test_module.trim_double_quotation_mark(''))
        self.assertEqual('hello', test_module.trim_double_quotation_mark('"hello"'))
        self.assertNotEqual('world', test_module.trim_double_quotation_mark('"hello"'))
        self.assertNotEqual('hello', test_module.trim_double_quotation_mark('"hello'))
        self.assertNotEqual('hello', test_module.trim_double_quotation_mark('hello"'))

class UtilityFullGeneratePathTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def testBasic(self):
        '''Run test'''
        root = '/home/byuan'
        conf = {}
        self.assertEqual(os.path.join(root, '.', '_site'), \
        test_module.full_generate_path(root, conf))
        conf['generate_path'] = '..'
        self.assertEqual(os.path.normpath(os.path.join(root, conf['generate_path'], '_site')), \
        test_module.full_generate_path(root, conf))
        conf['site_name'] = 'boluny.github.com'
        self.assertEqual(
            os.path.normpath(os.path.join(root, conf['generate_path'], conf['site_name'])),
            test_module.full_generate_path(root, conf))

    def testBaseConfigured(self):
        root = '/home/byuan'
        conf = {}
        conf['base'] = 'blog'
        self.assertEqual(os.path.normpath(os.path.join(root, '.', "_site", conf['base'])), \
            test_module.full_generate_path(root, conf))

    def testBaseAbsoluteConfigured(self):
        root = '/home/byuan'
        conf = {}
        conf['base'] = '/blog'
        self.assertEqual(os.path.normpath(os.path.join(root, '.', "_site", 'blog')), \
            test_module.full_generate_path(root, conf))

class UtilityNameConflictTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        name_a = ['hello', 'world', 'ready']
        name_b = ['hello', 'word', 'read']
        name_c = ['hell', 'word', 'read']
        self.assertTrue(test_module.name_conflict(name_a, name_b))
        self.assertFalse(test_module.name_conflict(name_a, name_c))
        self.assertTrue(test_module.name_conflict(name_b, name_c))

class UtilityFileNameNoExtTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        file_a = '/home/byuan/testa.md'
        file_b = 'C:\\test\\testb.md'
        file_c = 'testc.md'
        file_d = ''
        self.assertEqual('testa', test_module.file_name_no_ext(file_a))
        self.assertEqual('testc', test_module.file_name_no_ext(file_c))
        self.assertEqual('', test_module.file_name_no_ext(file_d))

        if os.name == 'nt':
            self.assertEqual('testb', test_module.file_name_no_ext(file_b))

class UtilityTryConvertDateStrTestCase(unittest.TestCase):
    '''Test case for converting time string to datetime object'''
    def runTest(self):
        '''Run test'''
        from datetime import datetime, timezone, timedelta

        time_str1='2013-06-19 15:26 +0800'
        time_object1 = datetime(2013, 6, 19, 15, 26, tzinfo=timezone(timedelta(0, 28800)))
        self.assertEqual(time_object1, test_module.try_convert_date_str(time_str1))

        time_str2='2013-06-19 15:26:27 +0800'
        time_object2 = datetime(2013, 6, 19, 15, 26, 27, tzinfo=timezone(timedelta(0, 28800)))
        self.assertEqual(time_object2, test_module.try_convert_date_str(time_str2))

        time_str3='2013-06-19 15:26:27'
        time_object3 = datetime(2013, 6, 19, 15, 26, 27)
        self.assertEqual(time_object3, test_module.try_convert_date_str(time_str3))


class UtilityIsYesTestCase(unittest.TestCase):
    '''Test case for indicate if a string literal is true or false'''
    def runTest(self):
        '''Run test'''

        str1 = 'y'
        self.assertTrue(test_module.is_yes(str1))

        str2 = 'yes'
        self.assertTrue(test_module.is_yes(str2))

        str3 = 'Y'
        self.assertTrue(test_module.is_yes(str3))

        str4 = 'Yes'
        self.assertTrue(test_module.is_yes(str4))

        str5 = 'true'
        self.assertTrue(test_module.is_yes(str5))

        str6 = 'True'
        self.assertTrue(test_module.is_yes(str6))

        str7 = 'no'
        self.assertFalse(test_module.is_yes(str7))
