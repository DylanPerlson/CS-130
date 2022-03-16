import context
from sheets import *
from decimal import Decimal
import unittest

import os; os.system('clear')

D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    def test_choose_func_edgecase(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'B1', '5.5')
        wb.set_cell_contents(sh, 'B2', 'true')
        wb.set_cell_contents(sh, 'B3', '=False')

        # wb.set_cell_contents(sh, 'a1', '=IFERROR(A1, A1)') # TODO fix
        # self.assertEqual(4, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=EXACT(1,"1")') # TODO
        self.assertEqual(wb.get_cell_value(sh, 'A1'), True)

        wb.set_cell_contents(sh,'A1','=CHOOSE("string",1.5,2.5,true,  false  , B1, B2, B3, "last")') # TODO
        self.assertEqual(wb.get_cell_value(sh, 'A1').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,-2.5,true,  false  , B1, B2, B3, "last")') # TODO
        self.assertEqual(wb.get_cell_value(sh, 'A1'), -2.5)

    # def test_indirect_with_ranges(self): # TODO write some tests for this
    #     wb = Workbook()
    #     (_,sh) = wb.new_sheet('sheet')

    #     wb.set_cell_contents(sh,'B1', 'sheet')

    #     wb.set_cell_contents(sh,'a2', '1')
    #     wb.set_cell_contents(sh,'b2', '2')
    #     wb.set_cell_contents(sh,'c2', '3')
    #     wb.set_cell_contents(sh,'a3', '4')
    #     wb.set_cell_contents(sh,'b3', '5')
    #     wb.set_cell_contents(sh,'c3', '6')
    #     wb.set_cell_contents(sh,'a4', '7')
    #     wb.set_cell_contents(sh,'b4', '8')
    #     wb.set_cell_contents(sh,'c4', '9')

    #     # wb.set_cell_contents(sh, 'A1', '=IFERROR(VLOOKUP(1, INDIRECT(B1 & "!A2:c4"), 2), "")')
    #     # wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, INDIRECT("sheet" & "!A2:c4"), 2)')
    #     # wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, sheet!A2:c4, 2)')
    #     # wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1 & "!A2:c4")')
    #     # wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1 & "!A2:c4")')




if __name__ == '__main__':
    unittest.main(verbosity=1)