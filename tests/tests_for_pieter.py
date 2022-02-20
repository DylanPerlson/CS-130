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

    def test_move_sheet_pieter(self):
        wb = Workbook()
        (idx1, name1) = wb.new_sheet("first_sheet")
        (idx2, name2) = wb.new_sheet("second_sheet")
        (idx3, name3) = wb.new_sheet("move_to_second_sheet")

        # print('idx1', idx1)
        # print('idx2', idx2)
        # print('idx3', idx3)

        wb.move_sheet(name3, 1)

        self.assertEqual(wb.sheets[1].sheet_name, "move_to_second_sheet")
        self.assertEqual(wb.sheets[2].sheet_name, "second_sheet")
        self.assertEqual(3,len(wb.sheets))
        self.assertEqual(wb.list_sheets(), [name1, name3, name2])







if __name__ == '__main__':
    unittest.main(verbosity=1)