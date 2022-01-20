def fact(n):
    if n < 0:
        return 1
        # raise ValueError('n must be at least 0')
    if n == 0:
        return 1
    return n * fact(n - 1)

import unittest

class TestFact(unittest.TestCase):
    def test_fact_3(self):
        self.assertEqual(fact(3), 6)
    def test_fact_0(self):
        self.assertEqual(fact(0), 1)
    def test_fact_throws(self):
        with self.assertRaises(ValueError):
            fact(-4)

if __name__ == '__main__':
    unittest.main()