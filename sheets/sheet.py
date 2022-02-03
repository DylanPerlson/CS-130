from collections import defaultdict
from sheets.cell_error import CellError
import lark
from sheets.dependency_graph import Dependency_graph
from .eval_expressions import RetrieveReferences
from .cell import Cell
from .cell_error import CellError, CellErrorType

MAX_ROW = 475254
MAX_COL = 9999
master_cell_dict = {}

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

    def get_dependent_cells(self, row, col, location, contents):
        dependent_cell_dict = {}
        # these if functions prevent problems with non-formulas
        if contents != None:
            if contents[0] == '=' and contents[1] != '?': # self.cells[(row,col)].type == "FORMULA":
                # example: print(self.retrieve_cell_references(contents))
                curr_cell = self.cells[(row,col)]
                parent_cells = self.retrieve_cell_references(contents)
                #print(parent_cells)
                if curr_cell in parent_cells:
                    #set circular reference error here
                    pass
                for curr_parent_cell in parent_cells:
                    split_cell_string = curr_parent_cell.split('!')
                    val = self.get_cell_value(split_cell_string[0], split_cell_string[1])
                    depend_row, depend_col = self.get_row_and_col(split_cell_string[1])
                    temp_tuple = (split_cell_string[0],depend_row,depend_col)
                    if curr_parent_cell not in curr_cell.parent_cells:
                        curr_cell.parent_cells[temp_tuple] = val
                    curr_cell_string = self.sheet_name + "!" + str(location)

                    
#                    if curr_cell_string not in master_cell_dict[temp_tuple].get_children_cells():
 #                       master_cell_dict[temp_tuple].add_child_cell(curr_cell_string, contents)

                    dependent_cell_dict[(split_cell_string[0],depend_row,depend_col)] = val
        return dependent_cell_dict

    def set_cell_contents(self, workbook_instance, location, contents):
        # extract the row and col numbers from the letter-number location
        row, col = self.get_row_and_col(location)
        if row > MAX_ROW or col > MAX_COL:
            raise ValueError
        # in case the new cell is beyond the extent
        if(row > self.extent[0]):
            self.extent[0] = row
        if(col > self.extent[1]):
            self.extent[1] = col
        
        self.cells[(row,col)] = Cell(contents) # if statement is old code; we need to update a cell entirely
        # if not in the master dictionary
        if (self.sheet_name,row,col) not in master_cell_dict:
            master_cell_dict[(self.sheet_name,row,col)] = self.cells[(row,col)]
        updated_cells = {}
        curr_cell = self.cells[(row,col)]
        
        # Parse formula based on parent nodes
        if self.cells[(row,col)].type == "FORMULA":
            # example: print(self.retrieve_cell_references(contents))
            parent_cells = self.retrieve_cell_references(contents)
            if isinstance(parent_cells, CellError):
                return
            elif curr_cell in parent_cells:
                #update all cells with circular reference here
                pass
            for cell in parent_cells:
                #Need to check if old value and new values differ before adding to changed cells notification
                parent_cells_dict = self.get_dependent_cells(row,col,location, contents)
                split_cell_string = cell.split('!')
                val = self.get_cell_value(split_cell_string[0], split_cell_string[1])
                depend_row, depend_col = self.get_row_and_col(split_cell_string[1])
                if val != parent_cells_dict[(split_cell_string[0],depend_row,depend_col)]:
                    updated_cells[self.sheet_name] = split_cell_string[1]
        
        #If not a formula, update children node that depend on this cell
        children_cells = self.cells[(row,col)].get_children_cells()
        for curr_child_cell in children_cells:
            curr_child_cell.get_cell_value(workbook_instance, self)
            updated_cells[self.sheet_name].append(curr_child_cell)
        return updated_cells
        
             

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
        try:
            formula = parser.parse(self.contents)
        except:
            return CellError(CellErrorType.PARSE_ERROR, 'Unable to parse formula' ,'Parse Error')
        ref = RetrieveReferences(self)
        ref.visit(formula)
        return ref.references
        
