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

    # this code is used to check cell notifications
    # but when it's uncommented it gives output
    # so usually it is commented out:
    def test_notification_with_print_output(self):
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
        wb.set_cell_contents(name,'A5', '=A1')
        wb.set_cell_contents(name,'A1','1')
        print('4 above')


    def test_circular_references(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2',"=A1")
        wb.set_cell_contents(name,'A1',"=A2")
        self.assertEqual(wb.get_cell_value(name, 'A1').get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(wb.get_cell_value(name, 'A2').get_type(), CellErrorType.CIRCULAR_REFERENCE)






if __name__ == '__main__':
    unittest.main(verbosity=0)