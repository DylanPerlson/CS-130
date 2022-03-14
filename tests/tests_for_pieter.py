import context
from sheets import *
from decimal import Decimal
import unittest

import os; os.system('clear')

D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    def test_hlookup(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'a3', '3')
        wb.set_cell_contents(sh,'b3', '4')
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(42, a2:b3, 3)')





if __name__ == '__main__':
    unittest.main(verbosity=1)