# -*- coding: utf-8 -*-
'''test cases for config_loader module'''

import unittest
import os
import shutil
import cray.craylib.config_loader as config_loader
from cray.craylib.generate_manager import GenerateManager


ROOT_DIR = os.path.join(os.path.dirname(__file__), "test_site")
SITE_DIR = os.path.join(os.path.dirname(__file__), "_site")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(SiteGenerationTestCase())

    return suite

class SiteGenerationTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        if os.path.exists(SITE_DIR):
            shutil.rmtree(SITE_DIR, ignore_errors=True)

        conf_loader = config_loader.ConfigLoader(ROOT_DIR)
        self.assertTrue(conf_loader.parse_config())
        generate_manager = GenerateManager(ROOT_DIR)
        generate_manager.read_config(conf_loader)
        generate_manager.generate_site()

        self.assertTrue(os.path.exists(SITE_DIR))

        index_path = os.path.join(SITE_DIR, 'index.html')
        about_path = os.path.join(SITE_DIR, 'about', 'index.html')
        hello_post_path = os.path.join(SITE_DIR, 'post', '2017', '6', '2', 'hello-world', \
        'index.html')

        self.assertTrue(os.path.exists(index_path))
        self.assertTrue(os.path.exists(about_path))
        self.assertTrue(os.path.exists(hello_post_path))

        index_content = r'''<html>
<head>
	<meta charset="utf-8">
    <title>Index</title>
</head>
<body>
	<header class="site-header">

  <div class="wrapper">
    <a class="site-title" href="/">Index</a>

    <nav class="site-nav">
	<!--
      <a href="#" class="menu-icon">
        <svg viewBox="0 0 18 15">
          <path fill="#424242" d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.031C17.335,0,18,0.665,18,1.484L18,1.484z"/>
          <path fill="#424242" d="M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0c0-0.82,0.665-1.484,1.484-1.484 h15.031C17.335,6.031,18,6.696,18,7.516L18,7.516z"/>
          <path fill="#424242" d="M18,13.516C18,14.335,17.335,15,16.516,15H1.484C0.665,15,0,14.335,0,13.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.031C17.335,12.031,18,12.696,18,13.516L18,13.516z"/>
        </svg>
      </a>
	-->
      <div class="trigger">
        
          
          <a class="page-link" href="/about/">about</a>
          
        
      </div>
    </nav>

  </div>

</header>
	<h1>Post list:</h1>
    <ul id="navigation">
    
        <li><a href="post/2017/6/2/hello-world">Welcome to Cray!</a></li>
    
    </ul>

    <footer>
<h3>Powered by Bolun 2013 - 2017</h3>
</footer>
</body>
</html>'''

        about_content = r'''<html>
<head>
	<meta charset="utf-8">
    <title>about</title>
</head>
<body>
	<header class="site-header">

  <div class="wrapper">
    <a class="site-title" href="/">Index</a>

    <nav class="site-nav">
	<!--
      <a href="#" class="menu-icon">
        <svg viewBox="0 0 18 15">
          <path fill="#424242" d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.031C17.335,0,18,0.665,18,1.484L18,1.484z"/>
          <path fill="#424242" d="M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0c0-0.82,0.665-1.484,1.484-1.484 h15.031C17.335,6.031,18,6.696,18,7.516L18,7.516z"/>
          <path fill="#424242" d="M18,13.516C18,14.335,17.335,15,16.516,15H1.484C0.665,15,0,14.335,0,13.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.031C17.335,12.031,18,12.696,18,13.516L18,13.516z"/>
        </svg>
      </a>
	-->
      <div class="trigger">
        
          
          <a class="page-link" href="/about/">about</a>
          
        
      </div>
    </nav>

  </div>

</header> 
	<h1>about</h1>
	<div><p>This is the first test page for test_site</p></div>
	
	<footer>
<h3>Powered by Bolun 2013 - 2017</h3>
</footer> 
    
</body>
</html>'''

        hello_content = r'''<html>
<head>
	<meta charset="utf-8">
    <title>Welcome to Cray!</title>
</head>
<body>
	<header class="site-header">

  <div class="wrapper">
    <a class="site-title" href="/">Index</a>

    <nav class="site-nav">
	<!--
      <a href="#" class="menu-icon">
        <svg viewBox="0 0 18 15">
          <path fill="#424242" d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.031C17.335,0,18,0.665,18,1.484L18,1.484z"/>
          <path fill="#424242" d="M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0c0-0.82,0.665-1.484,1.484-1.484 h15.031C17.335,6.031,18,6.696,18,7.516L18,7.516z"/>
          <path fill="#424242" d="M18,13.516C18,14.335,17.335,15,16.516,15H1.484C0.665,15,0,14.335,0,13.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.031C17.335,12.031,18,12.696,18,13.516L18,13.516z"/>
        </svg>
      </a>
	-->
      <div class="trigger">
        
          
          <a class="page-link" href="/about/">about</a>
          
        
      </div>
    </nav>

  </div>

</header> 
	<h1>Welcome to Cray!</h1>
	<p>2017-06-02 22:22:22</p>
	<div><p>hello world!</p></div>
	
	<footer>
<h3>Powered by Bolun 2013 - 2017</h3>
</footer> 
    
</body>
</html>'''

        with open(index_path) as index_fd:
            self.assertEqual(index_content, index_fd.read())

        with open(about_path) as about_fd:
            self.assertEqual(about_content, about_fd.read())

        with open(hello_post_path) as hello_fd:
            self.assertEqual(hello_content, hello_fd.read())

        if os.path.exists(SITE_DIR):
            shutil.rmtree(SITE_DIR, ignore_errors=True)
