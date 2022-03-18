"""Tests that are specifically for Pieter."""

import os
import unittest

import context
from sheets import *


os.system('clear')

class Pieter(unittest.TestCase):
    """Tests that are specifically for Pieter."""

    def test_sorting(self):
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

        #wb.sort_region(sh, 'A2', 'C4', [1]) keep this commented until we actually use

        val = wb.get_cell_value(sh, 'B2')
        #self.assertEqual(val, 5, f'instead it is: {val}')


if __name__ == '__main__':
    unittest.main(verbosity=1)
