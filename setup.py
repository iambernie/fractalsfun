#!/usr/bin/env python
import os
from setuptools import setup, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.tgz ./*.egg-info')

        os.system('find . -name "*.pyc" -delete')
        os.system('find . -type d -name "__pycache__" -delete')

class TestCommand(Command):
    description = "run all tests"
    user_options = [] # distutils complains if this is not here.

    def __init__(self, *args):
        self.args = args[0]
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    def run(self):
        from fractalsfun.tests import runtests
        runtests.run_all_tests()


setup(
    name = "fractalsfun",
    version = "0.0.1",
    packages = ['fractalsfun'],
    cmdclass = {'clean': CleanCommand,
                'test': TestCommand,}
)

