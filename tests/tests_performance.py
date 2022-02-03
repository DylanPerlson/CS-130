import os; os.system('cls')
import context
from sheets import *

def test_long_reference_chain():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    wb.set_cell_contents(name, 'A1', '1')
    length = 50
    
    for i in range(1, length):
        location_letter = wb.base_10_to_alphabet(i)
        location_letter_prev = wb.base_10_to_alphabet(i-1)
        location = str(location_letter)+str(1)
        location_prev = str(location_letter_prev)+str(1)

        wb.set_cell_contents(name, location, '=1+'+location_prev)
    
    assert wb.get_cell_value(name, location) == length

def test_very_connected_ref_chain(): # TODO implement later
    pass

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

    length = 50

    for i in range(1, length+1):
        location = 'A'+str(i)
        wb.set_cell_contents(name, location, '=B1')
    
    wb.set_cell_contents(name, 'B1', '2')
    # assert wb.get_cell_value(name, 'A1') == 2 # TODO uncomment

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
    
    # TODO uncomment below
    # wb.set_cell_contents(name, 'A1', '='+location)
    # assert wb.get_cell_value(name,'A4').get_type() == CellErrorType.CIRCULAR_REFERENCE
    # wb.set_cell_contents(name, 'A1', '2')
    # assert wb.get_cell_value(name,'A4') == 2 


if __name__ == '__main__':
    import cProfile
    from pstats import Stats

    pr = cProfile.Profile()
    pr.enable()

    test_long_reference_chain()
    test_very_connected_ref_chain()
    test_cell_with_many_deps()
    test_significant_cell_change()
    test_cell_cycle()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(5)