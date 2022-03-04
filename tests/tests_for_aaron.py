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

    # # TODO check this test (it gives console output)
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
        wb.set_cell_contents(name,'A7',"=AND(false)")
        wb.set_cell_contents(name,'A8',"=AND()")
        wb.set_cell_contents(name,'A9',"=AND(false, true, false)")
        wb.set_cell_contents(name,'A10',"=AND(true, true, true, true)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), False)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)
        self.assertEqual(wb.get_cell_value(name, 'A6'), False)
        self.assertEqual(wb.get_cell_value(name, 'A7'), False)
        self.assertEqual(wb.get_cell_value(name, 'A8').get_type(), CellErrorType.TYPE_ERROR)
        self.assertEqual(wb.get_cell_value(name, 'A9'), False)
        self.assertEqual(wb.get_cell_value(name, 'A10'), True)

    def test_or(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=OR(true, false)")
        wb.set_cell_contents(name,'A4',"=OR(true, true)")
        wb.set_cell_contents(name,'A5',"=OR(false, false)")
        wb.set_cell_contents(name,'A6',"=OR(false, true)")
        wb.set_cell_contents(name,'A7',"=OR(false)")
        wb.set_cell_contents(name,'A8',"=OR()")
        wb.set_cell_contents(name,'A9',"=OR(false, true, false)")
        wb.set_cell_contents(name,'A10',"=OR(true, true, true, true)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), True)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)
        self.assertEqual(wb.get_cell_value(name, 'A6'), True)
        self.assertEqual(wb.get_cell_value(name, 'A7'), False)
        self.assertEqual(wb.get_cell_value(name, 'A8').get_type(), CellErrorType.TYPE_ERROR)
        self.assertEqual(wb.get_cell_value(name, 'A9'), True)
        self.assertEqual(wb.get_cell_value(name, 'A10'), True)

    def test_not(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3',"=NOT(true)")
        wb.set_cell_contents(name,'A4',"=NOT(false)")

        self.assertEqual(wb.get_cell_value(name, 'A3'), False)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)

    def test_exact(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A3','=EXACT("hello", "HELLO")')
        wb.set_cell_contents(name,'A4','=EXACT("Hello","Hello")')
        wb.set_cell_contents(name,'A5','=EXACT("Hello", "hElLo")')

        self.assertEqual(wb.get_cell_value(name, 'A3'), False)
        self.assertEqual(wb.get_cell_value(name, 'A4'), True)
        self.assertEqual(wb.get_cell_value(name, 'A5'), False)

    def test_error_priority(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2','=#ERROR! * #REF!')
        wb.set_cell_contents(name,'A3','=#REF! * #ERROR!')
        wb.set_cell_contents(name,'A5','=#REF! + #NAME?')
        wb.set_cell_contents(name,'A6','=#DIV/0! + #VALUE!')
        wb.set_cell_contents(name,'A7','=#VALUE! & #ERROR!')


        self.assertEqual(wb.get_cell_value(name,'A2').get_type(),CellErrorType.PARSE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A3').get_type(),CellErrorType.PARSE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A5').get_type(),CellErrorType.BAD_REFERENCE)
        self.assertEqual(wb.get_cell_value(name,'A6').get_type(),CellErrorType.TYPE_ERROR)
        self.assertEqual(wb.get_cell_value(name,'A7').get_type(),CellErrorType.PARSE_ERROR)
    
    def test_mixed(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A2','6')
        wb.set_cell_contents(name,'B1','1')
        wb.set_cell_contents(name,'C1','1')
        wb.set_cell_contents(name,'D1','14')
        wb.set_cell_contents(name, 'E1', '=OR(AND(A1 > 5, B1 < 2), AND(C1 < 6, D1 = 14))')

        self.assertEqual(wb.get_cell_value(name, 'E1'), True)




if __name__ == '__main__':
    unittest.main(verbosity=0)