import context
from sheets import *
import decimal
import unittest
from sheets import version
from sheets import cell


class Project5(unittest.TestCase):
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


    
if __name__ == '__main__':
    unittest.main(verbosity=1)