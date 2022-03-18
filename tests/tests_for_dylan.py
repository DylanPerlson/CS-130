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
        
        self.assertEqual(wb.sheets[0].cells[(1,3)].evaluated_value, 2)
        self.assertEqual(wb.sheets[0].cells[(1,4)].evaluated_value,3)
        self.assertEqual(wb.sheets[0].cells[(1,5)].evaluated_value,5)
        #TODO DTP does this actually mean the cell value was updated though?

        self.assertEqual(wb.get_cell_value(name,'A5'),5)
        self.assertEqual(wb.get_cell_value(name,'A4'),3)
        self.assertEqual(wb.get_cell_value(name,'A3'),2)
    # def test_tarjan(self):
    #     wb = Workbook()
    #     (_, name) = wb.new_sheet("s1")
    #     wb.set_cell_contents(name,'A1','1')
    #     wb.set_cell_contents(name,'A2','1')
    #     wb.set_cell_contents(name,'A3','1')
    #     wb.set_cell_contents(name,'A4','=A2')
    #     wb.set_cell_contents(name,'A2','=A4')

    def test_rename_dependents(self):
        wb = Workbook()
        (_, name1) = wb.new_sheet("s1")
        (_, name2) = wb.new_sheet("s2")
        wb.set_cell_contents(name1,'A3','=A1+A2')
        wb.set_cell_contents(name1,'A4','=A2+A3')
        wb.set_cell_contents(name2,'A1',"=s1!A1+A2")
        wb.rename_sheet('S1','new_name')


        # (_, name) = wb.new_sheet("s1")
        # def on_cells_changed(workbook, changed_cells):
        #     print(f'Cell(s) changed:  {changed_cells}')
        # wb.notify_cells_changed(on_cells_changed)
        # print('.')
        # wb.set_cell_contents(name,'A1','1')
        # wb.set_cell_contents(name,'A2',"hi")
        # wb.set_cell_contents(name,'A3',"=A1 + 2")
        # wb.set_cell_contents(name,'A1','2')
        # print('2 above')
        # wb.set_cell_contents(name,'A4', '=A3')
        # wb.set_cell_contents(name,'A1', '5')
        # print('3 above')

    #not setting every circ ref cell to be a circ ref

    def test_copy_rename(self):
        length = 20
        wb = Workbook()
        (_, name1) = wb.new_sheet("s1")
        (_, name2) = wb.new_sheet("s2")
        
        for i in range(length):
            loc = 'A'+str(i+1)
            contents = '=b'+str(i+1)
            wb.set_cell_contents(name1,loc,contents)

        wb.move_cells(name1,'A1','B100','E3',name2)
        for i in range(length):
            loc = 'A'+str(i+1)
            self.assertEqual(wb.get_cell_contents(name1,loc),None)
            loc = 'E'+str(i+3)
            val = '=F'+str(i+3)
            self.assertEqual(wb.get_cell_contents(name2,loc),val)

    def test_circ_ref_for_ever_cell(self):
        length = 20
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        
        
        for i in range(length):
            loc = 'A'+str(i+1)
            contents = '=A'+str(i+2)+'+4'
            wb.set_cell_contents(name,loc,contents)

        loc = 'A'+str(length+1)
        wb.set_cell_contents(name,loc,'=A1+3')

        for i in range(length+1):
            loc = 'A'+str(i+1)
            self.assertEqual(wb.get_cell_value(name,loc).get_type(),CellErrorType.CIRCULAR_REFERENCE)

    def test_more_rename(self):
        length = 20
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        (_, name2) = wb.new_sheet("Old")
        for i in range(length):
            loc = 'A'+str(i+1)
            contents = '=Old!A'+str(i+2)+'+4'
            wb.set_cell_contents(name,loc,contents)
        
        wb.rename_sheet(name2,'nEw')
        for i in range(length):
            loc = 'A'+str(i+1)
            contents = '=nEw!A'+str(i+2)+'+4'
            self.assertEqual(wb.get_cell_contents(name,loc),contents)

        wb.rename_sheet('s1','other_s')

        for i in range(length):
            loc = 'A'+str(i+1)
            contents = '=nEw!A'+str(i+2)+'+4'
            self.assertEqual(wb.get_cell_contents('OtHER_S',loc),contents)

if __name__ == '__main__':
    unittest.main(verbosity=1)
    
