import unittest
from tests_project1 import Project1
from tests_project2 import Project2
from tests_project3 import Project3
from tests_project4 import Project4
from tests_for_aaron import Aaron
from tests_for_dylan import Dylan
from tests_for_pieter import Pieter

import os; os.system('clear')


def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [Project1, Project2, Project3, Project4,
                            Aaron, Dylan, Pieter]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner(verbosity=1)
    results = runner.run(big_suite)

    # ...

if __name__ == '__main__':
    run_some_tests()