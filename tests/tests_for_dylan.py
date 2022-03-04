import context
from sheets import *
import decimal
import unittest


class Dylan(unittest.TestCase):
    def test_None_error(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2',"=A1")
        self.assertEqual(wb.get_cell_value(name,'A2'),0)


    def test_reference_change(self):

        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','5')
        wb.set_cell_contents(name,'A2',"=A1")
        wb.set_cell_contents(name,'A1','7')
        self.assertEqual(wb.get_cell_value(name,'A1'),7)

    def test_topological(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','=A2+A3')
        wb.set_cell_contents(name,'A2','=A3') # parent cells need to be notified of changes i believe
        wb.set_cell_contents(name,'A3','5')
        self.assertEqual(wb.get_cell_value(name,'A1'),10)

    def test_fib_failure(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        
        wb.set_cell_contents(name,'A3','=A1+A2')  
        wb.set_cell_contents(name,'A4','=A2+A3') 
        wb.set_cell_contents(name,'A5','=A3+A4') 
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2','1')
        self.assertEqual(wb.get_cell_value(name,'A5'),5)
        self.assertEqual(wb.get_cell_value(name,'A4'),3)
        self.assertEqual(wb.get_cell_value(name,'A3'),2)
    def test_tarjan(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2','1')
        wb.set_cell_contents(name,'A3','1')
        wb.set_cell_contents(name,'A4','=A2')
        wb.set_cell_contents(name,'A2','=A4')
        





if __name__ == '__main__':
    #print('Dylan--------')
    unittest.main(verbosity=1)