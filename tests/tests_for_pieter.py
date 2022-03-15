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
        wb.set_cell_contents(sh,'c2', 'three')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        # [[1, 2, 'three'],
        #  [4, 5, 6],
        #  [7, 8, 9]]

        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(1, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 1)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(1, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 7)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(2, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 5)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(2, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 8)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(three, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 'three')
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(three, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 6)

        # print(wb.get_cell_value(sh, 'A1'))

    def test_vlookup(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', 'three')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '=true')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        # [[1   , 2, 'three'],
        #  [4   , 5, 6],
        #  [true, 8, 9]]

        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 1)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 'three')
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(4, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 5)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(4, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 6)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(true, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), True)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(true, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 9)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(false, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1').get_type(), CellErrorType.TYPE_ERROR)

    def test_if_with_ranges(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'B1', 'false')

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        wb.set_cell_contents(sh, 'A10', '=AVERAGE(IF(B1, A2:A4, B2:B4))') # TODO more tests

        # print(wb.get_cell_value(sh, 'A10'))

    def test_choose_with_ranges(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'B1', 'false')

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        wb.set_cell_contents(sh, 'A10', '=SUM(CHOOSE(1, A2:A4, B2:B4))') # TODO more tests

        # print(wb.get_cell_value(sh, 'A10'))

    def test_indirect_with_ranges(self):
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


        # wb.set_cell_contents(sh, 'A1', '=IFERROR(VLOOKUP(1, INDIRECT(B1 & "!A2:c4"), 2), "")') # TODO more tests
        # wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1 & "!A2:c4")') # TODO more tests
        wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1 & "!A2:c4")') # TODO more tests

        print(wb.get_cell_value(sh, 'A1'))

        # print(wb.get_cell_value(sh, 'A10'))


    # SUM(1,2,3,4)




if __name__ == '__main__':
    unittest.main(verbosity=1)