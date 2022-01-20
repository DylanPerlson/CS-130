import os; os.system('cls')
import context
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


    def test_white_space_in_sheet_name(self):
        wb = sheets.Workbook()
        with self.assertRaises(ValueError):
            (_,_) = wb.new_sheet(" first_sheet")
        with self.assertRaises(ValueError):
            (_,_) = wb.new_sheet("first_sheet ")


    def test_sheet_name_uniqueness(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        with self.assertRaises(ValueError):
            (_, name2) = wb.new_sheet("first_sheet")
        with self.assertRaises(ValueError):
            (_, name2) = wb.new_sheet("First_Sheet")
        

    def test_set_and_get_cell_contents(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        (_, name2) = wb.new_sheet("second_sheet")

        wb.set_cell_contents(name1, 'AA57', '12')
        wb.set_cell_contents("second_sheet", 'ba4', '=10' )
        wb.set_cell_contents("second_sheet", 'ba5', "'string" )

        content1 = wb.get_cell_contents("first_sheet", 'AA57')
        content2 = wb.get_cell_contents(name2, 'ba4')
        content3 = wb.get_cell_contents(name2, 'ba5')

        self.assertEqual(content1, '12') # TODO not sure whether this must be a string or decimal.Decimal
        self.assertEqual(content2, '=10')
        self.assertEqual(content3, "'string")

    def test_simple_formula(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        # (_, name2) = wb.new_sheet("second_sheet")

        content = '=12+3-5'
        wb.set_cell_contents(name1, 'AA57', content)
        self.assertEqual(eval(content[1:]),wb.get_cell_value(name1, 'aa57')) # TODO decimal.Decimal

        content = '=12+3*(4+5)/4'
        wb.set_cell_contents(name1, 'ba43', content)
        self.assertEqual(eval(content[1:]),wb.get_cell_value(name1, 'ba43'))

        content = '=42*-4*-1'
        wb.set_cell_contents(name1, 'eee3', content)
        self.assertEqual(eval(content[1:]),wb.get_cell_value(name1, 'eee3'))
    
    def test_max_sheet_size(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'ZZZZ9999', 'maximum')
        value1 = wb.get_cell_contents("first_sheet", 'ZZZZ9999')
        self.assertEqual(value1, 'maximum')

        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, 'ZZZZ10000', 'too many columns')
        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, 'AAAAA9999', 'too many rows')


    """ def test_simple_cell_reference(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        # (_, name2) = wb.new_sheet("second_sheet")

        wb.set_cell_contents(name1, 'AA57', '5')
        wb.set_cell_contents(name1, 'c4', '=aa57')
        self.assertEqual(5,wb.get_cell_value(name1, 'c4')) # TODO decimal.Decimal """


    def test_extent(self):
        wb = sheets.Workbook()
        (_, name) = wb.new_sheet("first_sheet")
        self.assertEqual((0,0),wb.get_sheet_extent(name))
        wb.set_cell_contents(name, 'D14', 'something')
        self.assertEqual((4,14),wb.get_sheet_extent(name))
        wb.set_cell_contents(name, 'Z3', 'something')
        self.assertEqual((26,14),wb.get_sheet_extent(name))
        wb.set_cell_contents(name, 'AA20', 'something')
        self.assertEqual((27,20),wb.get_sheet_extent(name))
        # TODO add update to extent if cells are cleared
        

    # def test_contents_always_string(self):

        




if __name__ == '__main__':
    unittest.main()