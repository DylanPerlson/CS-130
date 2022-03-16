from html.entities import name2codepoint
import os; os.system('clear')
import context
from sheets import *

def test_long_reference_chain():
    wb = Workbook()
    
    #get cell value from a chain reference is not slow, the continually setting a value is 
    length = 400
    (_,name) = wb.new_sheet("sheet")

    
    pr = cProfile.Profile()
    pr.enable()

    pr = cProfile.Profile()
    pr.enable()

    for i in range(2, length+1):
        location = 'A'+str(i)
        location_prev = 'A'+str(i-1)

        wb.set_cell_contents(name, location, '=1+'+location_prev)

   
    wb.set_cell_contents(name, 'A1', '1')
    
    print(wb.get_cell_value(name, location))

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('cumtime').print_stats(15)
    #assert wb.get_cell_value(name, location) == length
    #only get cell value once, and only parse at the very end???

def test_long_reference_chain_letters():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    wb.set_cell_contents(name, 'A1', '1')
    length = 300

    for i in range(1, length):
        location_letter = wb._base_10_to_alphabet(i)
        location_letter_prev = wb._base_10_to_alphabet(i-1)
        location = str(location_letter)+str(1)
        location_prev = str(location_letter_prev)+str(1)
        wb.set_cell_contents(name, location, '=1+'+location_prev)
        #wb.get_cell_value(name, location)

    print(wb.get_cell_value(name, location))
    #assert wb.get_cell_value(name, location) == length
    #print(wb.get_cell_value(name, location))


def test_cell_with_many_deps():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    # wb.set_cell_contents(name, 'A1', '1')

    length = 50
    formula = '='

    for i in range(1, length+1):
        location = 'A'+str(i)
        wb.set_cell_contents(name, location, '1')

    for i in range(1, length+1):
        location = 'A'+str(i)
        formula = formula + '+' + location

    wb.set_cell_contents(name, 'B1', formula)
    assert int(wb.get_cell_value(name, 'B1')) == length

def test_significant_cell_change():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    wb.set_cell_contents(name, 'B1', '1')
    # wb.set_cell_contents(name, 'A1', '1')

    length = 10

    for i in range(1, length+1):
        location = 'A'+str(i)
        wb.set_cell_contents(name, location, '=B1')

    wb.set_cell_contents(name, 'B1', '2')
    assert wb.get_cell_contents(name, 'A1') == '=B1'
    assert wb.get_cell_value(name, 'A1') == 2, 'Cell value of A1 is wrong.' # for Pieter there is an error here

def test_cell_cycle():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    wb.set_cell_contents(name, 'A1', '1')
    # wb.set_cell_contents(name, 'B1', '1')

    length = 50

    for i in range(2, length+1):
        location = 'A'+str(i)
        location_prev = 'A'+str(i-1)
        wb.set_cell_contents(name, location, '='+location_prev)

    # for Pieter there is an error below
    wb.set_cell_contents(name, 'A1', '='+location)
    assert wb.get_cell_value(name,'A4').get_type() == CellErrorType.CIRCULAR_REFERENCE, 'No circular reference error given.'
    wb.set_cell_contents(name, 'A1', '2')
    assert wb.get_cell_value(name,'A4') == 2, 'Cell value of A4 is wrong.'

def test_fibonacci():
    wb = Workbook()

    (_,sheet) = wb.new_sheet()


    length = 100

    for i in range(3, length):
        location = 'A'+str(i)
        location_prev1 = 'A'+str(i-1)
        location_prev2 = 'A'+str(i-2)
        wb.set_cell_contents(sheet, location, '=' + location_prev1 + '+' + location_prev2)

    pr = cProfile.Profile()
    pr.enable()
    wb.set_cell_contents(sheet, 'A1', '1')
    wb.set_cell_contents(sheet, 'A2', '1')

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('cumtime').print_stats(5)

    cell_value = wb.get_cell_value(sheet, location)
    print(location)
    print(cell_value)
    #print(fibo_output)
    
