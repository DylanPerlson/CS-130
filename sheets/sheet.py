"""Define Class object, used by the Workbook class."""
import lark

from sheets.cell_error import CellError
# from sheets.dependency_graph import Dependency_graph

from .cell import Cell
from .cell_error import CellError, CellErrorType
from .eval_expressions import RetrieveReferences

MAX_ROW = 475254
MAX_COL = 9999
ERROR_LITERALS = ['#REF!', '#ERROR!', '#CIRCREF!', '#VALUE!', '#DIV/0!', '#NAME?']

# Object class for individual spreadsheet
class Sheet:
    """Sheet object constructor taking in name and workbook"""
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.extent = [0,0]
        self.num_cells = 0
        self.cells = {}

    def _get_col_and_row(self,location):
        """ Helper function to get absolute row/col of inputted location (AD42) """
        # be aware we did this backwards

        for e,i in enumerate(location):
            if i.isdigit():
                row = location[:e]
                #convert row letters to its row number
                temp = 0
                for j in range(1, len(row)+1):
                    temp += (ord(row[-j].lower()) - 96)*(26**(j-1))

                row = temp
                col = int(location[e:])
                break

        return row, col


    def set_cell_contents(self, workbook_instance, location, contents):
        """Set the contents of the specified cell on this sheet."""

        #check if we are trying to get an out of bound cell
        row, col = self._get_col_and_row(location)
        if row > MAX_ROW or col > MAX_COL:
            raise ValueError()

        #update the cell extent
        if row > self.extent[0]:
            self.extent[0] = row
        if col > self.extent[1]:
            self.extent[1] = col


        #stash old cell
        prev_cell = None
        if (row,col) in self.cells:
            prev_cell = self.cells[(row,col)]

        #update cell
        new_cell = Cell(contents)
        self.cells[(row,col)] = new_cell


        sheet_location = self.sheet_name.lower() + '!' + location.lower()

        #add all of the new cells to the master cell dict





        # I believe I did this incorrectly
        for parent_cell in self._retrieve_cell_references(workbook_instance, new_cell.contents):
            parent_cell = parent_cell.lower()
            workbook_instance.children_dict[parent_cell] = []
        workbook_instance.master_cell_dict[sheet_location] = []
        for parent_cell in self._retrieve_cell_references(workbook_instance, new_cell.contents):
            parent_cell = parent_cell.lower()

            workbook_instance.children_dict[parent_cell].append(sheet_location)
            workbook_instance.master_cell_dict[sheet_location].append(parent_cell)





    def get_cell_contents(self, location):
        """Function that gets the contents of the cell."""
        row, col = self._get_col_and_row(location)
        if (row,col) not in self.cells:
            return None
        return self.cells[(row,col)].contents

    def get_cell_value(self, workbook_instance, location):
        """Function that gets the value of the cell."""
        row, col = self._get_col_and_row(location)
        if row > MAX_ROW or col > MAX_COL:
            return CellError(CellErrorType.BAD_REFERENCE, 'bad reference')

        sheet_instance = self
        if (row,col) not in self.cells: #empty cell case
            return None
        else:
            return self.cells[(row,col)].get_cell_value(workbook_instance,sheet_instance, location)

    def _retrieve_cell_references(self, workbook_instance, contents):
        """Helper function that returns the references in a cell's formula."""
        #add none case (Dylan)
        if contents is None:
            return []
        #parser = lark.Lark.open('sheets/formulas.lark', start='formula')
        try:
            formula = workbook_instance.parser.parse(contents)
        except lark.exceptions.LarkError:
            # should not need a parse error here for this current use case (Dylan)
            return []
            # return CellError(CellErrorType.PARSE_ERROR,
            # 'Unable to parse formula',
            # lark.exceptions.LarkError)

        ref = RetrieveReferences(self)
        ref.visit(formula)
        return ref.references
