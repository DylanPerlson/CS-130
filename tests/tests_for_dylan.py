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
        wb.set_cell_contents(name,'A2','=A3') 
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
    def test_cell_range_update(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        wb.set_cell_contents(name,'A1','1')
        wb.set_cell_contents(name,'A2','1')
        wb.set_cell_contents(name,'A3','1')
        wb.set_cell_contents(name,'A4','=SUM(A1:A3)')
       
        # print(wb.master_cell_dict)
        # print(wb.children_dict)
        #check that the above print as intended


    def test_notification_dylan(self):
        wb = Workbook()
        (_, name) = wb.new_sheet("s1")
        def on_cells_changed(workbook, changed_cells):
            print(f'Cell(s) changed:  {changed_cells}')
        
        
        wb.set_cell_contents(name,'A1','hi')
        wb.set_cell_contents(name,'A2','1')
        wb.notify_cells_changed(on_cells_changed)
        #test each function for appropriate notifications
        print('.')
        #wb.copy_sheet(name)
        #wb.move_cells(name,'A1','A5','A10')
        #wb.copy_cells(name,'A1','A5','A10')
        #wb.move_cells(name,'A1','A5','A10')
        #wb.del_sheet(name)
        

        #go through all of the p5 req. 
      


        #cell changes and notificatiosn for cell range
        #comment out all prints



    def test_sorting_simple(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')

        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')

        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '1')

        wb.sort_region(sh, 'A2', 'C4', [1])
        val = wb.get_cell_value(sh, 'B3')
        self.assertEqual(val, 6, f'instead it is: {val}') # excel #1

        wb.set_cell_contents(sh,'a2', '10')
        wb.set_cell_contents(sh,'b2', '2')
        wb.set_cell_contents(sh,'c2', '3')

        wb.set_cell_contents(sh,'a3', '4')
        wb.set_cell_contents(sh,'b3', '5')
        wb.set_cell_contents(sh,'c3', '6')

        wb.set_cell_contents(sh,'a4', '7')
        wb.set_cell_contents(sh,'b4', '8')
        wb.set_cell_contents(sh,'c4', '1')

        wb.sort_region(sh, 'A2', 'C4', [3])
        val = wb.get_cell_value(sh, 'B2')
        self.assertEqual(val, 10, f'instead it is: {val}') # excel #2

    def test_sorting_stable_dylan(self):
        wb = Workbook()
        (_,sh) = wb.new_sheet('sheet')

        wb.set_cell_contents(sh,'a2', '3')
        wb.set_cell_contents(sh,'b2', '#DIV/0!')
        wb.set_cell_contents(sh,'c2', '#REF!')
        
        wb.set_cell_contents(sh,'a3', '10')
        wb.set_cell_contents(sh,'b3', '20')
        wb.set_cell_contents(sh,'c3', '30')

       

        #2 1 2 for a - swap first and second
        
        wb.sort_region(sh, 'A2', 'C4', [1])
        # print(wb.get_cell_value(sh, 'A2'))
        # print(wb.get_cell_value(sh, 'B2'))
        # print(wb.get_cell_value(sh, 'C2'))
        
        # print(wb.get_cell_value(sh, 'A3'))
        # print(wb.get_cell_value(sh, 'B3'))
        # print(wb.get_cell_value(sh, 'C3'))
        # the above is working

if __name__ == '__main__':
    unittest.main(verbosity=1)
    
    
