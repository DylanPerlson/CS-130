from collections import defaultdict
from sheets.cell_error import CellError
import lark
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
        self.cell_graph = defaultdict(list)
    
    def add_cell_dependency(self,u,v):
        """
        function to add an edge to graph
        Need to call this if formula is updated to reference another cell
        """

        (self.cells[u]).append(v)

    def DFSUtil(self,v,visited):
        """
        A function used by DFS
        Multi phase evaluation phase
        Check all dependencies is one step, Update graph afterwards
        Start updating cells
        """

        # Mark the current node as visited and print it
        visited[v]= True

        #Recur for all the vertices adjacent to this vertex
        for i in self.cells[v]:
            if visited[i]==False:
                self.DFSUtil(i,visited)


    def fill_order(self,v,visited, stack):
        """ Mark the current node as visited """ 

        visited[v]= True
        #Recur for all the vertices adjacent to this vertex
        for i in self.cell_graph[v]:
            if visited[i]==False:
                self.fill_order(i, visited, stack)
        stack = stack.append(v)
    
    def get_transpose(self):
        """ Function that returns reverse (or transpose) of this graph """

        g = Sheet(self.sheet_name, self.parent_workbook)
        g.num_cells = self.num_cells

        # Recur for all the vertices adjacent to this vertex
        for i in self.cell_graph:
            for j in self.cell_graph[i]:
                g.add_cell_dependency(j,i)
        return g

    def print_sccs(self):
        """
        The main function that finds and prints all strongly
        connected components whilst performing topological sort
        """
        
        circ_ref_cells = []
        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited = [False] * (self.num_cells)
        # Fill vertices in stack according to their finishing times
        for i in range(self.cells):
            if visited[i]==False:
                self.fill_order(i, visited, stack)

        # Create a reversed graph
        gr = self.get_transpose()
         
        # Mark all the vertices as not visited (For second DFS)
        visited = [False] * (self.num_cells)

         # Now process all vertices in order defined by Stack
        while stack:
            i = stack.pop()
            if visited[i]==False:
                gr.DFSUtil(i, visited)
                circ_ref_cells.append(i)
        # Want to find all cycles,
        # When you update a single cell, only that single cell's dependencies changes
        # Topological order starting at A1
        # At any given time, graph updates based around one location
        # Suppose A1 =A2 A3 =A2
        # user inputs something for A2
        # lame way: loop through all cells to determine loop
        # Better way: Have edge from A2 to A1, A3
        # If A2 updates, you know what cells need to be updated
        # Every Cell store edges of cells that rely on it
        # Propogate changes out from that node

        self.parent_workbook.del_sheet(self.sheet_name)
        #If circular reference, only update cell VALUE to CIRCREF! error, not update contents
        for curr_cell in circ_ref_cells:
            self.set_cell_contents(curr_cell, CellError(CellErrorType.CIRCULAR_REFERENCE, "#CIRC_REF!", "None"))
        for curr_cell in self.cells:
            self[curr_cell].get_value_from_contents(self[curr_cell].contents)

    def get_row_and_col(self,location):
        """ Helper function to get absolute row/col of inputted location """
        
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
        
        if not (row,col) in self.cells.keys():
            self.cells[(row,col)] = Cell(contents)
        else:
            self.cells[(row,col)].contents = contents # TODO maybe make a new Cell object here
        # self.cells[(row,col)] = contents
        # self.printSCCs()

        # these if functions prevent problems with non-formulas
        if contents != None:
            if contents[0] == '=' and contents[1] != '?': # self.cells[(row,col)].type == "FORMULA":
                # example: print(self.retrieve_cell_references(contents))
                pass

    def get_cell_contents(self, location):
        row, col = self.get_row_and_col(location)
        if (row,col) not in self.cells.keys():
            return None;
        return self.cells[(row,col)].contents 

    def get_cell_value(self, workbook_instance, location):
        row, col = self.get_row_and_col(location)
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
        



   

        
 