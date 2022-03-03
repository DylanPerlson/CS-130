import context
from sheets import *
import decimal
import unittest


class Aaron(unittest.TestCase):
    # def test_single_cell_notification(self):
    #     wb = Workbook()
    #     (_, name) = wb.new_sheet("s1")
    #     def on_cells_changed(workbook, changed_cells):
    #         print(f'Cell(s) changed:  {changed_cells}')
    #     wb.notify_cells_changed(on_cells_changed)
        
    #     wb.set_cell_contents(name,'A1','1')
    #     wb.set_cell_contents(name,'A2',"=A1")
    #     wb.set_cell_contents(name,'A1',"5")

    def test_aaron(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        def on_cells_changed(workbook, changed_cells):
            print(f'Cell(s) changed:  {changed_cells}')
        wb.notify_cells_changed(on_cells_changed)
        print('.')
        wb.set_cell_contents(name,'A1','1') 
        wb.set_cell_contents(name,'A2',"hi")
        wb.set_cell_contents(name,'A3',"=A1 + 2")  
        wb.set_cell_contents(name,'A1','2')
        print('2 above')
        wb.set_cell_contents(name,'A4', '=A3')
        wb.set_cell_contents(name,'A1', '5')
        print('3 above')

    def test_circular_references(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2',"=A1")
        wb.set_cell_contents(name,'A1',"=A2")
        self.assertEqual(wb.get_cell_value(name, 'A1').get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(wb.get_cell_value(name, 'A2').get_type(), CellErrorType.CIRCULAR_REFERENCE)
    
    def test_and(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=AND(true, false)")
        wb.set_cell_contents(name,'A4',"=AND(true, true)")
        wb.set_cell_contents(name,'A5',"=AND(false, false)")
        wb.set_cell_contents(name,'A6',"=AND(false, true)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), "false")
        self.assertEqual(wb.get_cell_value(name, 'A4'), "true")
        self.assertEqual(wb.get_cell_value(name, 'A5'), "false")
        self.assertEqual(wb.get_cell_value(name, 'A6'), "false")
    
    def test_or(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=OR(true, false)")
        wb.set_cell_contents(name,'A4',"=OR(true, true)")
        wb.set_cell_contents(name,'A5',"=OR(false, false)")
        wb.set_cell_contents(name,'A6',"=OR(false, true)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), "true")
        self.assertEqual(wb.get_cell_value(name, 'A4'), "true")
        self.assertEqual(wb.get_cell_value(name, 'A5'), "false")
        self.assertEqual(wb.get_cell_value(name, 'A6'), "true")
    
    def test_not(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=NOT(true)")
        wb.set_cell_contents(name,'A4',"=NOT(false)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), "false")
        self.assertEqual(wb.get_cell_value(name, 'A4'), "true")
    
    def test_exact(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=EXACT('hello', 'HELLO')")
        wb.set_cell_contents(name,'A4',"=EXACT('Hello','Hello')")
        wb.set_cell_contents(name,'A5',"=EXACT('Hello', 'hElLo')")

        self.assertEqual(wb.get_cell_value(name, 'A3'), "false")
        self.assertEqual(wb.get_cell_value(name, 'A4'), "true")
        self.assertEqual(wb.get_cell_value(name, 'A5'), "false")




if __name__ == '__main__':
    unittest.main(verbosity=0)