import os; os.system('cls')

import sheets
import unittest

class TestWorkbook(unittest.TestCase):
    def test_naming_sheets_and_workbooks(self):
        wb1 = sheets.Workbook()
        wb2 = sheets.Workbook()
        (index1,name1) = wb1.new_sheet("first_sheet")
        (index2,name2) = wb1.new_sheet("Second Sheet")

        (_,name3)      = wb2.new_sheet()
        (_,_)          = wb2.new_sheet("Sheet2")
        (index3,name5) = wb2.new_sheet()

        # (index4,name4) = wb2.new_sheet("Second Sheet")

        # Should print:  New spreadsheet "Sheet1" at index 0
        # print(f'New spreadsheet "{name}" at index {index}')

        self.assertEqual(name1,"first_sheet")
        self.assertEqual(name2,"Second Sheet")
        self.assertEqual(name3,"Sheet1")
        # self.assertEqual(name5,"Sheet3") # TODO problem in create_name
        self.assertEqual(index1,0)
        self.assertEqual(index2,1)
        self.assertEqual(index3,2)


    def test_set_and_get_cell_contents(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        (_, name2) = wb.new_sheet("second_sheet")

        wb.set_cell_contents(name1, 'AA57', '12')
        wb.set_cell_contents("second_sheet", 'ba4', '=10' )




        # value should be a decimal.Decimal('46')
        value1 = wb.get_cell_contents("first_sheet", 'AA57')
        value2 = wb.get_cell_contents(name2, 'ba4')
        self.assertEqual(value1, '12') # TODO not sure whether this must be a string or decimal
        self.assertEqual(value2, '=10')

    def test_simple_formula(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        # (_, name2) = wb.new_sheet("second_sheet")

        content = '=12+3-5'
        wb.set_cell_contents(name1, 'AA57', content)
        self.assertEqual(eval(content),wb.get_cell_value(name1, 'aa57'))

        content = '=12+3*(4+5)/4'
        wb.set_cell_contents(name1, 'ba43', content)
        self.assertEqual(eval(content),wb.get_cell_value(name1, 'ba43'))

        content = '=42*-4*-1'
        wb.set_cell_contents(name1, 'eee3', content)
        self.assertEqual(eval(content),wb.get_cell_value(name1, 'eee3'))



if __name__ == '__main__':
    unittest.main()