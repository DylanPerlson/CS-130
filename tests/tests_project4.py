import context
from sheets import *
import decimal
import unittest
from sheets import version
from sheets import cell

import os; os.system('clear')

class Project4(unittest.TestCase):
    def test_lark_bool_lit(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'a1', '=true')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', 'FaLse')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

    def test_bool_oper(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()

        # stuff that should be True

        wb.set_cell_contents(sh, 'a1', '=true')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="5"=5')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=5=5')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="e" = "e"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="e" == "E"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=False <> "False"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '=false < true')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="BLUE" = "blue"')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        wb.set_cell_contents(sh, 'a1', '="12" > 12')
        self.assertEqual(True, wb.get_cell_value(sh, 'a1'))

        # stuff that should be False

        wb.set_cell_contents(sh, 'a1', '=true = "True"')
        self.assertEqual(False, wb.get_cell_value(sh, 'a1'))

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

    def test_and(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=AND(true, false)")
        wb.set_cell_contents(name,'A4',"=AND(1, true)")
        wb.set_cell_contents(name,'A5',"=AND(false, false)")
        wb.set_cell_contents(name,'A6',"=AND(0, true)")
        wb.set_cell_contents(name,'A7',"=AND(false)")
        wb.set_cell_contents(name,'A8',"=AND()")
        wb.set_cell_contents(name,'A9',"=AND(false, 10, false)")
        wb.set_cell_contents(name,'A10',"=AND(true, true, true, true)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), False)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)
        self.assertEqual(wb.get_cell_value(name, 'A6'), False)
        self.assertEqual(wb.get_cell_value(name, 'A7'), False)
        self.assertEqual(wb.get_cell_value(name, 'A8').get_type(), CellErrorType.TYPE_ERROR)
        self.assertEqual(wb.get_cell_value(name, 'A9'), False)
        self.assertEqual(wb.get_cell_value(name, 'A10'), True)

        wb.set_cell_contents(name,'A10','=AND("string")')
        self.assertEqual(wb.get_cell_value(name, 'A10').get_type(), CellErrorType.TYPE_ERROR)


    def test_or(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=OR(true, false)")
        wb.set_cell_contents(name,'A4',"=OR(true, 10)")
        wb.set_cell_contents(name,'A5',"=OR(false, false)")
        wb.set_cell_contents(name,'A6',"=OR(0, true)")
        wb.set_cell_contents(name,'A7',"=OR(false)")
        wb.set_cell_contents(name,'A8',"=OR()")
        wb.set_cell_contents(name,'A9',"=OR(false, true, false)")
        wb.set_cell_contents(name,'A10',"=OR(true, true, true, 1)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), True)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)
        self.assertEqual(wb.get_cell_value(name, 'A6'), True)
        self.assertEqual(wb.get_cell_value(name, 'A7'), False)
        self.assertEqual(wb.get_cell_value(name, 'A8').get_type(), CellErrorType.TYPE_ERROR)
        self.assertEqual(wb.get_cell_value(name, 'A9'), True)
        self.assertEqual(wb.get_cell_value(name, 'A10'), True)

        wb.set_cell_contents(name,'A10','=OR("string", true)')
        self.assertEqual(wb.get_cell_value(name, 'A10').get_type(), CellErrorType.TYPE_ERROR)

    def test_not(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=NOT(true)")
        self.assertEqual(wb.get_cell_value(name, 'A3'), False)

        wb.set_cell_contents(name,'A4',"=NOT(false)")
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)

        wb.set_cell_contents(name,'A4','=NOT("string")')
        self.assertEqual(wb.get_cell_value(name, 'A4').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A4',"=NOT(false)")
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)

    def test_exact(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3','=EXACT("hello", "HELLO")')
        wb.set_cell_contents(name,'A4','=EXACT("Hello","Hello")')
        wb.set_cell_contents(name,'A5','=EXACT("Hello", "hElLo")')

        self.assertEqual(wb.get_cell_value(name, 'A3'), False)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)

    def test_error_priority(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2','=#ERROR! * #REF!')
        wb.set_cell_contents(name,'A3','=#REF! * #ERROR!')
        wb.set_cell_contents(name,'A5','=#REF! + #NAME?')
        wb.set_cell_contents(name,'A6','=#DIV/0! + #VALUE!')
        wb.set_cell_contents(name,'A7','=#VALUE! & #ERROR!')


        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.PARSE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A3').get_type(),CellErrorType.PARSE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(),CellErrorType.TYPE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A7').get_type(),CellErrorType.PARSE_ERROR)

    def test_mixed(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2','6')
        wb.set_cell_contents(name,'B1','1')
        wb.set_cell_contents(name,'C1','1')
        wb.set_cell_contents(name,'D1','14')
        wb.set_cell_contents(name, 'E1', '=OR(AND(A1 > 5, B1 < 2), AND(C1 < 6, D1 = 14))')

        self.assertEqual(wb.get_cell_value(name, 'E1'), True)

    def test_xor(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=XOR(True, False)")
        self.assertEqual(wb.get_cell_value(name, 'A3'), True)

        wb.set_cell_contents(name,'A4',"=XOR(True, True)")
        self.assertEqual(wb.get_cell_value(name, 'A4'), False)

        wb.set_cell_contents(name,'A5',"=XOR(False, False)")
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)

        wb.set_cell_contents(name,'A6',"=XOR(False, True)")
        self.assertEqual(wb.get_cell_value(name, 'A6'), True)

        wb.set_cell_contents(name,'A7',"=XOR(False)")
        self.assertEqual(wb.get_cell_value(name, 'A7'), False)

        wb.set_cell_contents(name,'A8','=XOR("something")')
        self.assertEqual(wb.get_cell_value(name, 'A8').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A8','=XOR(4,3)')
        self.assertEqual(wb.get_cell_value(name, 'A8'), False)

        wb.set_cell_contents(name,'A8','=XOR(4,3,0,1)')
        self.assertEqual(wb.get_cell_value(name, 'A8'), True)

        wb.set_cell_contents(name,'A8',"=XOR(0,1,1,0)")
        self.assertEqual(wb.get_cell_value(name, 'A8'), False)

        wb.set_cell_contents(name,'A9',"=XOR(False, True, False)")
        self.assertEqual(wb.get_cell_value(name, 'A9'), True)

        wb.set_cell_contents(name,'A10',"=XOR(True, False, True, False, True, True)")
        self.assertEqual(wb.get_cell_value(name, 'A10'), False)

        wb.set_cell_contents(name,'A10',"=XOR(True, True, False, True, True)")
        self.assertEqual(wb.get_cell_value(name, 'A10'), False)

        wb.set_cell_contents(name,'A10',"=XOR(False, False, False, False, False, True)")
        self.assertEqual(wb.get_cell_value(name, 'A10'), True)

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

    def test_choose_func_edgecase(self):
        wb = Workbook()
        (_, sh) = wb.new_sheet()

        wb.set_cell_contents(sh, 'B1', '5.5')
        wb.set_cell_contents(sh, 'B2', 'true')
        wb.set_cell_contents(sh, 'B3', '=False')

        wb.set_cell_contents(sh,'A1','=EXACT(1,"1")')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), True)

        wb.set_cell_contents(sh,'A1','=CHOOSE("string",1.5,2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(wb.get_cell_value(sh, 'A1').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(sh,'A1','=CHOOSE(2,1.5,-2.5,true,  false  , B1, B2, B3, "last")')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), -2.5)

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

    def test_indirect_func(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()
        (_,sh2) = wb.new_sheet()

        wb.set_cell_contents(sh, 'B1', '=3')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B1")')
        self.assertEqual(wb.get_cell_value(sh, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'B1', '=true')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B1")')
        self.assertEqual(wb.get_cell_value(sh, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'B1', '=1+2')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B1")')
        self.assertEqual(wb.get_cell_value(sh, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'B1', '=AND(true,false)')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B1")')
        self.assertEqual(wb.get_cell_value(sh, 'B1'), wb.get_cell_value(sh, 'A1'))

        # referring to a different sheet

        wb.set_cell_contents(sh2, 'B1', '=AND(true,false)')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("' + sh2 + '!B1")')
        self.assertEqual(wb.get_cell_value(sh2, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh2, 'B1', '=CHOOSE(3, 1, 2, 3)')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("' + sh2 + '!B1")')
        self.assertEqual(wb.get_cell_value(sh2, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh2, 'B1', '="something"')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("' + sh2 + '!B1")')
        self.assertEqual(wb.get_cell_value(sh2, 'B1'), wb.get_cell_value(sh, 'A1'))

        # errors

        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B2")')
        self.assertEqual(CellErrorType.BAD_REFERENCE, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh2, 'B1', '=CHOOSE(3, 1, 2, 3)')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("' + sh2 + '!B2")')
        self.assertEqual(CellErrorType.BAD_REFERENCE, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh, 'A1', '=INDIRECT("something")')
        self.assertEqual(CellErrorType.BAD_REFERENCE, wb.get_cell_value(sh, 'A1').get_type())

        wb.set_cell_contents(sh, 'A1', '=INDIRECT("true")')
        self.assertEqual(CellErrorType.BAD_REFERENCE, wb.get_cell_value(sh, 'A1').get_type())

        # edge cases

        wb.set_cell_contents(sh, 'B1', '=4')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B1")')
        self.assertEqual(wb.get_cell_value(sh, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'B1', '=4')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT(B1)')
        self.assertEqual(wb.get_cell_value(sh, 'B1'), wb.get_cell_value(sh, 'A1'))

        wb.set_cell_contents(sh, 'A1', '=EXACT(#REF!,#ERROR!)')
        self.assertEqual(CellErrorType.PARSE_ERROR, wb.get_cell_value(sh, 'A1').get_type())

    def test_indirect_func2(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')
        (_,sh2) = wb.new_sheet()

        wb.set_cell_contents(sh, 'B1', '=3')
        wb.set_cell_contents(sh, 'A1', '=INDIRECT("sheet!B1")')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), wb.get_cell_value(sh, 'B1'))

        wb.set_cell_contents(sh, 'A1', '=INDIRECT("B2")')
        self.assertEqual(CellErrorType.BAD_REFERENCE, wb.get_cell_value(sh, 'A1').get_type())

    def test_exact2(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")

        wb.set_cell_contents(name, 'B1', '=EXACT(FALSE, "FALSE")')
        self.assertEqual(wb.get_cell_value(name, 'B1'), True)

        wb.set_cell_contents(name, 'B1', "'")
        wb.set_cell_contents(name, 'C1', '=EXACT(A1, B1)')
        self.assertEqual(wb.get_cell_value(name, 'C1'), True)


if __name__ == '__main__':
    unittest.main(verbosity=1)
