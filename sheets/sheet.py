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

        #first we need to remove any parent dependents if it exists
        row, col = self._get_col_and_row(location)
        if row > MAX_ROW or col > MAX_COL:
            raise ValueError()

        if row > self.extent[0]:
            self.extent[0] = row
        if col > self.extent[1]:
            self.extent[1] = col

        if (row,col) in self.cells:
            curr_cell = self.cells[(row,col)]
            if curr_cell.type == "FORMULA":
                prev_contents = curr_cell.contents
                #notify parent cells to remove this cell from their dependents list
                #parent_cell sheet_name!A1
                for parent_cell in self._retrieve_cell_references(prev_contents):
                    # reminder our rows and cols are switch, but we need to keep it this way                    
                    #remove current cell
                    removing_entry = self.sheet_name.lower() + '!' + location

                    workbook_instance.master_cell_dict[(parent_cell.lower())].remove(removing_entry.lower())

        self.cells[(row,col)] = Cell(contents)


        #notify the parent cells to add this cell as a dependent
        curr_cell = self.cells[(row,col)]
        if curr_cell in ERROR_LITERALS:
            return
        elif curr_cell.type == "FORMULA":
            prev_contents = curr_cell.contents
            parent_cells = self._retrieve_cell_references(prev_contents)
            if isinstance(parent_cells, CellError):
                return
            else:
                #notify parent cells to remove this cell from their dependents list
                for parent_cell in parent_cells:
                    # reminder our rows and cols are switch, but we need to keep it this way
                    #add current cell

                    #create the list if it does not exist
                    if parent_cell.lower() not in workbook_instance.master_cell_dict:
                        workbook_instance.master_cell_dict[(parent_cell.lower())] = []

                    appending_entry = self.sheet_name.lower()  + '!' + location
                    workbook_instance.master_cell_dict[(parent_cell.lower())].append(appending_entry.lower())
        
        
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

    def _retrieve_cell_references(self, contents):
        """Helper function that returns the references in a cell's formula."""
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')
        try:
            formula = parser.parse(contents)
        except lark.exceptions.LarkError:
            return CellError(CellErrorType.PARSE_ERROR,
            'Unable to parse formula',
            lark.exceptions.LarkError)

        ref = RetrieveReferences(self)
        ref.visit(formula)
        return ref.references
