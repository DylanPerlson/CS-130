import context
from sheets import *
import decimal
import unittest


class Aaron(unittest.TestCase):
    def test_aaron(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2',"hi")
        wb.set_cell_contents(name,'A3',"=A1 + 2")
        wb.set_cell_contents(name,'A1','2')



if __name__ == '__main__':
    unittest.main(verbosity=1)