
from multiprocessing.sharedctypes import Value # TODO do we need these

from sheets.cell_error import CellError, CellErrorType
from .sheet import Sheet
import json

MAX_ROW = 475254
MAX_COL = 9999
A_UPPERCASE = ord('A')
ALPHABET_SIZE = 26

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
        # TODO any other invalid strings?
        
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
                return i.get_cell_contents(location) # TODO make sure get contents is correct
            
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

    @staticmethod
    def load_workbook(fp): # : TextIO) -> Workbook:
        """
        This is a static method (not an instance method) to load a workbook
        from a text file or file-like object in JSON format, and return the
        new Workbook instance.  Note that the _caller_ of this function is
        expected to have opened the file; this function merely reads the file.
        
        If the contents of the input cannot be parsed by the Python json
        module then a json.JSONDecodeError should be raised by the method.
        (Just let the json module's exceptions propagate through.)  Similarly,
        if an IO read error occurs (unlikely but possible), let any raised
        exception propagate through.
        
        If any expected value in the input JSON is missing (e.g. a sheet
        object doesn't have the "cell-contents" key), raise a KeyError with
        a suitably descriptive message.
        
        If any expected value in the input JSON is not of the proper type
        (e.g. an object instead of a list, or a number instead of a string),
        raise a TypeError with a suitably descriptive message.
        """

        data = json.load(fp)
        # print(data)

        new_workbook = "code in progress"
        return new_workbook

    def save_workbook(self, fp): #, fp: TextIO) -> None:
        """
        Instance method (not a static/class method) to save a workbook to a
        text file or file-like object in JSON format.  Note that the _caller_
        of this function is expected to have opened the file; this function
        merely writes the file.
        
        If an IO write error occurs (unlikely but possible), let any raised
        exception propagate through.
        """

        file = {"sheets":[]}

        for i in self.sheets: # TODO they have to be in the right order !!!
            cells = {}
            for key, value in i.cells.items():
                cells[(self.base_10_to_alphabet(key[0])+str(key[1]))] = value.contents

            sheet = {"name": i.sheet_name, "cell_contents": cells}

            file["sheets"].append(sheet)

            # print(json.dumps(file, sort_keys=True, indent=4))
            # print(type(json_string))
            # print(file)

        json_string = json.dumps(file)
        fp.write(json_string)
        pass

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

    def base_10_to_alphabet(self, number):
        """ Helper function: base 10 to alphabet
        Convert a decimal number to its base alphabet representation
        from: https://codereview.stackexchange.com/a/182757
        """



        return ''.join(
                chr(A_UPPERCASE + part)
                for part in self._decompose(number)
        )[::-1]

    def _decompose(self, number):
        """Generate digits from `number` in base alphabet, least significants
        bits first.

        Since A is 1 rather than 0 in base alphabet, we are dealing with
        `number - 1` at each iteration to be able to extract the proper digits.

        from: https://codereview.stackexchange.com/a/182757
        """

        while number:
            number, remainder = divmod(number - 1, ALPHABET_SIZE)
            yield remainder