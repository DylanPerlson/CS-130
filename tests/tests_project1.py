import context
from sheets import *
import decimal
import unittest


class Project1(unittest.TestCase):
    def test_divide_by_zero(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("sheet")
        wb.set_cell_contents(name,'A1','=3/0')
        wb.set_cell_contents(name,'A4','=-A1')
        self.assertEqual(wb.get_cell_value(name,'A4').get_type(), CellErrorType.DIVIDE_BY_ZERO)
        self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.DIVIDE_BY_ZERO)
        wb.set_cell_contents(name,'A2','=3/A3')
        wb.set_cell_contents(name,'A3','0')
        wb.set_cell_contents(name,'A5','=2+A1')
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(),CellErrorType.DIVIDE_BY_ZERO)

        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.DIVIDE_BY_ZERO)

    def test_error_operations(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("sheet")
        wb.set_cell_contents(name,'A1','=4 + #REF!')
        wb.set_cell_contents(name,'A4','=4 / #REF!')
        self.assertEqual(wb.get_cell_value(name,'A4').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.BAD_REFERENCE)
        wb.set_cell_contents(name,'A2','=4 * #REF!')
        wb.set_cell_contents(name,'A3','=(#REF!)')
        wb.set_cell_contents(name,'A5','=4 - #REF!')
        wb.set_cell_contents(name,'A6','=+#REF!')
        wb.set_cell_contents(name,'A7','=#REF!')
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A3').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A7').get_type(),CellErrorType.BAD_REFERENCE)

    def test_error_operations_with_parentheses(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("sheet")
        wb.set_cell_contents(name,'A4','=4 / #ERROR!')
        self.assertEqual(wb.get_cell_value(name,'A4').get_type(),CellErrorType.PARSE_ERROR)

        wb.set_cell_contents(name,'A2','=4 * #CIRCREF!')
        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.CIRCULAR_REFERENCE)

        # wb.set_cell_contents(name,'A1','=#CIRCREF!')
        #wb.set_cell_contents(name,'A3','=A1')
        #wb.set_cell_contents(name,'A1','=A3')
        #wb.set_cell_contents(name,'A2','=-A1')
        #self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.CIRCULAR_REFERENCE)

        wb.set_cell_contents(name,'A1','=4 + #REF!')
        self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.BAD_REFERENCE)

        wb.set_cell_contents(name,'A3','= #NAME?')
        self.assertEqual(wb.get_cell_value(name,'A3').get_type(),CellErrorType.BAD_NAME)

        wb.set_cell_contents(name,'A5','=4 - #VALUE!')
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(),CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A6','=+#DIV/0!')
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(),CellErrorType.DIVIDE_BY_ZERO)

        # with parentheses
        wb.set_cell_contents(name,'A4','=4 / (#ERROR!)')
        self.assertEqual(wb.get_cell_value(name,'A4').get_type(),CellErrorType.PARSE_ERROR)

        wb.set_cell_contents(name,'A2','=4 * (#CIRCREF!)')
        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.CIRCULAR_REFERENCE)

        wb.set_cell_contents(name,'A1','=4 + (#REF!)')
        self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.BAD_REFERENCE)

        wb.set_cell_contents(name,'A3','= (#NAME?)')
        self.assertEqual(wb.get_cell_value(name,'A3').get_type(),CellErrorType.BAD_NAME)

        wb.set_cell_contents(name,'A5','= 4 - (#VALUE!)')
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(),CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A6','= +(#DIV/0!)')
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(),CellErrorType.DIVIDE_BY_ZERO)


    def test_parse_errors(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("sheet")
        wb.set_cell_contents(name,'A1','=3+')
        wb.set_cell_contents(name,'A4','=1+(2/1')
        self.assertEqual(wb.get_cell_value(name,'A4').get_type(),CellErrorType.PARSE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.PARSE_ERROR)
        wb.set_cell_contents(name,'A2','="Hello" & "World')
        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.PARSE_ERROR)

    def test_quoted_string(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name,'A1',"'100")
        wb.set_cell_contents(name,'A2','13.4')
        wb.set_cell_contents(name,'A3',"' this is a string")

        self.assertEqual(wb.get_cell_value(name,'A2'),decimal.Decimal('13.4'))
        self.assertEqual(wb.get_cell_value(name,'A1'),'100')
        self.assertEqual(wb.get_cell_contents(name,'A1'),"'100")
        self.assertEqual(wb.get_cell_value(name,'A3')," this is a string")

        wb.set_cell_contents(name,'A3',"'-13.3")
        self.assertEqual(wb.get_cell_value(name,'A3'),'-13.3')

    def test_unset_cells_return_None(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("first_sheet")
        self.assertEqual(wb.get_cell_value(name,'A1'),None)
        self.assertEqual(wb.get_cell_contents(name,'A1'),None)

    def test_empty_cells(self):
        """ Testing whether empty cells return 0 or ''. """
        wb = Workbook()
        (_, name) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name, 'a1', '=a2+2')
        wb.set_cell_contents(name,'B4','=A2+3')
        self.assertEqual(wb.get_cell_value(name,'B4'),3)
        wb.set_cell_contents(name,'B7','=A6&"hi"')
        self.assertEqual(wb.get_cell_value(name,'B7'),'hi')

    def test_bad_inputs(self):
        wb = Workbook()
        (_, name) = wb.new_sheet()

        wb.set_cell_contents(name, 'AA57', 'words')
        wb.set_cell_contents(name, 'AAA3', '=12+4')
        wb.set_cell_contents(name, 'JNE41', 'more words')

        with self.assertRaises(ValueError):
            wb.get_cell_contents(name, 'a 1')

        with self.assertRaises(ValueError):
            wb.get_cell_contents(name, 0)

        with self.assertRaises(ValueError):
            wb.get_cell_value(name, 'a 5')

        with self.assertRaises(ValueError):
            wb.get_cell_value(name, 5)

        with self.assertRaises(KeyError):
            wb.get_cell_contents('non_existing_sheet', 'a5')

    def test_set_none(self):
        wb = Workbook()
        (_, name) = wb.new_sheet()

        wb.set_cell_contents(name, 'AA57', 'words')
        self.assertEqual('words', wb.get_cell_contents(name, 'AA57'))

        wb.set_cell_contents(name, 'AA57', None)
        self.assertEqual(None, wb.get_cell_contents(name, 'AA57'))

    def test_decimal(self):
        wb = Workbook()
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
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'AA57', '12.0')
        wb.set_cell_contents(name1, 'AA58', "'123")
        wb.set_cell_contents(name1, 'AA59', "=aa57+aa58")

        self.assertEqual(decimal.Decimal(135), wb.get_cell_value(name1, 'aa59'))

    def test_string_concat(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'AA57', 'hello')
        wb.set_cell_contents(name1, 'AA58', "' world")
        wb.set_cell_contents(name1, 'aa59', '=aa57 & " world" & "!"')

        self.assertEqual('hello world!', wb.get_cell_value(name1, 'aa59'))

    # test based on the acceptance tests, but I don't fully understand
    def test_trailing_zeros_with_concat(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

    #     self.assertEqual('12', str(wb.get_cell_value(name1, 'aa57')))

        wb.set_cell_contents(name1, 'A3', '=5.0 & " should become 5"')
        self.assertEqual('5 should become 5', wb.get_cell_value(name1, 'A3'))

    def test_decimal_trailing_zeros(self):
        """ implementing a test for trailing zeros with the decimals """
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        wb.set_cell_contents(name1, 'AA57', '12.0')
        self.assertEqual('12', str(wb.get_cell_value(name1, 'aa57')))

        wb.set_cell_contents(name1, 'A1', '100')
        self.assertEqual('100', str(wb.get_cell_value(name1, 'A1')))

        wb.set_cell_contents(name1, 'A2', '1000.50')
        self.assertEqual('1000.5', str(wb.get_cell_value(name1, 'A2')))

        wb.set_cell_contents(name1, 'A3', '=12.0+1.00')
        self.assertEqual('13', str(wb.get_cell_value(name1, 'A3')))

    def test_limited_punctuation(self): # allowed: .?!,:;!@#$%^&*()-_
        wb = Workbook()
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

    def test_whitespace_in_sheet_name(self):
        wb = Workbook()
        with self.assertRaises(ValueError):
            (_,_) = wb.new_sheet(" first_sheet")
        with self.assertRaises(ValueError):
            (_,_) = wb.new_sheet("first_sheet ")

    def test_mistakes_in_cell_location(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, ' AA57', '12')
        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, 'A5A57', '12')

    def test_sheet_name_uniqueness(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        with self.assertRaises(ValueError):
            (_, name2) = wb.new_sheet("first_sheet")
        with self.assertRaises(ValueError):
            (_, name2) = wb.new_sheet("First_Sheet")

    def test_set_and_get_cell_contents(self):
        wb = Workbook()
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

        with self.assertRaises(ValueError):
            wb.get_cell_contents(name1, ' AA57')
        with self.assertRaises(ValueError):
            wb.get_cell_contents(name1, 'A5A57')

    def test_leading_whitespace(self):
        """Test that leading whitespace remains when using a leading quote."""

        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'A1', "'   three spaces")
        value = wb.get_cell_value(name1, 'A1')

        self.assertEqual(value, "   three spaces")

    def test_whitespace_cell_contents(self):
        """Test that leading and trailing whitespace is removed from contents."""
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        wb.set_cell_contents(name1, 'AA57', 'Lots of space in the back      ')
        wb.set_cell_contents(name1, 'ba4', '        =54' )
        wb.set_cell_contents(name1, 'ba5', "      " )
        wb.set_cell_contents(name1, 'C23', "")

        content1 = wb.get_cell_contents("first_sheet", 'AA57')
        content2 = wb.get_cell_contents(name1, 'ba4')
        content3 = wb.get_cell_contents(name1, 'ba5')
        value3 = wb.get_cell_value(name1, 'ba5')
        content4 = wb.get_cell_contents(name1, 'C23')

        self.assertEqual(content1, 'Lots of space in the back')
        self.assertEqual(content2, '=54')
        self.assertEqual(content3, None)
        # self.assertEqual(value3, None) # TODO empty cells issue; is 'None' instead of None
        self.assertEqual(content4, None)

    def test_simple_formula_with_decimal(self):
        wb = Workbook()
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

    def test_minus_address(self):
        wb = Workbook()
        (_, sheet) = wb.new_sheet()
        wb.set_cell_contents(sheet,'A1','=1')
        wb.set_cell_contents(sheet,'A2','=-A1')
        self.assertEqual(decimal.Decimal(-1), wb.get_cell_value(sheet, 'a2'))

    def test_max_sheet_size(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name1, 'ZZZZ9999', 'maximum')
        value1 = wb.get_cell_contents("first_sheet", 'ZZZZ9999')
        self.assertEqual(value1, 'maximum')

        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, 'ZZZZ10000', 'too many columns')
        with self.assertRaises(ValueError):
            wb.set_cell_contents(name1, 'AAAAA9999', 'too many rows')

    # TODO DTP
    # def test_bad_reference(self):
    #     wb = Workbook()
    #     (_, name1) = wb.new_sheet("first_sheet")
    #     wb.set_cell_contents(name1,'A1', '= ZZAZZ9999')
    #     print(wb.get_cell_value(name1,'A1'))
    #     #this should retrun bad reference, but is a value error


    def test_simple_cell_reference(self):
        wb = Workbook()
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
        wb = Workbook()
        (_, name) = wb.new_sheet("first_sheet")
        self.assertEqual((0,0),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'D14', 'something')
        self.assertEqual((4,14),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'Z3', 'something')
        self.assertEqual((26,14),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'AA20', 'something')
        self.assertEqual((27,20),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'AA20', None)
        self.assertEqual((26,14),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'Z3', None)
        self.assertEqual((4,14),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'D14', None)
        self.assertEqual((0,0),wb.get_sheet_extent(name))

        with self.assertRaises(ValueError):
            wb.get_cell_value(name,'ZZZZ99999')

    def test_naming_sheets_and_workbooks(self):
        wb1 = Workbook()
        wb2 = Workbook()
        (index1,name1) = wb1.new_sheet("first_sheet")
        (index2,name2) = wb1.new_sheet("Second Sheet")
        (_,_) = wb1.new_sheet("first_sheett")
        # (_,_) = wb1.new_sheet("first_sheett")
        (_,_) = wb1.new_sheet()
        (_,_) = wb1.new_sheet()
        (_,_) = wb1.new_sheet()
        (_,_) = wb1.new_sheet("Second Sheett")

        (_,name3)      = wb2.new_sheet()
        (_,_)          = wb2.new_sheet("Sheet2")
        (index3,name5) = wb2.new_sheet()

        self.assertEqual(name1,"first_sheet")
        self.assertEqual(name2,"Second Sheet")
        self.assertEqual(name3,"Sheet1")
        self.assertEqual(name5,"Sheet3")

    def test_double_quote_string(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh, 'A1', "'one quote: ''")
        content1 = wb.get_cell_value(sh, 'A1')

        self.assertEqual(content1, "one quote: '")

    def test_type_conversion(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh, 'A1', "'1")
        wb.set_cell_contents(sh, 'A2', "1")
        wb.set_cell_contents(sh, 'A3', "=A1+A2")

        self.assertEqual(wb.get_cell_value(sh, 'A3'), 2)

    def test_error_as_cell_value(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh, 'A1', '#REF!')

        self.assertEqual(wb.get_cell_value(sh,'A1').get_type(), CellErrorType.BAD_REFERENCE)

    def test_double_quote_literal(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'A1', "'one quote: ''")
        content1 = wb.get_cell_value(sh, 'A1')
        self.assertEqual(content1, "one quote: '")


if __name__ == '__main__':
    unittest.main(verbosity=1)