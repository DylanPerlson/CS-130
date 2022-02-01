
from logging import exception
from multiprocessing.sharedctypes import Value # TODO do we need these

from sheets.cell_error import CellError, CellErrorType
from .sheet import Sheet
MAX_ROW = 475254
MAX_COL = 9999
class Workbook:
    import decimal
    # A workbook containing zero or more named spreadsheets.
    #
    # Any and all operations on a workbook that may affect calculated cell
    # values should cause the workbook's contents to be updated properly.

    #decimal, error code
    def __init__(self):
        # Initialize a new empty workbook.
        self.sheets = []
        self.num_sheets = 0
        self.allowed_characters = ".?!,:;!@#$%^&*()-_ "
        self.needs_quotes = ".?!,:;!@#$%^&*()- "
        

    def num_sheets(self) -> int:
        # Return the number of spreadsheets in the workbook.
        return self.num_sheets
       

    def list_sheets(self): # list
        """
        Return a list of the spreadsheet names in the workbook, with the
        capitalization specified at creation, and in the order that the sheets
        appear within the workbook.
        
        In this project, the sheet names appear in the order that the user
        created them; later, when the user is able to move and copy sheets,
        the ordering of the sheets in this function's result will also reflect
        such operations.
        
        A user should be able to mutate the return-value without affecting the
        workbook's internal state.
        """

        name_list = []

        for i in self.sheets:
            name_list.append(i.sheet_name)
        
        return name_list

    def new_sheet(self, sheet_name: str = None):
        """
        Add a new sheet to the workbook.  If the sheet name is specified, it
        must be unique.  If the sheet name is None, a unique sheet name is
        generated.  "Uniqueness" is determined in a case-insensitive manner,
        but the case specified for the sheet name is preserved.
        
        The function returns a tuple with two elements:
        (0-based index of sheet in workbook, sheet name).  This allows the
        function to report the sheet's name when it is auto-generated.
        
        If the spreadsheet name is an empty string (not None), or it is
        otherwise invalid, a ValueError is raised.
        """

        name_given = False
        #check for invalid strings
       
        if (sheet_name == ""): 
            raise ValueError   
        
        #if no name given
        if sheet_name == None:
            name_given = True
            auto_name = "Sheet"
            sheet_name = auto_name + str(self.create_name())
            new_sheet = Sheet(sheet_name)
        
        
        # no leading or trailing white space allowed
        if sheet_name[0] == " " or sheet_name[-1] == " ": 
            raise ValueError   

        for i in sheet_name:
            if not i.isalnum() and not i in self.allowed_characters:
                raise ValueError


        #cannot already be taken
        if name_given == False:
            for i in self.sheets:
                if i.sheet_name.lower() == sheet_name.lower():
                    raise ValueError
            else:
                new_sheet = Sheet(sheet_name)

        self.num_sheets += 1 
        self.sheets.append(new_sheet)

        return (self.num_sheets-1, sheet_name) # '-1' is because index should start at 0

      
        

    def del_sheet(self, sheet_name: str):
        """
        Delete the spreadsheet with the specified name.
        
        The sheet name match is case-insensitive; the text must match but the
        case does not have to.
        
        If the specified sheet name is not found, a KeyError is raised.
        """
        
        all_sheet_names = []
        for i in range(len(self.sheets)):
            all_sheet_names.append(self.sheets[i].sheet_name.lower())
        
        if sheet_name not in all_sheet_names:
            raise KeyError
        try:
            for i in range(len(self.sheets)):
                #remove the sheet with sheet_name
                curr_sheet = self.sheets[i]
                if curr_sheet.sheet_name.lower() == sheet_name.lower():
                    self.sheets.remove(curr_sheet)
                    self.num_sheets -= 1
                    return
        except KeyError as e:
            raise
       

    

    def get_sheet_extent(self, sheet_name: str):
        """
        Return a tuple (num-cols, num-rows) indicating the current extent of
        the specified spreadsheet.
        
        The sheet name match is case-insensitive; the text must match but the
        case does not have to.
        
        If the specified sheet name is not found, a KeyError is raised.
        """
        
      
        
        # new code for getting the extent
        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                i.extent = [0,0]
                for key in i.cells:
                    if i.cells[key].contents is not None and key[0] > i.extent[0]:
                        i.extent[0] = key[0]
                    if i.cells[key].contents is not None and key[1] > i.extent[1]:
                        i.extent[1] = key[1]
                return (i.extent[0],i.extent[1])


        #if sheet name not found, raise key error
        raise KeyError





    def set_cell_contents(self, sheet_name: str, location: str,
                          contents: 'None'):
        """
        Set the contents of the specified cell on the specified sheet.
        
        The sheet name match is case-insensitive; the text must match but the
        case does not have to.  Additionally, the cell location can be
        specified in any case.
        
        If the specified sheet name is not found, a KeyError is raised.
        If the cell location is invalid, a ValueError is raised.
        
        A cell may be set to "empty" by specifying a contents of None.
        
        Leading and trailing whitespace are removed from the contents before
        storing them in the cell.  Storing a zero-length string "" (or a
        string composed entirely of whitespace) is equivalent to setting the
        cell contents to None.
        
        If the cell contents appear to be a formula, and the formula is
        invalid for some reason, this method does not raise an exception;
        rather, the cell's value will be a CellError object indicating the
        naure of the issue.
        """
        
        for i in self.sheets:
            #edit cell content of specified sheet
            if (i.sheet_name == None):
                continue
            if not self.check_valid_cell(location):
                raise ValueError
            
            if i.sheet_name.lower() == sheet_name.lower():
                #self.check_valid_cell(location)
                #if want to set cell contents to empty
                if contents == None or (not self.is_float(contents) and contents.strip() == ''):
                    i.set_cell_contents(location, None)
                elif self.is_float(contents):
                    i.set_cell_contents(location, contents)
                else: #store normally
                    i.set_cell_contents(location, contents.strip())
                #completed task
                return
               
        #no sheet found
        raise KeyError
        

    def get_cell_contents(self, sheet_name: str, location: str):
        """
        Return the contents of the specified cell on the specified sheet.
        
        The sheet name match is case-insensitive; the text must match but the
        case does not have to.  Additionally, the cell location can be
        specified in any case.
        
        If the specified sheet name is not found, a KeyError is raised.
        If the cell location is invalid, a ValueError is raised.
        
        Any string returned by this function will not have leading or trailing
        whitespace, as this whitespace will have been stripped off by the
        set_cell_contents() function.
        
        This method will never return a zero-length string; instead, empty
        cells are indicated by a value of None.
        """
        if not self.check_valid_cell(location):
            raise ValueError

        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                self.check_valid_cell(location)
                return i.get_cell_contents(location)

        raise ValueError


    def get_cell_value(self, sheet_name: str, location: str):
        """
        Return the evaluated value of the specified cell on the specified
        sheet.
        
        The sheet name match is case-insensitive; the text must match but the
        case does not have to.  Additionally, the cell location can be
        specified in any case.
        
        If the specified sheet name is not found, a KeyError is raised.
        If the cell location is invalid, a ValueError is raised.
        
        The value of empty cells is None.  Non-empty cells may contain a
        value of str, decimal.Decimal, or CellError.
        
        Decimal values will not have trailing zeros to the right of any
        decimal place, and will not include a decimal place if the value is a
        whole number.  For example, this function would not return
        Decimal('1.000'); rather it would return Decimal('1').
        """
        row,col = self.get_row_and_col(location)
        if row > MAX_ROW or col > MAX_COL:
            return CellError(CellErrorType.BAD_REFERENCE, 'bad reference')

        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                self.check_valid_cell(location)
                workbook_instance = self
                return i.get_cell_value(workbook_instance,location) 
            
        raise KeyError




    def check_valid_cell (self, location):
        """ Check if the cell location is valid """    
        if not location.isalnum():
            return False
            # raise ValueError
            
        digits = False
        for c in location:
            if not c.isdigit() and digits == False: 
                continue
            elif c.isdigit() and digits == False:
                digits = True
            elif c.isdigit() and digits == True:
                continue
            elif c == ' ':
                return False
            else:
                return False 
                # raise ValueError
        
        for c in range(len(location)-1):
            if not location[c+1].isdigit() and location[c].isdigit():
                return False

        return True

    def create_name(self,num = 1):
        """ finds an unused name """

        auto_name = "Sheet"
       
        for i in self.sheets:
            if i.sheet_name == auto_name + str(num):              
                return self.create_name(num + 1)
                
        return num

    def rename_sheet(self, sheet_name, new_sheet_name):
        old_name = sheet_name
        new_name = new_sheet_name
        # Rename the specified sheet to the new sheet name.  Additionally, all
        # cell formulas that referenced the original sheet name are updated to
        # reference the new sheet name (using the same case as the new sheet
        # name, and single-quotes iff [if and only if] necessary).
        #
        # The sheet_name match is case-insensitive; the text must match but the
        # case does not have to.
        #
        # As with new_sheet(), the case of the new_sheet_name is preserved by
        # the workbook.
        #
        # If the sheet_name is not found, a KeyError is raised.
        #
        # If the new_sheet_name is an empty string or is otherwise invalid, a
        # ValueError is raised.
         #As usual, the new sheet name must be both valid and unique in the workbook; if it is not, an exception is raised. 
         #Also as usual, the case of the new name is preserved by the workbook.
        
        old_name_exists = False
        proper_old_name = None
        
        #check if the workbook name is a valid name
        if (new_name == ""): 
            raise ValueError   
        for i in new_name:
            if not i.isalnum() and not i in self.allowed_characters:
                raise ValueError
        # no leading or trailing white space allowed
        if new_name[0] == " " or new_name[-1] == " ": 
            raise ValueError   
 
       
        # change the name of the sheet
        for i in self.sheets:
            #old name is case insensitive
            if (i.sheet_name.lower() == old_name.lower()):
                proper_old_name = i.sheet_name
                i.sheet_name = new_name
                old_name_exists = True
                break;

        # old name not found
        if (old_name_exists == False):
            raise KeyError
            
        # change the formulas for every cell
        for s in self.sheets:
            for key in s.cells:
                #check if the cell is a formula
                if s.cells[key].type == "FORMULA":
                    #check if the formula contains the old_name
                    if proper_old_name+'!' in s.cells[key].contents:                                  
                        s.cells[key].contents = s.cells[key].contents.replace(proper_old_name+'!',new_name+'!')
                    elif "'"+proper_old_name+"'!" in s.cells[key].contents:
                       
                    
                    #    In fact, if a sheet’s name doesn’t start with an alphabetical 
                    #    character or underscore, or if a sheet’s name contains spaces or 
                    #    any other characters besides “A-Z”, “a-z”, “0-9” or the underscore “_”, 
                    #    it must be quoted to parse correctly. For example: 'Other Totals'!G15
                       
                        # if necessary
                        needed = False
                        for char in self.needs_quotes:
                            if char in new_name:
                                needed = True
                                s.cells[key].contents = s.cells[key].contents.replace("'"+proper_old_name+"'!","'"+new_name+"'!")
                                break
                        if self.is_float(new_name[0]):
                                needed = True
                                s.cells[key].contents = s.cells[key].contents.replace("'"+proper_old_name+"'!","'"+new_name+"'!")
                        if not needed: # not necessary
                            s.cells[key].contents = s.cells[key].contents.replace("'"+proper_old_name+"'!",new_name+'!')

                        
                        #remove other uneccesary '
                        contents_arr = s.cells[key].contents.split("'")
                        remove_apostrophe = []
                        for i in range(len(contents_arr)):
                            #make sure name doesnt start with a !
                            #find where there is a name broken by '
                            if (contents_arr[i][0] == '!' and contents_arr[i-1][0] != '!'):
                                remove_apostrophe.append(contents_arr[i-1])
                        for i in remove_apostrophe:
                            #check if the other equations need quotes
                            needed = False
                            for char in self.needs_quotes:
                                if char in i:
                                    needed = True
                                    break
                            #also needs quotes if starts with a number
                            if self.is_float(i[0]):
                                needed = True
                            if needed: #if needed do not change the name then
                                continue
                            else: # other wise remove unecessary '
                                s.cells[key].contents = s.cells[key].contents.replace("'"+i+"'!",i+"!")



        

    #helper fuction to determine if a value is a float
    def is_float(self, element):
        element = str(element)
        try:
            float(element)
            return True
        except ValueError:
            return False

    def get_row_and_col(self,location):
        # Helper function to get absolute row/col of inputted location 
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
