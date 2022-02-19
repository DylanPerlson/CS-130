import os; os.system('clear')
import context
from sheets import *

def test_long_reference_chain():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    wb.set_cell_contents(name, 'A1', '1')
    length = 1000
    
    for i in range(1, length):
        location_letter = wb._base_10_to_alphabet(i)
        location_letter_prev = wb._base_10_to_alphabet(i-1)
        location = str(location_letter)+str(1)
        location_prev = str(location_letter_prev)+str(1)
        
        wb.set_cell_contents(name, location, '=1+'+location_prev)
        
    
    assert wb.get_cell_value(name, location) == length

def test_very_connected_ref_chain(): # TODO dimplement later
    pass

def test_cell_with_many_deps():
    wb = Workbook()

    (_,name) = wb.new_sheet("sheet")
    # wb.set_cell_contents(name, 'A1', '1')

    length = 300
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
    wb.set_cell_contents(sheet, 'A1', '1')
    wb.set_cell_contents(sheet, 'A2', '1')

    length = 23

    for i in range(3, length+1):
        location = 'A'+str(i)
        location_prev1 = 'A'+str(i-1)
        location_prev2 = 'A'+str(i-2)
        wb.set_cell_contents(sheet, location, '=' + location_prev1 + '+' + location_prev2)

    cell_value = wb.get_cell_value(sheet, location)
    fibo_output = _fibonacci(length)
    assert cell_value == fibo_output, f'get_cell_value should be {fibo_output}, but is {cell_value}'

# helper function for nth Fibonacci number
def _fibonacci(n):
    # from https://www.geeksforgeeks.org/python-program-for-program-for-fibonacci-numbers-2/
    a = 0
    b = 1

    # Check is n is less than 0
    if n < 0:
        print("Incorrect input")

    # Check is n is equal to 0
    elif n == 0:
        return 0

    # Check if n is equal to 1
    elif n == 1:
        return b
    else:
        for _ in range(1, n):
            c = a + b
            a = b
            b = c
        return b



if __name__ == '__main__':
    import cProfile
    from pstats import Stats

    pr = cProfile.Profile()
    pr.enable()

    #test_long_reference_chain()
    #test_very_connected_ref_chain()
    #test_cell_with_many_deps()
    #test_significant_cell_change() #I think that this test might be wrong
    test_fibonacci()
    # test_cell_cycle()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(3)
