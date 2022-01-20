'''
import sheets

# test whether we can put something in a cell and get the extend of the sheet, etc.

# Test to ensure workbook initialized properly
test_workbook = sheets.Workbook()

test_workbook.new_sheet('FirstSheet') # the name is FirstSheet
'''

############### CODE FROM THE ASSIGNMENT: ###############

import sheets

print(f'Using sheets engine version 1.0')
# Make a new empty workbook
wb = sheets.Workbook()

# TODO why is empty new sheet not working???????
(index, name) = wb.new_sheet("test")
(id2,name2) = wb.new_sheet("ABC")



\

i,n = wb.new_sheet()
print(n)








print('setting val')
wb.set_cell_contents(name, 'A1',10 )
#print(list(wb.sheets[1].cells.values())[0].value)
print("A1 val:",wb.get_cell_value(name, 'A1'))
print("A2 val:",wb.get_cell_value(name, 'A2'))
wb.set_cell_contents(name, 'A3',"=A2+A1" )


# value should be a decimal.Decimal('46')
val = wb.get_cell_value(name, 'A3')
cont = wb.get_cell_contents(name, 'A3')
print("value:", val)
print("contents:", cont)

print('extent:',wb.get_sheet_extent(name))
