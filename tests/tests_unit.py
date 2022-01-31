import os; os.system('cls')
import context
from sheets import *
import unittest


class TestWorkbook(unittest.TestCase):
    def test_rename(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("s1")
        (_, name2) = wb.new_sheet("s2")
        wb.set_cell_contents(name2,'A1',"=s1!A1+3")
        wb.rename_sheet('s1','new_name')
        self.assertEqual('new_name',wb.sheets[0].sheet_name)
        self.assertEqual('=new_name!A1+3',wb.get_cell_contents(name2,'A1'))
        
        wb.set_cell_contents(name2,'A1',"='new_name'!A1+3")
        wb.rename_sheet('new_name','new_name2')
        self.assertEqual('=new_name2!A1+3',wb.get_cell_contents(name2,'A1'))
       
        (_, name2) = wb.new_sheet("s3")
        wb.set_cell_contents(name2,'A1',"='new_name2'!A1 + 's3'!A1")
        wb.rename_sheet('new_name2','new name')
        self.assertEqual("='new name'!A1 + s3!A1",wb.get_cell_contents(name2,'A1'))
        
        # normal replace and uneccesary '' works no, do errors and other req work now?
        
     


    
    """ Performing unit tests on the sheets module. """
    '''
    def test_set_cell_as_error(self):
        wb = sheets.Workbook()    
        (_, name) = wb.new_sheet("sheet")
        a = CellError(CellErrorType.)
    '''

    #def test_bad_ref(self):
        #wb = sheets.Workbook()    
        #(_, name) = wb.new_sheet("sheet")
        #print(wb.get_cell_value('name','A1'))
    def test_divide_by_zero(self):
        wb = sheets.Workbook()    
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
        
        #print(wb.get_cell_value(name,'A1') is CellError(CellErrorType.DIVIDE_BY_ZERO, "division by zero", ZeroDivisionError))
    # def test_string_errors(self):
    #     wb = sheets.Workbook()    
    #     (_, name) = wb.new_sheet("sheet")
    #     wb.set_cell_contents(name,'A1',3/0)
    #     print(wb.get_cell_contents(name,'A1'))
        

        #with self.assertRaises(CellErrorType.PARSE_ERROR):
            #wb.set_cell_contents(name,'A1',"='hi'+3")
    def test_error_operations(self):
        wb = sheets.Workbook()    
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
    
    def test_parse_errors(self):
        wb = sheets.Workbook()    
        (_, name) = wb.new_sheet("sheet")
        wb.set_cell_contents(name,'A1','=3+')   
        wb.set_cell_contents(name,'A4','=1+(2/1')
        self.assertEqual(wb.get_cell_value(name,'A4').get_type(),CellErrorType.PARSE_ERROR)  
        self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.PARSE_ERROR)
        wb.set_cell_contents(name,'A2','="Hello" & "World')
        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.PARSE_ERROR)

    # def test_set_error_cells(self):
    #     wb = sheets.Workbook()    
    #     (_, name) = wb.new_sheet("sheet")
    #     wb.set_cell_contents(name,'A1','#ERROR!')   
    #     wb.set_cell_contents(name,'A4','#CIRCREF!')
    #     self.assertEqual(wb.get_cell_value(name,'A4'), CellErrorType.CIRCULAR_REFERENCE)  
    #     self.assertEqual(wb.get_cell_value(name,'A1'), CellErrorType.PARSE_ERROR)
    #     wb.set_cell_contents(name,'A2','REF!')
    #     self.assertEqual(wb.get_cell_value(name,'A2'),CellErrorType.BAD_REFERENCE)
 
    def test_string_comes_back_as_decimal(self): 
        wb = sheets.Workbook()    
        (_, name) = wb.new_sheet("first_sheet")
        wb.set_cell_contents(name,'A1',"'100")
        wb.set_cell_contents(name,'A2','13.4')
        
        self.assertEqual(wb.get_cell_value(name,'A2'),decimal.Decimal('13.4'))
        self.assertEqual(wb.get_cell_value(name,'A1'),decimal.Decimal('100'))
        self.assertEqual(wb.get_cell_contents(name,'A1'),"'100")

        wb.set_cell_contents(name,'A3',"'-13.3")
        self.assertEqual(wb.get_cell_value(name,'A3'),decimal.Decimal('-13.3'))

        
    def test_unset_cells_return_None(self): 
        wb = sheets.Workbook()    
        (_, name) = wb.new_sheet("first_sheet")
        self.assertEqual(wb.get_cell_value(name,'A1'),None)
        self.assertEqual(wb.get_cell_contents(name,'A1'),None)
        
         
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
        (_,_) = wb1.new_sheet("first_sheett")
        # (_,_) = wb1.new_sheet("first_sheett")
        (_,_) = wb1.new_sheet()
        (_,_) = wb1.new_sheet()
        (_,_) = wb1.new_sheet()
        (_,_) = wb1.new_sheet("Second Sheett")

        (_,name3)      = wb2.new_sheet()
        (_,_)          = wb2.new_sheet("Sheet2")
        (index3,name5) = wb2.new_sheet()

        # print(wb1.list_sheets())

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


    def test_whitespace_in_sheet_name(self):
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

        with self.assertRaises(ValueError):
            wb.get_cell_contents(name1, ' AA57')
        with self.assertRaises(ValueError):
            wb.get_cell_contents(name1, 'A5A57')


    def test_whitespace_cell_contents(self):
        """ test that leading and trailing whitespace is removed from contents """
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

        wb.set_cell_contents(name, 'AA20', None)
        self.assertEqual((26,14),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'Z3', None)
        self.assertEqual((4,14),wb.get_sheet_extent(name))

        wb.set_cell_contents(name, 'D14', None)
        self.assertEqual((0,0),wb.get_sheet_extent(name))

        self.assertEqual(wb.get_cell_value(name,'ZZZZ99999').get_type(),CellErrorType.BAD_REFERENCE)



    def test_double_quotes_for_single_quotes(self):
        pass # TODO

    def test_delete_sheets(self):
        wb = sheets.Workbook()
        (_,_) = wb.new_sheet("first_sheet")
        (_,_) = wb.new_sheet("sheet_to_delete")
        (_,_) = wb.new_sheet("third_sheet")

        with self.assertRaises(KeyError):
            wb.del_sheet("invalid_sheet_name")

        wb.del_sheet("sheet_to_delete")
        self.assertEqual(wb.num_sheets, 2)
        self.assertEqual(wb.list_sheets(),['first_sheet', 'third_sheet'])
        wb.del_sheet("first_sheet")
        self.assertEqual(wb.num_sheets, 1)
        self.assertEqual(wb.list_sheets(),['third_sheet'])

        (_,_) = wb.new_sheet("one_last_sheet")
        self.assertEqual(wb.list_sheets(),['third_sheet',"one_last_sheet"])

        wb.del_sheet("one_last_sheet")
        wb.del_sheet("third_sheet")
        self.assertEqual(wb.num_sheets, 0)
        self.assertEqual(wb.list_sheets(),[])
    

    # def test_cell_errors(self): #make this a better parse error
    #     wb = sheets.Workbook()
    #     (_, name1) = wb.new_sheet("first_sheet")
    
    #     wb.set_cell_contents(name1, 'B4', '=9/0')
    #     value1 = wb.get_cell_value("first_sheet", 'B4')
    #     print(list(wb.sheets[0].cells.values())[0].contents)
    #     print("Expect divide by 0 errors")
    #     print(value1)

    #     wb.set_cell_contents(name1, 'C4', '=5+')
    #     value3 = wb.get_cell_value("first_sheet", 'C4')
    #     print(list(wb.sheets[0].cells.values())[1].contents)
    #     print("Expect parse error")
    #     print(value3)

    #     wb.set_cell_contents(name1, 'D4', '=second_sheet!A4 + 1')
    #     value4 = wb.get_cell_value("first_sheet", 'D4')
    #     print(list(wb.sheets[0].cells.values())[2].contents)
    #     print("Expect bad reference error")
    #     print(value4)

    #     wb.set_cell_contents(name1, 'E4', '="Hello"+1')
    #     value5 = wb.get_cell_value("first_sheet", 'E4')
    #     print(list(wb.sheets[0].cells.values())[3].contents)
    #     print("Expect type error")
    #     print(value5)

        # wb.set_cell_contents(name1, 'B4', '=5>3')
        # value6 = wb.get_cell_value("first_sheet", 'B4')
        # print(list(wb.sheets[0].cells.values())[5].contents)
        # print("Expect name error")
        # print(value6)

        #Edge case that has to prioritize errors
    
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


    # test based on the acceptance tests, but I don't fully understand
    def test_trailing_zeros_with_concat(self):
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

    #     self.assertEqual('12', str(wb.get_cell_value(name1, 'aa57')))
    
        wb.set_cell_contents(name1, 'A3', '=5.0 & " should become 5"')
        self.assertEqual('5 should become 5', wb.get_cell_value(name1, 'A3'))

    
    """ implementing a test for 'from sheets import *'
    def test_from_import(self):
        import sys
        from sheets import *
        
        self.assertTrue('Workbook' in sys.modules) """


    def test_decimal_trailing_zeros(self):
        """ implementing a test for trailing zeros with the decimals """
        wb = sheets.Workbook()
        (_, name1) = wb.new_sheet("first_sheet")

        wb.set_cell_contents(name1, 'AA57', '12.0')
        self.assertEqual('12', str(wb.get_cell_value(name1, 'aa57')))
    
        wb.set_cell_contents(name1, 'A1', '100')
        self.assertEqual('100', str(wb.get_cell_value(name1, 'A1')))
    
        wb.set_cell_contents(name1, 'A2', '1000.50')
        self.assertEqual('1000.5', str(wb.get_cell_value(name1, 'A2')))
    
        wb.set_cell_contents(name1, 'A3', '=12.0+1.00')
        self.assertEqual('13', str(wb.get_cell_value(name1, 'A3')))
    
    
if __name__ == '__main__':
    print('------------------------NEW TEST------------------------')
    unittest.main(verbosity=0)
        

