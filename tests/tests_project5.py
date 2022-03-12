import context
from sheets import *
import decimal
import unittest
from sheets import version
from sheets import cell


class Project5(unittest.TestCase):
     def test_moving_multi(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("s1")
        wb.set_cell_contents(name1,'A1',"=AND(A2:A3)")
        wb.set_cell_contents(name1,'A2','=AND(A2,A3)')
        wb.move_cells(name1,'A1','B4','C1')
        self.assertEqual(wb.get_cell_contents(name1,'C1'),"=AND(C2:C3)")
        self.assertEqual(wb.get_cell_contents(name1,'C2'),"=AND(C2,C3)")



    
if __name__ == '__main__':
    unittest.main(verbosity=1)