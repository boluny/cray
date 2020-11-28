import os

from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Programming Language :: Python",
#   "Programming Language :: Python :: 2",
#   "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
#     "Programming Language :: Python :: Implementation :: PyPy",
]

# extras_require = {
#     "format" : ["rfc3987", "strict-rfc3339", "webcolors"],
#     ":python_version=='2.7'": ["functools32"],
# }

setup(
    name="cray",
    packages=find_packages(exclude=['yatest']),
    version="0.0.3",
    # package_data={"jsonschema": ["schemas/*.json"]},
    setup_requires=["Jinja2>=2.8", "Markdown>=2.6.8"],
    test_suite="yatest",
    # extras_require=extras_require,
    author="Bolun Yuan",
    author_email="yuanbl0605@163.com",
    classifiers=classifiers,
    description="A micro static site generator written in Python",
    license="MIT",
    long_description=long_description,
    entry_points={"console_scripts": ["cray = cray.cli:main"]},
    # vcversioner={"version_module_paths" : ["jsonschema/_version.py"]},
)
