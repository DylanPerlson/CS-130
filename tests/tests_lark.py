
import context
from sheets import *

wb = Workbook()
(_,sheet) = wb.new_sheet()

wb.set_cell_contents(sheet, 'a1', '=2')
wb.set_cell_contents(sheet, 'a2', '=$a$1')

assert wb.get_cell_value(sheet, 'a2') == 2
# print('value should be 2:', wb.get_cell_value(sheet, 'a2'))
