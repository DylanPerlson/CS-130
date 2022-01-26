import os; os.system('cls')
import context
import sheets
from sheets.cell_error import CellError, CellErrorType
import unittest
import decimal

class TestWorkbook(unittest.TestCase):
    """ Performing unit tests on the sheets module. """

    def test_empty_cells(self):
        """ Testing whether empty cells return 0 or ''. """   
        wb = sheets.Workbook()
        (_, name) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name,'B4','=A2+3')
        self.assertEqual(wb.get_cell_value(name,'B4'),3)
        wb.set_cell_contents(name,'B7','=A6&"hi"')
        self.assertEqual(wb.get_cell_value(name,'B7'),'hi')


    def test_naming_sheets_and_workbooks(self):
        wb1 = sheets.Workbook()
        wb2 = sheets.Workbook()
        (index1,name1) = wb1.new_sheet("first_sheet")
        (index2,name2) = wb1.new_sheet("Second Sheet")

        (_,name3)      = wb2.new_sheet()
        (_,_)          = wb2.new_sheet("Sheet2")
        (index3,name5) = wb2.new_sheet()

        self.assertEqual(name1,"first_sheet")
        self.assertEqual(name2,"Second Sheet")
        self.assertEqual(name3,"Sheet1")
        self.assertEqual(name5,"Sheet3")

        self.assertEqual(index1,0)
        self.assertEqual(index2,1)
        self.assertEqual(index3,2)


    def test_limited_punctuation(self): # allowed: .?!,:;!@#$%^&*()-_
        wb = sheets.Workbook()
        (_,_) = wb.new_sheet(". is the best")
        (_,_) = wb.new_sheet("@ is the best")
        (_,_) = wb.new_sheet("# is the best")
        (_,_) = wb.new_sheet("$ is the best")
        (_,_) = wb.new_sheet("& is the best")
        (_,_) = wb.new_sheet("_ is the best")
        with self.assertRaises(ValueError):
            (_,name) = wb.new_sheet("€ is the best")
        with self.assertRaises(ValueError):
            (_,name) = wb.new_sheet("' is the best")
        with self.assertRaises(ValueError):
            (_,name) = wb.new_sheet('" is the best')


    def test_white_space_in_sheet_name(self):
        wb = sheets.Workbook()
        with self.assertRaises(ValueError):
            (_,_) = wb.new_sheet(" first_sheet")
        with self.assertRaises(ValueError):
            (_,_) = wb.new_sheet("first_sheet ")


    def test_mistakes_in_cell_location(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, ' AA57', '12')
        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, 'A5A57', '12')


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

        self.assertEqual(content1, '12') 
        self.assertEqual(content2, '=10')
        self.assertEqual(content3, "'string")


    def test_leading_trailing_whitespace_cell_contents(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        wb.set_cell_contents(name1, 'AA57', 'Lots of space in the back      ')
        wb.set_cell_contents(name1, 'ba4', '        =54' )
        wb.set_cell_contents(name1, 'ba5', "      " )
        wb.set_cell_contents(name1, 'C23', "")

        content1 = wb.get_cell_contents("first_sheet", 'AA57')
        content2 = wb.get_cell_contents(name1, 'ba4')
        content3 = wb.get_cell_contents(name1, 'ba5')
        content4 = wb.get_cell_contents(name1, 'C23')

        self.assertEqual(content1, 'Lots of space in the back') 
        # TODO ^ not sure whether this must be a string or decimal.Decimal
        self.assertEqual(content2, '=54')
        self.assertEqual(content3, None)
        self.assertEqual(content4, None)


    def test_simple_formula_with_decimal(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        content = '=12+3-5'
        wb.set_cell_contents(name1, 'AA57', content)
        self.assertEqual(decimal.Decimal(12+3-5),wb.get_cell_value(name1, 'aa57'))

        content = '=12+3*(4+5)/4'
        wb.set_cell_contents(name1, 'ba43', content)
        self.assertEqual(decimal.Decimal(12+3*(4+5)/4),wb.get_cell_value(name1, 'ba43'))

        content = '=42*-4*-1'
        wb.set_cell_contents(name1, 'eee3', content)
        self.assertEqual(decimal.Decimal(42*-4*-1),wb.get_cell_value(name1, 'eee3'))


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


    def test_simple_cell_reference(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        (_, name2) = wb.new_sheet("second_sheet")

        wb.set_cell_contents(name1, 'AA57', '5')
        wb.set_cell_contents(name1, 'c4', '=aa57')
        wb.set_cell_contents(name2, 'c4', '=first_sheet!aa57')
        wb.set_cell_contents(name2, 'c5', "='first_sheet'!aa57")
        self.assertEqual(decimal.Decimal(5), wb.get_cell_value(name1, 'c4')) 
        self.assertEqual(decimal.Decimal(5), wb.get_cell_value(name2, 'c4')) 
        self.assertEqual(decimal.Decimal(5), wb.get_cell_value(name2, 'c5')) 


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
        # TODO add tets on when input into a cell is over bounds > ZZZZ


    def test_double_quotes_for_single_quotes(self):
        pass # TODO


    def delete_sheets(self):
        wb = sheets.Workbook()
        (_,_) = wb.new_sheet("first_sheet")
        (_,_) = wb.new_sheet("sheet_to_delete")
        (_,_) = wb.new_sheet("third_sheet")

        with self.assertRaises(KeyError):
            wb.del_sheet("invalid_sheet_name")

        wb.del_sheet("sheet_to_delete")
        self.assertEqual(wb.num_sheets, 2)
        wb.del_sheet("first_sheet")
        self.assertEqual(wb.num_sheets, 1)
        wb.del_sheet("third_sheet")
        self.assertEqual(wb.num_sheets, 0)


    def test_cell_errors(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'A4', '=9/0')
        value1 = wb.get_cell_value("first_sheet", 'A4')
        # print(list(wb.sheets[0].cells.values())[0].contents)
        # print("Expect divide by 0 error")
        # print(value1)

        wb.set_cell_contents(name1, 'B4', '=??????')
        value2 = wb.get_cell_value("first_sheet", 'B4')
        # print(list(wb.sheets[0].cells.values())[1].contents)
        # print("Expect parse error")
        # print(value2)


    def test_decimal(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        (_, name2) = wb.new_sheet("second_sheet")

        wb.set_cell_contents(name1, 'AA57', '12.0')
        wb.set_cell_contents(name1, 'AA58', '=aa57')
        wb.set_cell_contents("second_sheet", 'ba4', '=10' )
        wb.set_cell_contents("second_sheet", 'ba5', "'string" )

        content1 = wb.get_cell_value("first_sheet", 'AA57')
        content1a = wb.get_cell_value("first_sheet", 'AA58')
        content2 = wb.get_cell_value(name2, 'ba4')

        self.assertEqual(content1, decimal.Decimal(12)) 
        self.assertEqual(content1a, decimal.Decimal(12)) 
        self.assertEqual(content2, decimal.Decimal(10))


    def test_type_conversion(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'AA57', '12.0')
        wb.set_cell_contents(name1, 'AA58', "'123")
        wb.set_cell_contents(name1, 'AA59', "=aa57+aa58")

        self.assertEqual(decimal.Decimal(135), wb.get_cell_value(name1, 'aa59'))


    def test_string_concat(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'AA57', 'hello')
        wb.set_cell_contents(name1, 'AA58', "' world")
        wb.set_cell_contents(name1, 'aa59', '=aa57 & " world" & "!"')

        self.assertEqual('hello world!', wb.get_cell_value(name1, 'aa59'))

    
    """ implementing a test for trailing zeros with the decimals
    def test_decimal_trailing_zeros(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'AA57', '12.0')

        self.assertEqual('12', str(wb.get_cell_value(name1, 'aa57'))) """


if __name__ == '__main__':
    unittest.main(verbosity=0)