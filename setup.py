# -*- encoding: utf-8 -*-
import codecs
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import subprocess as sp
import sys

# Fetch version from version.py
version_py = os.path.join(os.path.dirname(__file__),
                          'src', 'symboldict', 'version.py')
with codecs.open(version_py, encoding='utf8') as fh:
    version = (fh.read()
        .strip().split('=')[-1].replace('"','')).strip()

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


install_requires = [
    #'pytest',
    #'pytest-bdd',
]
dependency_links = [
    
]

long_description = (
    codecs.open(os.path.join(os.path.dirname(__file__), "README.rst"),
                encoding="utf-8").read() 
)

if __name__ == '__main__':
    setup(
        name='symboldict',
        license='MIT license',
        version="{ver}".format(ver=version),
        author='Eric Ringeisen',
        description='A dict class to organize and lazily import symbols',
        long_description=long_description,
        url="https://github.com/Gribouillis/symboldict",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=install_requires,
        dependency_links=dependency_links,
        include_package_data=True,
        entry_points="""\
        
        """,
        tests_require=['tox'],
        cmdclass = {'test': Tox},
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            "Topic :: Software Development :: Libraries",
            "Topic :: Utilities",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3"
        ] + [("Programming Language :: Python :: %s" % x)
                for x in "2.7 3.4".split()],
    )
