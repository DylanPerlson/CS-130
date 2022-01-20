from .cell import Cell

# Object class for individual spreadsheet
class Sheet:
    # Sheet object constructor taking in name and workbook
    def __init__(self, sheet_name):         
        self.sheet_name = sheet_name
        self.extent = [0,0]
        self.cells = {}
    
    #Helper function to get absolute row/col of inputted location
    def get_row_and_col(self,location):
        
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
        row, col = self.get_row_and_col(location) # TODO is this correct?
        
        # in case the new cell is beyond the extent
        if(row > self.extent[0]):
            self.extent[0] = row
        if(col > self.extent[1]):
            self.extent[1] = col
        
        if not (row,col) in self.cells.keys():
            self.cells[(row,col)] = Cell(contents)# TODO why are we sending in self to CELL?
        else:
            self.cells[(row,col)].contents = contents

        # TODO has incorrect locations etc. been taken care of? I think it has been

    def get_cell_contents(self, location):

        row, col = self.get_row_and_col(location)
        return self.cells[(row,col)].contents 

    def get_cell_value(self, workbook_instance, location):
        row, col = self.get_row_and_col(location)
        sheet_instance = self
        return self.cells[(row,col)].get_cell_value(workbook_instance,sheet_instance) 
        # TODO has this function been made?



   

        
 