import os; os.system('cls')
import context
from sheets import *
import decimal
import unittest

#TODO add range check

class TestWorkbook(unittest.TestCase):
    def test_copy_cells(self):
            wb = Workbook()
            
            (_, name) = wb.new_sheet("s1")
            wb.set_cell_contents(name,'A1','1')
            wb.set_cell_contents(name,'A2',"hi")
            wb.set_cell_contents(name,'B2',"yo")
            wb.copy_cells(name,'A1','B3','A5')
            
            
            self.assertEqual(wb.get_cell_value(name,'A1'),1)
            self.assertEqual(wb.get_cell_value(name,'A5'),1)
            self.assertEqual(wb.get_cell_value(name,'A6'),"hi")
            self.assertEqual(wb.get_cell_value(name,'B6'),"yo")

            (_, name2) = wb.new_sheet("s2")
            wb.set_cell_contents(name2,'A1','1')
            wb.set_cell_contents(name2,'B2','1')
            wb.set_cell_contents(name2,'A2','=A1+B2+2')
            wb.set_cell_contents(name2,'A3','=A1+s1!B2')
            #wb.set_cell_contents(name2,'B3','=$A$1+2')
            wb.copy_cells(name2,'A1','B4','B3')

            #print(wb.get_cell_contents(name2,'B3'))
            self.assertEqual(wb.get_cell_contents(name2,'A3'),'=A1+s1!B2')
            self.assertEqual(wb.get_cell_contents(name2,'B4'),'=B3+C4+2')
            self.assertEqual(wb.get_cell_contents(name2,'B5'),'=B3+s1!B2')



            
    def test_move_cells(self):
            wb = Workbook()
            
            (_, name) = wb.new_sheet("s1")
            wb.set_cell_contents(name,'A1','1')
            wb.set_cell_contents(name,'A2',"hi")
            wb.set_cell_contents(name,'B2',"yo")
            wb.move_cells(name,'A1','B3','A5')
            
            
            self.assertEqual(wb.get_cell_value(name,'A1'),'None')
            self.assertEqual(wb.get_cell_value(name,'A5'),1)
            self.assertEqual(wb.get_cell_value(name,'A6'),"hi")
            self.assertEqual(wb.get_cell_value(name,'B6'),"yo")

            (_, name2) = wb.new_sheet("s2")
            wb.set_cell_contents(name2,'A1','1')
            wb.set_cell_contents(name2,'B2','1')
            wb.set_cell_contents(name2,'A2','=A1+B2+2')
            wb.set_cell_contents(name2,'A3','=A1+s1!B2')
            wb.move_cells(name2,'A1','B4','B3')
            self.assertEqual(wb.get_cell_contents(name2,'B4'),'=B3+C4+2')
            self.assertEqual(wb.get_cell_contents(name2,'B5'),'=B3+s1!B2')
            
    
    pause = True
    if not pause:

        def test_aaron(self):
            wb = Workbook()
            (_, name) = wb.new_sheet("s1")
            wb.set_cell_contents(name,'A1','1')
            wb.set_cell_contents(name,'A2',"hi")
            wb.set_cell_contents(name,'A3',"=A1 + 2")
            wb.set_cell_contents(name,'A1','2')

        def test_reorder_workbook(self):
            wb = Workbook()    
            (_, name1) = wb.new_sheet("first_sheet")
            (_, name2) = wb.new_sheet("second_sheet")
            (_, name3) = wb.new_sheet("move_to_second_sheet")

            wb.reorder_sheets(name3, 1)
            
            self.assertEqual(wb.sheets[1].sheet_name, "move_to_second_sheet")
            self.assertEqual(wb.sheets[2].sheet_name, "second_sheet")
            self.assertEqual(3,len(wb.sheets))
        
        def test_copy(self):
            wb = Workbook()    
            
            (_, name1) = wb.new_sheet("first_sheet")
            (_, name2) = wb.new_sheet("second_sheet")
            wb.set_cell_contents(name1,'A1','1')
            wb.copy_sheet(name1)
            
            self.assertEqual(3,len(wb.sheets))
            self.assertEqual(wb.sheets[0].cells.keys(),wb.sheets[2].cells.keys())

        def test_rename(self):
            wb = Workbook()
            (_, name1) = wb.new_sheet("s1")
            (_, name2) = wb.new_sheet("s2")
            wb.set_cell_contents(name2,'A1',"=s1!A1+3")
            wb.rename_sheet('S1','new_name')
            self.assertEqual('new_name',wb.sheets[0].sheet_name)
            self.assertEqual('=new_name!A1+3',wb.get_cell_contents(name2,'A1'))
            
            wb.set_cell_contents(name2,'A1',"='new_name'!A1+3")
            wb.rename_sheet('New_nAme','new_name2')
            self.assertEqual('=new_name2!A1+3',wb.get_cell_contents(name2,'A1'))
        
            (_, name2) = wb.new_sheet("s3")
            wb.set_cell_contents(name2,'A1',"='new_name2'!A1 + 's3'!A1")
            wb.rename_sheet('new_name2','new?name')
            self.assertEqual("='new?name'!A1 + s3!A1",wb.get_cell_contents(name2,'A1'))
            
            wb.set_cell_contents(name2,'A1',"='new?name'!A1 + 's3'!A1")
            wb.rename_sheet('new?name','3name')
            self.assertEqual("='3name'!A1 + s3!A1",wb.get_cell_contents(name2,'A1'))
            

            with self.assertRaises(KeyError):
                wb.rename_sheet('foo','zoo')

            with self.assertRaises(ValueError):
                wb.rename_sheet('foo','')
            # normal replace and uneccesary '' works no, do errors and other req work now?
            
        


        
        """ Performing unit tests on the sheets module. """
        
        # def test_set_cell_as_error(self):
        #     wb = Workbook()    
        #     (_, name) = wb.new_sheet("sheet")
        #     a = CellError(CellErrorType.)
        

        #def test_bad_ref(self):
            #wb = Workbook()    
            #(_, name) = wb.new_sheet("sheet")
            #print(wb.get_cell_value('name','A1'))


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
            
            #print(wb.get_cell_value(name,'A1') is CellError(CellErrorType.DIVIDE_BY_ZERO, "division by zero", ZeroDivisionError))


        # def test_string_errors(self):
        #     wb = Workbook()    
        #     (_, name) = wb.new_sheet("sheet")
        #     wb.set_cell_contents(name,'A1',3/0)
        #     print(wb.get_cell_contents(name,'A1'))
            

            #with self.assertRaises(CellErrorType.PARSE_ERROR):
                #wb.set_cell_contents(name,'A1',"='hi'+3")


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
        
        def test_parse_errors(self):
            wb = Workbook()    
            (_, name) = wb.new_sheet("sheet")
            wb.set_cell_contents(name,'A1','=3+')   
            wb.set_cell_contents(name,'A4','=1+(2/1')
            self.assertEqual(wb.get_cell_value(name,'A4').get_type(),CellErrorType.PARSE_ERROR)  
            self.assertEqual(wb.get_cell_value(name,'A1').get_type(), CellErrorType.PARSE_ERROR)
            wb.set_cell_contents(name,'A2','="Hello" & "World')
            self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.PARSE_ERROR)


        # def test_set_error_cells(self):
        #     wb = Workbook()    
        #     (_, name) = wb.new_sheet("sheet")
        #     wb.set_cell_contents(name,'A1','#ERROR!')   
        #     wb.set_cell_contents(name,'A4','#CIRCREF!')
        #     self.assertEqual(wb.get_cell_value(name,'A4'), CellErrorType.CIRCULAR_REFERENCE)  
        #     self.assertEqual(wb.get_cell_value(name,'A1'), CellErrorType.PARSE_ERROR)
        #     wb.set_cell_contents(name,'A2','REF!')
        #     self.assertEqual(wb.get_cell_value(name,'A2'),CellErrorType.BAD_REFERENCE)

        
    

        def test_string_comes_back_as_decimal(self): 
            wb = Workbook()    
            (_, name) = wb.new_sheet("first_sheet")
            wb.set_cell_contents(name,'A1',"'100")
            wb.set_cell_contents(name,'A2','13.4')
            
            self.assertEqual(wb.get_cell_value(name,'A2'),decimal.Decimal('13.4'))
            self.assertEqual(wb.get_cell_value(name,'A1'),decimal.Decimal('100'))
            self.assertEqual(wb.get_cell_contents(name,'A1'),"'100")

            wb.set_cell_contents(name,'A3',"'-13.3")
            self.assertEqual(wb.get_cell_value(name,'A3'),decimal.Decimal('-13.3'))

            
        def test_unset_cells_return_None(self): 
            wb = Workbook()    
            (_, name) = wb.new_sheet("first_sheet")
            self.assertEqual(wb.get_cell_value(name,'A1'),None)
            self.assertEqual(wb.get_cell_contents(name,'A1'),None)
            
            
        def test_empty_cells(self):
            """ Testing whether empty cells return 0 or ''. """   
            wb = Workbook()
            (_, name) = wb.new_sheet("first_sheet")
            wb.set_cell_contents(name,'B4','=A2+3')
            self.assertEqual(wb.get_cell_value(name,'B4'),3)
            wb.set_cell_contents(name,'B7','=A6&"hi"')
            self.assertEqual(wb.get_cell_value(name,'B7'),'hi')


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

            # print(wb1.list_sheets())

            self.assertEqual(name1,"first_sheet")
            self.assertEqual(name2,"Second Sheet")
            self.assertEqual(name3,"Sheet1")
            self.assertEqual(name5,"Sheet3")

            with open('tests/json/save_testfile.json', 'w') as fp:
                wb1.save_workbook(fp)


        def test_load_workbook(self):
            with open('tests/json/load_testfile.json') as fp:
                wb = Workbook.load_workbook(fp)

            self.assertEqual('words', str(wb.get_cell_value("first_sheet", 'AA57')))
            self.assertEqual(wb.get_cell_value("first_sheet",'AAB3').get_type(),CellErrorType.PARSE_ERROR)  


        def test_json_non_string_contents(self): # TODO seems to work
            with self.assertRaises(TypeError):
                with open('tests/json/error1_testfile.json') as fp:
                    wb = Workbook.load_workbook(fp)


        def test_empty_json(self):
            with open('tests/json/empty_testfile.json') as fp:
                wb = Workbook.load_workbook(fp)

            self.assertEqual([], wb.list_sheets())
            self.assertEqual(0, wb.num_sheets())


        def test_sheetlist_json(self):
            with self.assertRaises(TypeError):
                with open('tests/json/sheetlist_testfile.json') as fp:
                    wb = Workbook.load_workbook(fp)


        def test_json_no_contents(self):
            ''' Test that a workbook with a single sheet and no contents
            is saved correctly. '''
            with open('tests/json/no_contents_testfile.json') as fp:
                wb = Workbook.load_workbook(fp)

            self.assertEqual(['first_sheet'], wb.list_sheets())
            self.assertEqual(1, wb.num_sheets())


        def test_json_perserve_capitalization(self):
            wb = Workbook()
            (_, name1) = wb.new_sheet("fiRst_sheet")
            (_,_) = wb.new_sheet("second_sheet")
            (_,_) = wb.new_sheet("LAST_sheet")

            wb.set_cell_contents(name1, 'AA57', 'words')
            wb.set_cell_contents(name1, 'AAA3', '=12+4')
            wb.set_cell_contents(name1, 'JNE41', 'more words')

            (_, name1) = wb.new_sheet("2nd_sheet")

            wb.set_cell_contents(name1, 'aa57', '12.0')
            wb.set_cell_contents(name1, 'AAA3', '=12.0+1.00')
            wb.set_cell_contents(name1, 'JNE41', '100')

            listed_sheets = wb.list_sheets()

            with open('tests/json/capitalization_testfile.json', 'w') as fp:
                wb.save_workbook(fp)

            with open('tests/json/capitalization_testfile.json') as fp:
                wb2 = Workbook.load_workbook(fp)

            self.assertEqual(listed_sheets, wb2.list_sheets())


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

            with self.assertRaises(KeyError):
                wb.get_cell_contents('non_existing_sheet', 'a5')


        def test_set_none(self):
            wb = Workbook()
            (_, name) = wb.new_sheet()

            wb.set_cell_contents(name, 'AA57', 'words')
            self.assertEqual('words', wb.get_cell_contents(name, 'AA57'))

            wb.set_cell_contents(name, 'AA57', None)
            self.assertEqual(None, wb.get_cell_contents(name, 'AA57'))


        def test_loading_bad_formula(self): # TODO
            pass
        
if __name__ == '__main__':
    # print('------------------------NEW TEST------------------------')
    unittest.main(verbosity=0)
        

