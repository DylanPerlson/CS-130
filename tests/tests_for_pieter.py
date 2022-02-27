import context
from sheets import *
from decimal import Decimal
import unittest

import os; os.system('clear')

D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    # TODO is this supposed to be supported
    # def test_double_quote_literal(self):
    #     wb = Workbook()
    #     (_, sh) = wb.new_sheet()
    #     wb.set_cell_contents(sh, 'A1', "one quote: ''")
    #     content1 = wb.get_cell_value(sh, 'A1')

    #     self.assertEqual(content1, "one quote: '")

    def test_lark_bool(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'a1', '=AND(5 < 6 , tester(true,false,6), OR(NOT(EXACT(true, false)), XOR(true, false, true)))')
        # print(wb.get_cell_value(sh, 'A1').pretty())

        wb.set_cell_contents(sh, 'a1', '=5 + 5')
        # print(wb.get_cell_value(sh, 'A1').pretty())








if __name__ == '__main__':
    unittest.main(verbosity=1)