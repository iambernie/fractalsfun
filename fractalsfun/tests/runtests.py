#!/usr/bin/env python
import unittest
from fractalsfun.tests import all_tests
from fractalsfun.tests.colored import ColoredTextTestRunner


def run_all_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(all_tests)

    runner = ColoredTextTestRunner(verbosity=2)
    results = runner.run(suite)

    if (len(results.failures) or len(results.errors)) > 0:
        exit(1)
    else:
        exit(0)




