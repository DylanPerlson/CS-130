import context
from sheets import *
import decimal
import unittest
from sheets import version
from sheets import cell

import os; os.system('clear')

class Project5(unittest.TestCase):
    def test_avg_sum(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")

        wb.set_cell_contents(name,'A1',"5")
        wb.set_cell_contents(name,'A2',"15")
        wb.set_cell_contents(name,'A3',"10")
        wb.set_cell_contents(name,'A4',"=SUM(A1,A3)")
        wb.set_cell_contents(name,'A5',"=SUM(A1:A3)")
        wb.set_cell_contents(name,'A6',"=AVERAGE(A1,A3)")
        wb.set_cell_contents(name,'A7',"=AVERAGE(A1:A3)")

        self.assertEqual(wb.get_cell_value(name,'A4'),15)
        self.assertEqual(wb.get_cell_value(name,'A5'),30)

        self.assertEqual(wb.get_cell_value(name,'A6'),7.5)
        self.assertEqual(wb.get_cell_value(name,'A7'),10)

        wb.set_cell_contents(name,'A5','=SUM(1,2,3,4,5,6,7,8)')
        self.assertEqual(wb.get_cell_value(name,'A5'), 36)

        wb.set_cell_contents(name,'A5','=SUM(1,true,false)')
        self.assertEqual(wb.get_cell_value(name,'A5'), 2)

        wb.set_cell_contents(name,'A5','=SUM("string")')
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A6','=AVERAGE("string", 4)')
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A6','=AVERAGE(true, true, false, false)')
        self.assertEqual(wb.get_cell_value(name,'A6'), 0.5)

    def test_min_max(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")

        wb.set_cell_contents(name,'A1',"3")
        wb.set_cell_contents(name,'A2',"2")
        wb.set_cell_contents(name,'A3',"10")
        wb.set_cell_contents(name,'A4',"=MIN(A1,A3)")
        wb.set_cell_contents(name,'A5',"=MIN(A1:A3)")
        wb.set_cell_contents(name,'A6',"=MAX(A1,A2)")
        wb.set_cell_contents(name,'A7',"=MAX(A1:A3)")

        self.assertEqual(wb.get_cell_value(name,'A4'),3)
        self.assertEqual(wb.get_cell_value(name,'A5'),2)

        self.assertEqual(wb.get_cell_value(name,'A6'),3)
        self.assertEqual(wb.get_cell_value(name,'A7'),10)

        wb.set_cell_contents(name,'A5','=MIN("string")')
        # print(wb.get_cell_value(name,'A5'))
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A6','=MAX("string")')
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(), CellErrorType.TYPE_ERROR)

        wb.set_cell_contents(name,'A6','=MAX(-1,-2,-3,true)')
        self.assertEqual(wb.get_cell_value(name,'A6'), 1)

        wb.set_cell_contents(name,'A6','=MIN(2,3,false)')
        self.assertEqual(wb.get_cell_value(name,'A6'), 0)

    def test_cell_range_other_sheet(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("s1")
        (_, name2) = wb.new_sheet("s2")
        wb.set_cell_contents(name2,'A3','True')
        wb.set_cell_contents(name2,'A2','False')

        wb.set_cell_contents(name1,'A1',"=AND(s2!A3:A2)")

        self.assertEqual(wb.get_cell_value(name1,'A1'),False)

    def test_moving_multi(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("s1")
        wb.set_cell_contents(name1,'A1',"=AND(A2:A3)")
        wb.set_cell_contents(name1,'A2','=AND(A2,A3)')
        wb.move_cells(name1,'A1','B4','C1')
        self.assertEqual(wb.get_cell_contents(name1,'C1'),"=AND(C2:C3)")
        self.assertEqual(wb.get_cell_contents(name1,'C2'),"=AND(C2,C3)")

    def test_rename_multi(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("s1")
        wb.set_cell_contents(name1,'A1',"=AND(A2:A3)")
        wb.set_cell_contents(name1,'A2','=AND(A2,A3)')
        name2 = 'skdbkhsd'
        wb.rename_sheet(name1,name2)
        self.assertEqual(wb.get_cell_contents(name2,'A1'),"=AND(A2:A3)")
        self.assertEqual(wb.get_cell_contents(name2,'A2'),"=AND(A2,A3)")

    def test_and_range(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','True')
        wb.set_cell_contents(name,'A2','false')
        wb.set_cell_contents(name,'A3','true')
        wb.set_cell_contents(name,'A4','=AND(A1:A3)')
        #print(wb.get_cell_value(name,'A4'))
        self.assertEqual(wb.get_cell_value(name,'A4'),False)
        wb.set_cell_contents(name,'A2','true')
        wb.set_cell_contents(name,'A4','=AND(A1:A3)')
        #does not notify the cell range of dependencies
        #print(wb.get_cell_value(name,'A4'))
        self.assertEqual(wb.get_cell_value(name,'A4'),True)

        #what about
        #wb.set_cell_contents(name,'A4','=AND(A1,A2:A3)')


        #TODO DYLAN need to also include other sheets

    def test_or_range(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")

        # wb.set_cell_contents(name,'A1','3')
        # wb.set_cell_contents(name,'A2','4')
        # wb.set_cell_contents(name,'A3','=A1+A2')
        # print(wb.get_cell_value(name,'A3'))


        wb.set_cell_contents(name,'A1','True')
        wb.set_cell_contents(name,'A2','false')
        wb.set_cell_contents(name,'A3','true')
        wb.set_cell_contents(name,'A4','=OR(A1:A3)')
        self.assertEqual(wb.get_cell_value(name,'A4'),True)
        wb.set_cell_contents(name,'A1','false')
        wb.set_cell_contents(name,'A2','false')
        wb.set_cell_contents(name,'A3','false')
        wb.set_cell_contents(name,'A4','=OR(A1:A3)')
        self.assertEqual(wb.get_cell_value(name,'A4'),False)


    def test_mixed(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2','6')
        wb.set_cell_contents(name,'B1','1')
        wb.set_cell_contents(name,'C1','1')
        wb.set_cell_contents(name,'D1','14')
        wb.set_cell_contents(name, 'E1', '=OR(AND(A1 > 5, B1 < 2), AND(C1 < 6, D1 = 14))')

        self.assertEqual(wb.get_cell_value(name, 'E1'), True)

    def test_hlookup(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', 'three')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', 'true')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        # [[1   , 2, 'three'],
        #  [4   , 5, 6],
        #  [true, 8, 9]]

        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(1, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 1)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(1, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), True)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(2, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 5)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP(2, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 8)
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP("three", a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 'three')
        wb.set_cell_contents(sh, 'A1', '=HLOOKUP("three", a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 6)

        # print(wb.get_cell_value(sh, 'A1'))

    def test_vlookup(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', 'three')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '=true')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        # [[1   , 2, 'three'],
        #  [4   , 5, 6],
        #  [true, 8, 9]]

        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 1)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 'three')
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(4, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 5)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(4, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 6)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(true, a2:c4, 1)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), True)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(true, a2:c4, 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 9)
        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(false, a2:c4, 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1').get_type(), CellErrorType.TYPE_ERROR)

    def test_if_with_ranges(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()


        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        wb.set_cell_contents(sh,'B1', 'false')
        wb.set_cell_contents(sh, 'A10', '=AVERAGE(IF(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 5)

        wb.set_cell_contents(sh,'B1', 'true')
        wb.set_cell_contents(sh, 'A10', '=AVERAGE(IF(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 4)

        wb.set_cell_contents(sh,'B1', 'false')
        wb.set_cell_contents(sh, 'A10', '=SUM(IF(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 15)

        wb.set_cell_contents(sh,'B1', 'true')
        wb.set_cell_contents(sh, 'A10', '=MIN(IF(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 1)

        wb.set_cell_contents(sh,'B1', 'false')
        wb.set_cell_contents(sh, 'A10', '=MAX(IF(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 8)

    def test_choose_with_ranges(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet()

        wb.set_cell_contents(sh,'B1', 'false')

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        wb.set_cell_contents(sh,'B1', '2')
        wb.set_cell_contents(sh, 'A10', '=AVERAGE(CHOOSE(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 5)

        wb.set_cell_contents(sh,'B1', '1')
        wb.set_cell_contents(sh, 'A10', '=AVERAGE(CHOOSE(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 4)

        wb.set_cell_contents(sh,'B1', '2')
        wb.set_cell_contents(sh, 'A10', '=SUM(CHOOSE(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 15)

        wb.set_cell_contents(sh,'B1', '1')
        wb.set_cell_contents(sh, 'A10', '=MIN(CHOOSE(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 1)

        wb.set_cell_contents(sh,'B1', '2')
        wb.set_cell_contents(sh, 'A10', '=MAX(CHOOSE(B1, A2:A4, B2:B4))')
        self.assertEqual(wb.get_cell_value(sh, 'A10'), 8)

    def test_indirect_with_ranges(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh, 'B1', sh)

        wb.set_cell_contents(sh,'a2', '1')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')
        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '#REF!')
        wb.set_cell_contents(sh,'c3', '6')
        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '9')

        wb.set_cell_contents(sh, 'A1', '=IFERROR(VLOOKUP(4, INDIRECT(B1 & "!A2:c4"), 2), "")')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), '')

        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(7, INDIRECT("' + sh + '" & "!A2:c4"), 3)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 9)

        wb.set_cell_contents(sh, 'A1', '=VLOOKUP(1, INDIRECT(B1 & "!A2:c4"), 2)')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 2)

        wb.set_cell_contents(sh,'B3', '5')
        wb.set_cell_contents(sh, 'A1', '=SUM(INDIRECT(B1 & "!A2:c4"))')
        self.assertEqual(wb.get_cell_value(sh, 'A1'), 45)

        (_,sh2) = wb.new_sheet('second_sheet')
        wb.set_cell_contents(sh2,'B1', sh)

        wb.set_cell_contents(sh2, 'A1', '=IFERROR(VLOOKUP(4, INDIRECT(B1 & "!A2:c4"), 2), "")')
        self.assertEqual(wb.get_cell_value(sh2, 'A1'), 5)

        wb.set_cell_contents(sh2, 'A1', '=IFERROR(VLOOKUP(4, INDIRECT(B2 & "!A2:c4"), 2), "TEST")')
        self.assertEqual(wb.get_cell_value(sh2, 'A1'), 'TEST')

        wb.set_cell_contents(sh2, 'A1', '=INDIRECT("non_existing_sheet" & "!A2:c4")')
        self.assertEqual(wb.get_cell_value(sh2, 'A1').get_type(), CellErrorType.BAD_REFERENCE)


if __name__ == '__main__':
    unittest.main(verbosity=1)