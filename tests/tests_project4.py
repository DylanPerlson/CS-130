import context
from sheets import *
import decimal
import unittest


class Project3(unittest.TestCase):
    def test_lark_bool_lit(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'a1', '=true')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=FaLse')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

    def test_bool_oper(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()

        # stuff that should be True

        wb.set_cell_contents(sh, 'a1', '=true')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=5=5')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="e" = "e"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="e" = "E"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=false < true')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="BLUE" = "blue"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="12" > 12')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        # stuff that should be False

        wb.set_cell_contents(sh, 'a1', '=(5 = 4)')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=5 != 5')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="BLUE" < "blue"')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="a" < "["')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="TRUE" > FALSE')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=faLse > true')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=true == false')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'b1', 'hello world')
        wb.set_cell_contents(sh, 'b2', "hello")
        wb.set_cell_contents(sh, 'a1', '=b1 = B2 & " world"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))



if __name__ == '__main__':
    unittest.main(verbosity=1)