import context
from sheets import *
from decimal import Decimal
import numpy as np
import unittest

import os; os.system('clear')

D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):





    def test_indirect_with_ranges(self): # TODO write some tests for this
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'B1', 'sheet')

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        # wb.set_cell_contents(sh, 'A1', '=IFERROR(VLOOKUP(1, INDIRECT(B1 & "!A2:c4"), 2), "")')
        # wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, INDIRECT("sheet" & "!A2:c4"), 3)') # TODO works but needs test
        # wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, INDIRECT(B1 & "!A2:c4"), 3)') # TODO not working
        # wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, sheet!A2:c4, 2)')
        # wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1 & "!A2:c4")')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1 & "!A2:c4")')

        # print(wb.get_cell_value(sh, 'A1'))




if __name__ == '__main__':
    unittest.main(verbosity=1)