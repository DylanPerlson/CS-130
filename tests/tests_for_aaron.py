import context
from sheets import *
import decimal
import unittest


class Aaron(unittest.TestCase):
    def test_aaron(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        def on_cells_changed(workbook, changed_cells):
            print(f'Cell(s) changed:  {changed_cells}')
        wb.add_notification_function(on_cells_changed)
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2',"hi")
        wb.set_cell_contents(name,'A3',"=A1 + 2")
        wb.set_cell_contents(name,'A1','2')
        wb.set_cell_contents(name,'A4', '=A3')
        wb.set_cell_contents(name,'A1', '5')
    
    def test_circular_references(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2',"=A1")
        wb.set_cell_contents(name,'A1',"=A2")

        print(wb.get_cell_value(name, 'A1'))
        #assert wb.get_cell_value(name, 'A1') == CellErrorType.CIRCULAR_REFERENCE
        #assert wb.get_cell_value(name, 'A2') == CellErrorType.CIRCULAR_REFERENCE

        


if __name__ == '__main__':
    unittest.main(verbosity=1)