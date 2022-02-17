#from collections import defaultdict
#from locale import ABDAY_1
#from posixpath import split
from sheets.cell_error import CellError
import lark
#from sheets.dependency_graph import DependencyGraph
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

    # def _get_dependent_cells(self, row, col, location, contents):
    #     dependent_cell_dict = {}
    #     # these if functions prevent problems with non-formulas
    #     if contents is not None:
    #         if contents[0] == '=' and contents[1] != '?': # self.cells[(row,col)].type == "FORMULA":
    #             # example: print(self._retrieve_cell_references(contents))
    #             curr_cell = self.cells[(row,col)]
    #             parent_cells = self._retrieve_cell_references(contents)
    #             #print(parent_cells)
    #             if curr_cell in parent_cells:
    #                 #set circular reference error here
    #                 pass
    #             for curr_parent_cell in parent_cells:
    #                 split_cell_string = curr_parent_cell.split('!')
    #                 val = self.get_cell_value(split_cell_string[0], split_cell_string[1])
    #                 depend_row, depend_col = self._get_col_and_row(split_cell_string[1])
    #                 temp_tuple = (split_cell_string[0],depend_row,depend_col)
    #                 if curr_parent_cell not in curr_cell.parent_cells:
    #                     curr_cell.parent_cells[temp_tuple] = val
    #                 curr_cell_string = self.sheet_name + "!" + str(location)

                    
#                    if curr_cell_string not in master_cell_dict[temp_tuple].get_children_cells():
 #                       master_cell_dict[temp_tuple].add_child_cell(curr_cell_string, contents)

        #             dependent_cell_dict[(split_cell_string[0],depend_row,depend_col)] = val
        # return dependent_cell_dict

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
        if curr_cell.type == "FORMULA":
            prev_contents = curr_cell.contents
            #notify parent cells to remove this cell from their dependents list
            for parent_cell in self._retrieve_cell_references(prev_contents):
                # reminder our rows and cols are switch, but we need to keep it this way                    
                #add current cell
                
                #create the list if it does not exist
                if parent_cell not in workbook_instance.master_cell_dict:
                    workbook_instance.master_cell_dict[(parent_cell)] = []

                appending_entry = self.sheet_name.lower()  + '!' + location
                workbook_instance.master_cell_dict[(parent_cell)].append(appending_entry)


        #now we notify all of our own children that we have been updated

        # notify A1 to remove this cell from its dependents list

        # new contents = A2
        # then we notify A2 to remove this cell from its dependent list


        # then once everything has been updated we notify all of our own dependents
        #before we add anything to the dpendents list of other cells, 


        # if there are any depencies, then we add those dependencies to those cells list of dependents

        #

        #one all of this is updated, then we notify all of our dependent cells in our current list using the functions we are given






        # if (self.sheet_name,row,col) not in workbook_instance.master_cell_dict:
        #     workbook_instance.master_cell_dict[(self.sheet_name,row,col)] = []
        #     for curr_cell in self._retrieve_cell_references(contents):
        #         workbook_instance.master_cell_dict[(self.sheet_name,row,col)].append(curr_cell)
    
        
        # # Parse formula based on parent nodes
        # if self.cells[(row,col)].type == "FORMULA":
        #     # example: print(self._retrieve_cell_references(contents))
        #     parent_cells = self._retrieve_cell_references(contents)
        #     if isinstance(parent_cells, CellError):
        #         return
        #     elif curr_cell in parent_cells:
        #         #update all cells with circular reference here
        #         pass
        #     for cell in parent_cells:
        #         #Need to check if old value and new values differ before adding to changed cells notification
        #         parent_cells_dict = self._get_dependent_cells(row,col,location, contents)
        #         split_cell_string = cell.split('!')
        #         val = self.get_cell_value(split_cell_string[0], split_cell_string[1])
        #         depend_row, depend_col = self._get_col_and_row(split_cell_string[1])
        #         if val != parent_cells_dict[(split_cell_string[0],depend_row,depend_col)]:
        #             updated_cells[self.sheet_name] = split_cell_string[1]
        
        # #If not a formula, update children node that depend on this cell
        # children_cells = self.cells[(row,col)].get_children_cells()
        # for curr_child_cell in children_cells:
        #     curr_child_cell.get_cell_value(workbook_instance, self)
        #     updated_cells[self.sheet_name].append(curr_child_cell)
        # return updated_cells
        
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
        
