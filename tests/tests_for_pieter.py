import context
from sheets import *
from decimal import Decimal
import unittest


D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    def test_double_quote_string(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh, 'A1', "'one quote: ''")
        content1 = wb.get_cell_value(sh, 'A1')

        self.assertEqual(content1, "one quote: '")

    # def test_double_quote_literal(self):
    #     wb = Workbook()
    #     (_, sh) = wb.new_sheet()
    #     wb.set_cell_contents(sh, 'A1', "one quote: ''")
    #     content1 = wb.get_cell_value(sh, 'A1')

    #     self.assertEqual(content1, "one quote: '")

    def test_type_conversion(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh, 'A1', "'1")
        wb.set_cell_contents(sh, 'A2', "1")
        wb.set_cell_contents(sh, 'A3', "=A1+A2")

        self.assertEqual(wb.get_cell_value(sh, 'A3'), 2)

    def test_named_and_unnamed_sheets(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()







if __name__ == '__main__':
    unittest.main(verbosity=1)