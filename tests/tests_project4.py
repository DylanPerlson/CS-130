import context
from sheets import *
import decimal
import unittest
from sheets import version
from sheets import cell


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

    def test_version_func(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()
        wb.set_cell_contents(sh,'A1','=VERSION()')

        self.assertEqual(version, wb.get_cell_value(sh, 'A1'))

    def test_choose_func(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'B1', '5.5')
        wb.set_cell_contents(sh, 'B2', 'true')
        wb.set_cell_contents(sh, 'B3', '=False')

        wb.set_cell_contents(sh,'A1','=CHOOSE(1,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(1.5, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,2.5,true,  false  , B1, B2, B3, "last")+1')
        self.assertEqual(3.5, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(3,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(True, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(4,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(5,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(5.5, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(6,1.5,#REF!,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(True, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(7,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh,'A1','=CHOOSE(8,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual('last', wb.get_cell_value(sh, 'A1'))

        # test errors

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,#ERROR!,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(CellErrorType.PARSE_ERROR, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,#REF!,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(CellErrorType.BAD_REFERENCE, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,#NAME?,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(CellErrorType.BAD_NAME, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,(1/0),true,  false  , B1, B2, B3, "last")')
        self.assertEqual(CellErrorType.DIVIDE_BY_ZERO, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh, 'B1', '=1/0')
        wb.set_cell_contents(sh,'A1','=CHOOSE(5,1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(CellErrorType.DIVIDE_BY_ZERO, wb.get_cell_value(sh, 'A1').get_type())

    def test_isblank_func(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'B1', '=5')

        wb.set_cell_contents(sh, 'A1', '=ISBLANK()')
        self.assertEqual(CellErrorType.TYPE_ERROR, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh, 'A1', '=ISBLANK(1,1)')
        self.assertEqual(CellErrorType.TYPE_ERROR, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh, 'A1', '=ISBLANK(B1)')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'A1', '=ISBLANK(B2)')
        self.assertEqual(True, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'A1', '=ISBLANK(0)')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'A1', '=ISBLANK(False)')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'A1', '=ISBLANK("")')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

    def test_if_func(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'a1', '=IF(true, 5)')
        self.assertEqual(5, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IF(false, 5)')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IF(true, 5, 4)')
        self.assertEqual(5, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IF(false, 5, 4)')
        self.assertEqual(4, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IF(false, 5, "abc")')
        self.assertEqual('abc', wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IF("something else", 5, "abc")')
        self.assertEqual(CellErrorType.TYPE_ERROR, wb.get_cell_value(sh, 'A1').get_type())

    def test_iferror_func(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'a1', '=IFERROR(true, 5)')
        self.assertEqual(True, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IFERROR(#REF!, 5)')
        self.assertEqual(5, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IFERROR(#NAME?)')
        self.assertEqual('', wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=IFERROR("something", 4)')
        self.assertEqual('something', wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'B1', '=1/0')
        wb.set_cell_contents(sh, 'a1', '=IFERROR(B1, "abc")')
        self.assertEqual('abc', wb.get_cell_value(sh, 'A1'))

    def test_iserror_func(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'a1', '=ISERROR(true)')
        self.assertEqual(False, wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'a1', '=ISERROR(#REF!)')
        self.assertEqual(True, wb.get_cell_value(sh, 'A1'))


if __name__ == '__main__':
    unittest.main(verbosity=1)
