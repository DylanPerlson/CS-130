import context
from sheets import *
import decimal
import unittest


class Dylan(unittest.TestCase):
    def test_None_error(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2',"=A1")
        self.assertEqual(wb.get_cell_value(name,'A2'),None)


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
        wb.set_cell_contents(name,'A2','=A3') # parent cells need to be notified of changes i believe\
        wb.set_cell_contents(name,'A3','5')
        self.assertEqual(wb.get_cell_value(name,'A1'),10)
        





if __name__ == '__main__':
    #print('Dylan--------')
    unittest.main(verbosity=1)