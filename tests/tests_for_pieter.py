import context
from sheets import *
from decimal import Decimal
import unittest

import os; os.system('clear')

D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    pass


    # TODO is should be supported but isn't
    # def test_double_quote_literal(self):
    #     wb = Workbook()
    #     (_, sh) = wb.new_sheet()
    #     wb.set_cell_contents(sh, 'A1', "one quote: ''")
    #     content1 = wb.get_cell_value(sh, 'A1')

    #     self.assertEqual(content1, "one quote: '")

    # # look at the print output to run this test
    # def test_lark_func_parsing(self):
    #     wb = Workbook()
    #     (_,sh) = wb.new_sheet()

    #     print(wb.get_cell_value(sh, 'A1'))
    #     wb.set_cell_contents(sh, 'a1', '=AND(5 < 6 , XOR(True,false,6), OR(NOT(EXACT(true, false)), XOR(true, false, true)))')
    #     wb.set_cell_contents(sh, 'a1', '=AND(true, false)')
    #     print(wb.get_cell_value(sh, 'A1'))

    # def test_indirect_func(self):
    #     wb = Workbook()
    #     (_,sh) = wb.new_sheet()
    #     (_,sh2) = wb.new_sheet()












if __name__ == '__main__':
    unittest.main(verbosity=1)