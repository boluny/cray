import unittest
from craylib.Post import Post

def get_test_suites():
    suite = unittest.TestSuite()
    suite.addTest(PostGenerateTestCase())

    return suite

class PostGenerateTestCase(unittest.TestCase):
    def runTest(self):
        p1 = Post(r"E:\code_lab\visual_studio\cray\cray\sample_site\_post\2015-09-18-welcome-to-jekyll.markdown")
        p2 = Post(r"E:\code_lab\visual_studio\cray\cray\sample_site\_post\2015-09-18-no-existence.markdown")

        should_meta = {'title': r'"Welcome to Jekyll!"',
                       'layout': 'post',
                       'date': '2015-09-18 00:13:20',
                       'categories': 'jekyll update'
                       }
        self.assertFalse(p2.is_existed())

        self.assertTrue(p1.is_existed())
        p1.parse_file()
        x = p1.get_metadata()
        self.assertEqual(should_meta, x)

