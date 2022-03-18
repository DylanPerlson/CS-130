"""Tests that are specifically for Pieter."""

import os
import unittest

import context
from sheets import *


os.system('clear')

class Pieter(unittest.TestCase):
    """Tests that are specifically for Pieter."""

    def test_sorting_simple(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '1')

        wb.sort_region(sh, 'A2', 'C4', [1])
        val = wb.get_cell_value(sh, 'B2')
        self.assertEqual(val, 5, f'instead it is: {val}') # excel #1

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '1')

        wb.sort_region(sh, 'A2', 'C4', [3])
        val = wb.get_cell_value(sh, 'B2')
        self.assertEqual(val, 8, f'instead it is: {val}') # excel #2

    def test_sorting_multiple_cols(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'a2', '2')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '4')
        wb.set_cell_contents(sh,'a3', '1')
        wb.set_cell_contents(sh,'b3', '3')
        wb.set_cell_contents(sh,'c3', '5')
        wb.set_cell_contents(sh,'a4', '2')
        wb.set_cell_contents(sh,'b4', '1')
        wb.set_cell_contents(sh,'c4', '6')

        wb.sort_region(sh, 'A2', 'C4', [1,2])
        val = wb.get_cell_value(sh, 'C3')
        self.assertEqual(val, 4, f'instead it is: {val}') # excel #3

    def test_sorting_stable(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'a2', '2')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '4')
        wb.set_cell_contents(sh,'a3', '1')
        wb.set_cell_contents(sh,'b3', '3')
        wb.set_cell_contents(sh,'c3', '5')
        wb.set_cell_contents(sh,'a4', '2')
        wb.set_cell_contents(sh,'b4', '1')
        wb.set_cell_contents(sh,'c4', '6')

        wb.sort_region(sh, 'A2', 'C4', [1])
        val = wb.get_cell_value(sh, 'C3')
        self.assertEqual(val, 4, f'instead it is: {val}') # excel #4

    def test_sorting_descending(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'a2', '2')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '4')
        wb.set_cell_contents(sh,'a3', '1')
        wb.set_cell_contents(sh,'b3', '3')
        wb.set_cell_contents(sh,'c3', '5')
        wb.set_cell_contents(sh,'a4', '2')
        wb.set_cell_contents(sh,'b4', '1')
        wb.set_cell_contents(sh,'c4', '6')

        wb.sort_region(sh, 'A2', 'C4', [-1])
        val = wb.get_cell_value(sh, 'C3')
        self.assertEqual(val, 1, f'instead it is: {val}') # excel #5

    def test_sorting_blanks(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh, 'B1', sh)

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        # wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '1')

        wb.sort_region(sh, 'A2', 'C4', [3])
        val = wb.get_cell_value(sh, 'B3')
        self.assertEqual(val, 8, f'instead it is: {val}') # excel #6

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        # wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '1')

        wb.sort_region(sh, 'A2', 'C4', [1])
        val = wb.get_cell_value(sh, 'C2')
        self.assertEqual(val, 6, f'instead it is: {val}') # excel #7

    def test_sorting_errors(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh, 'B1', sh)

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'c2', '4')

        wb.set_cell_contents(sh,'a3', '#DIV/0!')
        wb.set_cell_contents(sh,'c3', '3')

        wb.set_cell_contents(sh,'a4', '#REF!')
        wb.set_cell_contents(sh,'c4', '2')

        wb.set_cell_contents(sh,'A5', '')
        wb.set_cell_contents(sh,'C5', '1')

        wb.sort_region(sh, 'A2', 'C5', [1])

        self.assertEqual(wb.get_cell_value(sh, 'C2'), 1)
        self.assertEqual(wb.get_cell_value(sh, 'C3'), 2)
        self.assertEqual(wb.get_cell_value(sh, 'C4'), 3)
        self.assertEqual(wb.get_cell_value(sh, 'C5'), 4)

    def test_sorting_validity(self):
        """If the specified sheet name is not found, a KeyError is raised.
        If any cell location is invalid, a ValueError is raised.
        If the sort_cols list is invalid in any way, a ValueError is raised."""

        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh, 'B1', sh)

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        with self.assertRaises(KeyError):
            wb.sort_region('non_existing_sheet', 'A2', 'C4', [1])

        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'VERYLONGSHEET1', 'C4', [1])

        # No column may be specified twice in sort_cols; e.g. [1, 2, 1] or
        # [2, -2] are both invalid specifications.
        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'A2', 'C4', [1, 2, 1])

        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'A2', 'C4', [2, -2])

        # The sort_cols list may not be empty.  No index may be 0, or refer
        # beyond the right side of the region to be sorted.
        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'A2', 'C4', [])

        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'A2', 'C4', [1, 2, 3, 0])

        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'A2', 'C4', [1, 2, 10])

        with self.assertRaises(ValueError):
            wb.sort_region(sh, 'A2', 'C4', [1, 2, -10])





if __name__ == '__main__':
    unittest.main(verbosity=1)
