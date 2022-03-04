import context
from sheets import *
from decimal import Decimal
from sheets import version
import unittest

import os; os.system('clear')

D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    # pass


    # TODO is this supposed to be supported
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

    #     wb.set_cell_contents(sh, 'a1', '=AND(5 < 6 , XOR(True,false,6), OR(NOT(EXACT(true, false)), XOR(true, false, true)))')
    #     print(wb.get_cell_value(sh, 'A1'))
    #     wb.set_cell_contents(sh, 'a1', '=AND(true, false)')
    #     print(wb.get_cell_value(sh, 'A1'))

    # # this test is in aarons file as well
    # def test_exact(self):
    #     wb = Workbook()
    #     (_, name) = wb.new_sheet("s1")
    #     wb.set_cell_contents(name,'A3','=EXACT("hello", "HELLO")')
    #     wb.set_cell_contents(name,'A4','=EXACT("Hello","Hello")')
    #     wb.set_cell_contents(name,'A5','=EXACT("Hello", "hElLo")')

    #     self.assertEqual(wb.get_cell_value(name, 'A3'), False)
    #     self.assertEqual(wb.get_cell_value(name, 'A4'), True)
    #     self.assertEqual(wb.get_cell_value(name, 'A5'), False)

    def test_version_func(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh,'A1','=VERSION()')

        self.assertEqual(version, wb.get_cell_value(sh, 'A1'))








if __name__ == '__main__':
    unittest.main(verbosity=1)