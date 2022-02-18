from sheets.cell_error import CellError
import lark
from .eval_expressions import RetrieveReferences
from .cell import Cell
from .cell_error import CellError, CellErrorType

MAX_ROW = 475254
MAX_COL = 9999
ERROR_LITERALS = ['#REF!', '#ERROR!', '#CIRCREF!', '#VALUE!', '#DIV/0!', '#NAME?']

# Object class for individual spreadsheet
class Sheet:
    # Sheet object constructor taking in name and workbook
    def __init__(self, sheet_name):         
        self.sheet_name = sheet_name
        self.extent = [0,0]
        self.num_cells = 0
        self.cells = {}
        self.parent_workbook = None

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
        #first we need to remove any parent dependents if it exists
        row, col = self._get_col_and_row(location)
        if row > MAX_ROW or col > MAX_COL:
            raise ValueError()
        # in case the new cell is beyond the extent
        if(row > self.extent[0]):
            self.extent[0] = row
        if(col > self.extent[1]):
            self.extent[1] = col

        if (row,col) in self.cells:
            curr_cell = self.cells[(row,col)]
            if curr_cell.type == "FORMULA":
                prev_contents = curr_cell.contents
                #notify parent cells to remove this cell from their dependents list
                for parent_cell in self._retrieve_cell_references(prev_contents):
                    # reminder our rows and cols are switch, but we need to keep it this way                    
                    #remove current cell
                    removing_entry = self.sheet_name.lower() + '!' + location
                    
                    workbook_instance.master_cell_dict[(parent_cell)].remove(removing_entry)
        
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
                    if parent_cell not in workbook_instance.master_cell_dict:
                        workbook_instance.master_cell_dict[(parent_cell)] = []

                    appending_entry = self.sheet_name.lower()  + '!' + location
                    workbook_instance.master_cell_dict[(parent_cell)].append(appending_entry)
        
        
    def get_cell_contents(self, location):
        row, col = self._get_col_and_row(location)
        if (row,col) not in self.cells.keys():
            return None
        return self.cells[(row,col)].contents 

    def get_cell_value(self, workbook_instance, location):
        row, col = self._get_col_and_row(location)
        if row > MAX_ROW or col > MAX_COL:
            return CellError(CellErrorType.BAD_REFERENCE, 'bad reference')

        sheet_instance = self
        if (row,col) not in self.cells.keys(): #empty cell case
            return None
        else:
            return self.cells[(row,col)].get_cell_value(workbook_instance,sheet_instance) 

    def _retrieve_cell_references(self, contents):
        """ helper function that returns the references in a cell's formula """
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')
        try:
            formula = parser.parse(contents)
        except:
            return CellError(CellErrorType.PARSE_ERROR, 'Unable to parse formula' ,'Parse Error')
        ref = RetrieveReferences(self)
        ref.visit(formula)
        return ref.references
        
