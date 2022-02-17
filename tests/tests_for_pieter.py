import context
from sheets import *
from decimal import Decimal
import unittest


D = Decimal # D(1) is now equivalent to decimal.Decimal(1)

class Pieter(unittest.TestCase):
    def test_minus_address(self):
        wb = Workbook()
        (_, sheet) = wb.new_sheet()
        wb.set_cell_contents(sheet,'A1','=1')   
        wb.set_cell_contents(sheet,'A2','=-A1')
        self.assertEqual(D(-1), wb.get_cell_value(sheet, 'a2'))

    def test_sheet_extent_shrinking(self):
        pass



if __name__ == '__main__':
    unittest.main(verbosity=1)