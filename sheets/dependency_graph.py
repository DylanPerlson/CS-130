from collections import defaultdict
from platform import node
from weakref import ref

from sklearn.decomposition import DictionaryLearning
from sheets.cell_error import CellError
from .cell import Cell
from .cell_error import CellError, CellErrorType

class DependencyGraph:
    def __init__(self, num_nodes = 0):
        # Initialize a new dependency graph
        self.graph = defaultdict(list)
        self.num_nodes = num_nodes

    # function to add an edge to graph
    def add_edge(self,u,v):
        if u not in self.graph.keys() and u not in self.graph.values():
            self.num_nodes += 1
        if v not in self.graph.keys() and v not in self.graph.values():
            self.num_nodes += 1
        self.graph[u].append(v)
 
    # A recursive function used by topologicalSort
    def topological_sort_util(self,v,visited,stack):
        # Mark the current node as visited.
        visited[v] = True
 
        # Recur for all the cells adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Push current vertex to stack which stores result
        stack.insert(0,v)
 
    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topological_sort(self):
        # Mark all the vertices as not visited
        visited = [False]*self.num_nodes
        stack =[]
 
        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.num_nodes):
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Print contents of stack
        return stack
    
# create a new Dictionary   
# with all the keys from master cell dict 


# visited_dict = curly
# for key in master_cell_dict.keys:
#     visited_dict[key] = False

#     pick the current node we are getting the value from as the starting node 
#     do a dfs on the start node 

#     and at every node mark visited dict to true  

#     if we ever reach a visited dict that is true 

#     then return circ ref

#     or if we run out of nodes to search, then we also end return not circ ref



    # def DFSUtil(self,v,visited):
    #     """
    #     A function used by DFS
    #     Multi phase evaluation phase
    #     Check all dependencies is one step, Update graph afterwards
    #     Start updating cells
    #     """

    #     # Mark the current node as visited and print it
    #     visited[v]= True

    #     #Recur for all the vertices adjacent to this vertex
    #     for i in self.cells[v]:
    #         if visited[i]==False:
    #             self.DFSUtil(i,visited)


    # def fill_order(self,v,visited, stack):
    #     """ Mark the current node as visited """ 

    #     visited[v]= True
    #     #Recur for all the vertices adjacent to this vertex
    #     for i in self.cell_graph[v]:
    #         if visited[i]==False:
    #             self.fill_order(i, visited, stack)
    #     stack = stack.append(v)
    
    # def get_transpose(self):
    #     """ Function that returns reverse (or transpose) of this graph """

    #     g = Sheet(self.sheet_name, self.parent_workbook)
    #     g.num_cells = self.num_cells

    #     # Recur for all the vertices adjacent to this vertex
    #     for i in self.cell_graph:
    #         for j in self.cell_graph[i]:
    #             g.add_cell_dependency(j,i)
    #     return g

    # def print_sccs(self):
    #     """
    #     The main function that finds and prints all strongly
    #     connected components whilst performing topological sort
    #     """
        
    #     circ_ref_cells = []
    #     stack = []
    #     # Mark all the vertices as not visited (For first DFS)
    #     visited = [False] * (self.num_cells)
    #     # Fill vertices in stack according to their finishing times
    #     for i in range(self.cells):
    #         if visited[i]==False:
    #             self.fill_order(i, visited, stack)

    #     # Create a reversed graph
    #     gr = self.get_transpose()
         
    #     # Mark all the vertices as not visited (For second DFS)
    #     visited = [False] * (self.num_cells)

    #      # Now process all vertices in order defined by Stack
    #     while stack:
    #         i = stack.pop()
    #         if visited[i]==False:
    #             gr.DFSUtil(i, visited)
    #             circ_ref_cells.append(i)
    #     # Want to find all cycles,
    #     # When you update a single cell, only that single cell's dependencies changes
    #     # Topological order starting at A1
    #     # At any given time, graph updates based around one location
    #     # Suppose A1 =A2 A3 =A2
    #     # user inputs something for A2
    #     # lame way: loop through all cells to determine loop
    #     # Better way: Have edge from A2 to A1, A3
    #     # If A2 updates, you know what cells need to be updated
    #     # Every Cell store edges of cells that rely on it
    #     # Propogate changes out from that node

    #     self.parent_workbook.del_sheet(self.sheet_name)
    #     #If circular reference, only update cell VALUE to CIRCREF! error, not update contents
    #     for curr_cell in circ_ref_cells:
    #         self.set_cell_contents(curr_cell, CellError(CellErrorType.CIRCULAR_REFERENCE, "#CIRC_REF!", "None"))
    #     for curr_cell in self.cells:
    #         self[curr_cell].get_value_from_contents(self[curr_cell].contents)