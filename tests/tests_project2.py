import context
from sheets import *
import decimal
import unittest


class Project2(unittest.TestCase):
    def test_reorder_workbook(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("first_sheet")
        (_, name2) = wb.new_sheet("second_sheet")
        (_, name3) = wb.new_sheet("move_to_second_sheet")

        wb.move_sheet(name3, 1)

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
        wb.rename_sheet('New_nAme','newName2')
        self.assertEqual('=newName2!A1+3',wb.get_cell_contents(name2,'A1'))

        #(_, name2) = wb.new_sheet("s3")
        #wb.set_cell_contents(name2,'A1',"='newName2'!A1 + 's3'!A1")
        #wb.rename_sheet('newName2','new?name')
        #self.assertEqual("='new?name'!A1 + s3!A1",wb.get_cell_contents(name2,'A1'))

        # wb.set_cell_contents(name2,'A1',"='new?name'!A1 + 's3'!A1")
        # wb.rename_sheet('new?name','3name')
        # self.assertEqual("='3name'!A1 + s3!A1",wb.get_cell_contents(name2,'A1'))

        with self.assertRaises(KeyError):
            wb.rename_sheet('foo','zoo')

        with self.assertRaises(ValueError):
            wb.rename_sheet('foo','')

    def test_save_workbook(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("fiRst_sheet")

        wb.set_cell_contents(name1, 'AA57', 'words')
        wb.set_cell_contents(name1, 'AAA3', '=12+4')
        wb.set_cell_contents(name1, 'JNE41', 'more words')

        (_, name2) = wb.new_sheet("2nd_sheet")

        wb.set_cell_contents(name2, 'aa57', '12.0')
        wb.set_cell_contents(name2, 'AAA3', '=12.0+1.00')
        wb.set_cell_contents(name2, 'JNE41', '100')

        with open('tests/json/save_testfile.json', 'w') as fp:
            wb.save_workbook(fp)

    def test_load_workbook(self):
        with open('tests/json/load_testfile.json') as fp:
            wb = Workbook.load_workbook(fp)

        self.assertEqual('words', str(wb.get_cell_value("first_sheet", 'AA57')))
        self.assertEqual(wb.get_cell_value("first_sheet",'AAB3').get_type(),CellErrorType.PARSE_ERROR)

    def test_json_non_string_contents(self):
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
        """ Test that a workbook with a single sheet and no contents
        is saved correctly. """
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



if __name__ == '__main__':
    unittest.main(verbosity=1)
