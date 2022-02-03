import os; os.system('cls')
import context
from sheets import *
import decimal
import unittest

class TestWorkbook(unittest.TestCase):
    def test_long_reference_chain(self):
        wb = Workbook()

        (_,name) = wb.new_sheet("sheet")
        wb.set_cell_contents(name, 'A1', '1')
        
        for i in range(1, 150):
            location_letter = wb.base_10_to_alphabet(i)
            location_letter_prev = wb.base_10_to_alphabet(i-1)
            location = str(location_letter)+str(1)

            wb.set_cell_contents(name, location, '=1+'+str(location_letter_prev)+str(1))

            if i%25 == 0:
                print(wb.get_cell_value(name, str(location_letter)+str(1)))

        # print(wb.get_cell_contents(name, 'A1'))
        # print(wb.get_cell_contents(name, 'BA1'))
        # print(wb.get_cell_value(name, 'BA1'))
        # print(wb.get_cell_contents(name, 'ALK1'))
        # print(wb.get_cell_value(name, 'ALK1'))




if __name__ == '__main__':
    unittest.main(verbosity=1)