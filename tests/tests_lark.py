
import context
from sheets import *

wb = Workbook()
(_,sheet) = wb.new_sheet()

wb.set_cell_contents(sheet, 'a2', '=$aa$14')
print('value should be None:', wb.get_cell_value(sheet, 'a2'))
