import context
from sheets import *
import decimal
import unittest


class Project3(unittest.TestCase):
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
            wb.set_cell_contents(name2,'B3','=$A1+2')
            wb.set_cell_contents(name2,'B4','=A$1+2')
            
            wb.copy_cells(name2,'A1','B4','B3')

            self.assertEqual(wb.get_cell_contents(name2,'C5'),'=$A3+2')
            self.assertEqual(wb.get_cell_contents(name2,'C6'),'=B$1+2')
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




# uncomment to test only this file
# if __name__ == '__main__':
#     unittest.main(verbosity=3)