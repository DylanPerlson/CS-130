from .cell import Cell

# Object class for individual spreadsheet
class Sheet:
    # Sheet object constructor taking in name and workbook
    def __init__(self, sheet_name, curr_workbook):         
        self.sheet_name = sheet_name
        self.extent = [0,0]
        self.cells = {}
    
    #Helper function to get absolute row/col of inputted location
    def get_row_and_col(self,location):
        print(location)
        for e,i in enumerate(location):
            # print(i)
            if i.isdigit():
                row = location[:e]
                
                #convert column letters to its column number
                temp = 0
                for j in range(1, len(row)):
                    print(j   )
                    temp += (ord(row[-j].lower()) - 96)#**j
                    print(temp)
                row = temp

                col = int(location[e:])
                print(row)
                print(col)
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
        
        if not self.cells.has_key((row,col)):
            self.cells[(row,col)] = Cell(contents, self)
        else:
            self.cells[(row,col)].contents = contents

        # TODO has incorrect locations etc. been taken care of? I think it has been

    def get_cell_contents(self, location):

        row, col = self.get_row_and_col(location)
        return self.cells[(row,col)].get_cell_contents() # TODO has this function been made?

    def get_cell_value(self, location):
    
        row, col = self.get_row_and_col(location)
        return self.cells[(row,col)].get_cell_value() # TODO has this function been made?



   

        
 