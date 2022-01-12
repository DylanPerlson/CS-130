'''
import sheets

# test whether we can put something in a cell and get the extend of the sheet, etc.

# Test to ensure workbook initialized properly
test_workbook = sheets.Workbook()

test_workbook.new_sheet('FirstSheet') # the name is FirstSheet
'''

############### CODE FROM THE ASSIGNMENT: ###############
import decimal
import sheets

# Should print the version number of your sheets library,
# which should be 1.0 for the first project.
print(f'Using sheets engine version 1.0')

# Make a new empty workbook
wb = sheets.Workbook()
(index, name) = wb.new_sheet("test")

# Should print:  New spreadsheet "Sheet1" at index 0
print(f'New spreadsheet "{name}" at index {index}')

wb.set_cell_contents(name, 'e2', '12')
# wb.set_cell_contents(name, 'b1', '34')
# wb.set_cell_contents(name, 'c1', '=a1+b1')

# value should be a decimal.Decimal('46')
value = wb.get_cell_contents(name, 'b2')
print("should be 12:", value)