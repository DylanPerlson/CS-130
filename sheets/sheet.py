from collections import defaultdict
from sheets.cell_error import CellError
import lark

from sheets.dependency_graph import Dependency_graph
from .eval_expressions import RetrieveReferences
from .cell import Cell
from .cell_error import CellError, CellErrorType

MAX_ROW = 475254
MAX_COL = 9999

# Object class for individual spreadsheet
class Sheet:
    # Sheet object constructor taking in name and workbook
    def __init__(self, sheet_name):         
        self.sheet_name = sheet_name
        self.extent = [0,0]
        self.num_cells = 0
        self.cells = {}
        self.dependent_cells = Dependency_graph()
        self.parent_workbook = None

    def get_row_and_col(self,location):
        """ Helper function to get absolute row/col of inputted location (AD42) """
        
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

    def get_dependent_cells(self, row, col, contents):
        dependent_cell_dict = {}
        # these if functions prevent problems with non-formulas
        curr_cell = self.cells[(row,col)]
        if contents != None:
            if contents[0] == '=' and contents[1] != '?': # self.cells[(row,col)].type == "FORMULA":
                # example: print(self.retrieve_cell_references(contents))
                dependent_cells = self.retrieve_cell_references(contents)
                if curr_cell.contents in dependent_cells:
                    pass
                for cell in dependent_cells:
                    #This part needs some thinking through
                    #Need to check if old value and new values differ before adding to changed cells notification
                    value = cell.get_cell_value(self.sheet_name, self.get_row_and_col(cell))
                    dependent_cell_dict[(row,col)].append(value)

    def set_cell_contents(self, location, contents):
        # extract the row and col numbers from the letter-number location
        row, col = self.get_row_and_col(location)
        if row > MAX_ROW or col > MAX_COL:
            raise ValueError
        # in case the new cell is beyond the extent
        if(row > self.extent[0]):
            self.extent[0] = row
        if(col > self.extent[1]):
            self.extent[1] = col
        
        #Get old values of dependent cells before updating and recalculating
        if contents != None:
            if contents[0] == '=' and contents[1] != '?':
                old_dependent_values = self.get_dependent_cells(row,col,contents)
        
        if not (row,col) in self.cells.keys():
            self.cells[(row,col)] = Cell(contents)
        else:
            self.cells[(row,col)].contents = contents # TODO maybe make a new Cell object here

        # these if functions prevent problems with non-formulas
        updated_cells = {}
        curr_cell = self.cells[(row,col)]
        if contents != None:
            if contents[0] == '=' and contents[1] != '?': # self.cells[(row,col)].type == "FORMULA":
                # example: print(self.retrieve_cell_references(contents))
                dependent_cells = self.retrieve_cell_references(contents)
                if curr_cell.contents in dependent_cells:
                    #update all cells with circular reference here
                    pass
                for cell in dependent_cells:
                    #This part needs some thinking through
                    #Need to check if old value and new values differ before adding to changed cells notification
                    val = cell.get_cell_value(self.sheet_name, self.get_row_and_col(cell))
                    if val not in old_dependent_values[cell].values():
                        updated_cells[self.sheet_name].append('''Get dependent cell location here''')
                        continue
        
        #return updated_cells
        
             

    def get_cell_contents(self, location):
        row, col = self.get_row_and_col(location)
        if (row,col) not in self.cells.keys():
            return None
        return self.cells[(row,col)].contents 

    def get_cell_value(self, workbook_instance, location):
        row, col = self.get_row_and_col(location)
        if row > MAX_ROW or col > MAX_COL:
            return CellError(CellErrorType.BAD_REFERENCE, 'bad reference')

        sheet_instance = self
        if (row,col) not in self.cells.keys(): #empty cell case
            return None
        else:
            return self.cells[(row,col)].get_cell_value(workbook_instance,sheet_instance) 

    def retrieve_cell_references(self, contents):
        """ helper function that returns the references in a cell's formula """
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')
        formula = parser.parse(contents)
        ref = RetrieveReferences(self)
        ref.visit(formula)
        return ref.references
        