def test_get_cell_val():
    
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    wb.set_cell_contents(name, 'A1', '=5+7')
    length = 100
    
    
        
    
    
    pr = cProfile.Profile()
    pr.enable()

    for i in range(100):
        wb.get_cell_value(name, 'A1')


    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('cumtime').print_stats(5)

def test_load_wkbk():
    wb = Workbook()
    (_, name1) = wb.new_sheet("fiRst_sheet")

    wb.set_cell_contents(name1, 'AA57', 'words')
    wb.set_cell_contents(name1, 'AAA3', '=12+4')
    wb.set_cell_contents(name1, 'JNE41', 'more words')
    for i in range(2, 150):
        location = 'A'+str(i)
        location_prev1 = 'A'+str(i-1)
        location_prev2 = 'A'+str(i-2)
        wb.set_cell_contents(name1, location, '=' + location_prev1 + '+' + location_prev2)

    (_, name2) = wb.new_sheet("2nd_sheet")

    wb.set_cell_contents(name2, 'aa57', '12.0')
    wb.set_cell_contents(name2, 'AAA3', '=12.0+1.00')
    wb.set_cell_contents(name2, 'JNE41', '100')


    pr = cProfile.Profile()
    pr.enable()

    with open('tests/json/save_testfile.json', 'w') as fp:
        wb.save_workbook(fp)
    with open('tests/json/load_testfile.json') as fp:
        wb2 = Workbook.load_workbook(fp)

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('cumtime').print_stats(5)

def test_rename_sheet():
    wb = Workbook()
    (_, name1) = wb.new_sheet("fiRst_sheet")

    
    wb.set_cell_contents(name1, 'AA57', 'words')
    wb.set_cell_contents(name1, 'AAA3', '=12+4')
    wb.set_cell_contents(name1, 'JNE41', 'more words')
    
    length = 50
   
    for j in range(5):
        (_,name) = wb.new_sheet("s"+str(j))

        for i in range(3, length):
            location = 'A'+str(i)
            location_prev1 = 'A'+str(i-1)
            location_prev2 = 'A'+str(i-2)
            wb.set_cell_contents(name1, location, '=' + location_prev1 + '+' + location_prev2)
            #print(wb.get_cell_contents(name1,location))


    pr = cProfile.Profile()
    pr.enable()

    wb.rename_sheet(name1,'new_sheet')

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('cumtime').print_stats(5)

def test_move_cells():
    wb = Workbook()
    (_, name1) = wb.new_sheet("fiRst_sheet")

    wb.set_cell_contents(name1, 'AA57', 'words')
    wb.set_cell_contents(name1, 'AAA3', '=12+4')
    wb.set_cell_contents(name1, 'JNE41', 'more words')
    for i in range(2, 100):
        location = 'A'+str(i)
        location_prev1 = 'A'+str(i-1)
        location_prev2 = 'A'+str(i-2)
        wb.set_cell_contents(name1, location, '=' + location_prev1 + '+' + location_prev2)


    pr = cProfile.Profile()
    pr.enable()

    wb.move_cells(name1,'A1','B100','C200')

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('cumtime').print_stats(5)

if __name__ == '__main__':
    import cProfile
    from pstats import Stats

    # pr = cProfile.Profile()
    # pr.enable()

    test_long_reference_chain()
    #test_long_reference_chain_letters()
    #test_very_connected_ref_chain()
    #test_cell_with_many_deps()
    #test_significant_cell_change() #I think that this test might be wrong
    #test_fibonacci()
    # test_cell_cycle()

    #test_load_wkbk()
    #test_rename_sheet()
    #test_move_cells() #this is slow
    #test_get_cell_val()
    # pr.disable()
    # stats = Stats(pr)
    # stats.sort_stats('cumtime').print_stats(5)
