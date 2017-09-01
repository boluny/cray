.. image:: https://travis-ci.org/boluny/cray.svg?branch=master
    :target: https://travis-ci.org/boluny/cray
    
cray
====

A micro static blog generator

Motivation
----------

The lazy author forgot the `Jekyll <http://jekyllrb.com>`_ usage and don't want to install Ruby and all start from 
the beginning.

# Yeah I know it's a shabby project until now but it will be updated in times.

Update in 2017-08-04:

I find `pelican <https://blog.getpelican.com/>`_ is a mature one, but I can still have my own one even it's not comply with python philosophy.


Usage 
-----

0. Prerequisite: Python3 and package pip installed and in %PATH%.

1. Clone the repository.

2. Cd into the root directory of the repository, install it using 

.. code-block:: bash 

    $ pip install .

3. Execute following commands:

.. code-block:: bash

    $ cray init [your-site-name]

    $ cd [your-site-name] && cray generate

    $ cray preview

4. Open browser for `http://127.0.0.1/ <http://127.0.0.1/>`_


Progress
--------

That's depends on some stuff if the author is defeated in **LOL** or **Wang Zhe Rong Yao** 
which is a game like LOL but on mobile platforms.

TODO list
---------

1. Usage hint of the program and CLI improvment.    [Done]
2. Add more unit tests.
3. Refactor if target #2 is done.
4. Want to generate mindmap using d3.js if I could write a markdown to d3 tree converter.
