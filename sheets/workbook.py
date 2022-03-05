"""Defines the workbook class for the spreadsheet API."""
import copy
import json

import lark

from sheets.cell_error import CellError, CellErrorType

from .sheet import Sheet

MAX_ROW = 475254
MAX_COL = 9999
A_UPPERCASE = ord('A')
ALPHABET_SIZE = 26

do_not_delete = False

class Workbook:
    """A workbook containing zero or more named spreadsheets.

    Any and all operations on a workbook that may affect calculated cell
    values should cause the workbook's contents to be updated properly.
    decimal, error code

    when we call set cell contents, we add that cell to cell_changed_dict
    if it does not exist and set to true.
    o.w. just set it to true

    every time call get cell value, we check if it has been changed or not,
    if it has been return value (have a stored value in it)
    o.w. re-evaluate
    """

    def __init__(self):
        # Initialize a new empty workbook.
        self.sheets = []
        self.number_sheets = 0
        self.notification_functions = []
        self.user_defined_functions = []

        #master_cell_dict[child] = [list of parent cells/ cells that reference child]
        self.master_cell_dict = {}

        self.visited_cell_dict = {}
        self.allowed_characters = ".?!,:;!@#$%^&*()-_ "
        self.needs_quotes = ".?!,:;!@#$%^&*()- "

        self.circ_refs = []
        self.evaluate_again = []
        self.notifying_cells = []
        self.children_dict = {}
        self.cell_changed_dict = {}

        self.parser = lark.Lark.open('sheets/formulas.lark', start='formula')
        
        self.num_visits = 0
        self.function_directory =   {
            'AND': 'and_func',
            'OR': 'or_func',
            'NOT': 'not_func',
            'XOR': 'xor_func',
            'EXACT': 'exact_func',
            'IF': 'if_func',
            'IFERROR': 'iferror_func',
            'CHOOSE': 'choose_func',
            'ISBLANK': 'isblank_func',
            'ISERROR': 'iserror_func',
            'VERSION': 'version_func',
            'INDIRECT': 'indirect_func'
            }


    def move_cells(self, sheet_name, start_location,
            end_location, to_location, to_sheet = None):
        """Move cells from one location to another, possibly moving them to
        another sheet.  All formulas in the area being moved will also have
        all relative and mixed cell-references updated by the relative
        distance each formula is being copied.

        Cells in the source area (that are not also in the target area) will
        become empty due to the move operation.

        The start_location and end_location specify the corners of an area of
        cells in the sheet to be moved.  The to_location specifies the
        top-left corner of the target area to move the cells to.

        Both corners are included in the area being moved; for example,
        copying cells A1-A3 to B1 would be done by passing
        start_location="A1", end_location="A3", and to_location="B1".

        The start_location value does not necessarily have to be the top left
        corner of the area to move, nor does the end_location value have to be
        the bottom right corner of the area; they are simply two corners of
        the area to move.

        This function works correctly even when the destination area overlaps
        the source area.

        The sheet name matches are case-insensitive; the text must match but
        the case does not have to.

        If to_sheet is None then the cells are being moved to another
        location within the source sheet.

        If any specified sheet name is not found, a KeyError is raised.
        If any cell location is invalid, a ValueError is raised.

        If the target area would extend outside the valid area of the
        spreadsheet (i.e. beyond cell ZZZZ9999), a ValueError is raised, and
        no changes are made to the spreadsheet.

        If a formula being moved contains a relative or mixed cell-reference
        that will become invalid after updating the cell-reference, then the
        cell-reference is replaced with a #REF! error-literal in the formula.
        """

        #check for invalid cells or sheets

        cur_sheet = None
        to_sheet = None
        start_row, start_col = self._get_col_and_row(start_location)
        end_row, end_col = self._get_col_and_row(end_location)


        if not self._check_valid_cell(start_location) or not self._check_valid_cell(end_location):
            raise ValueError()
        if end_row > MAX_ROW or end_col > MAX_COL or start_row > MAX_ROW or start_col > MAX_COL:
            raise ValueError()

        to_exists = False
        cur_exists = False
        #check if the sheet exists
        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                cur_exists = True
                cur_sheet = i
                break

        if to_sheet is not None:
            for i in self.sheets:
                if i.sheet_name.lower() == to_sheet.lower():
                    to_exists = True
                    to_sheet = i
                    break

            #if no valid sheet name
            if to_exists is False or cur_exists is False:
                raise KeyError()

        # make sure they are in correct order
        if start_row > end_row:
            start_row, end_row = end_row, start_row
        if start_col > end_col:
            start_col, end_col = end_col, start_col

        copy_dict = {}
        #how much the rows and cols move
        move_row, move_col = self._get_col_and_row(to_location)
        delta_row = move_row - start_row
        delta_col = move_col - start_col

        #copy all of the cells
        for r in range(start_row, end_row+1):
            for c in range(start_col, end_col+1):
                cell = str(self._base_10_to_alphabet(r))+str(c)

                copy_dict[(r,c)] = cur_sheet.get_cell_contents(cell)
                #check if we need to update the formula
                if str(copy_dict[(r,c)])[0] == '=':
                    cell_list = []
                    for e,i in enumerate(self.sheets):
                        if i.sheet_name.lower() == sheet_name.lower():
                            cell_list = self.sheets[e]._retrieve_cell_references(self,
                            copy_dict[(r,c)])

                    for i in cell_list:

                        [name, loc] = i.split('!',1)
                        old_loc = loc
                        #not in the sheet so do not need to update
                        if name.lower() != sheet_name.lower():
                            continue

                        #is in sheet so need to update
                        elif name.lower() == sheet_name.lower():
                            abs_row = False
                            abs_col = False

                            if '$' in loc:
                                abs_loc = loc.split('$')
                                if abs_loc[0] == '':
                                    abs_col = True
                                if abs_loc[-1].isdigit():
                                    abs_row = True

                                #swap bc we implimented our helper wrong
                                abs_col, abs_row = abs_row, abs_col

                                loc = ''.join(abs_loc)


                            #update rows  and cols

                            loc_row, loc_col = self._get_col_and_row(loc)




                            replace_r = loc_row
                            replace_c = loc_col

                            if loc_row in range(start_row, end_row+1) and abs_row is False:
                                replace_r = loc_row + delta_row

                            if loc_col in range(start_col, end_col+1) and abs_col is False:
                                replace_c = loc_col + delta_col


                            #swap bc we implimented our helper wrong
                            replace_r, replace_c = replace_c, replace_r

                            if abs_row is True and abs_col is False:
                                new_loc = '$'+str(self._base_10_to_alphabet(replace_c))\
                                    +str(replace_r)
                            elif abs_row is False and abs_col is True:
                                new_loc = str(self._base_10_to_alphabet(replace_c))\
                                    +'$'+str(replace_r)
                            elif abs_row is True and abs_col is True:
                                new_loc = '$'+str(self._base_10_to_alphabet(replace_c))\
                                    +'$'+str(replace_r)
                            else:
                                new_loc = str(self._base_10_to_alphabet(replace_c))+str(replace_r)
                            #TODO (Dylan) there is a possible very nuanced error of overlapping replacements

                            copy_dict[(r,c)] = copy_dict[(r,c)].replace(old_loc,new_loc)



                        else:
                            
                            raise ValueError()




                #delete the value after copying values - only if the move function was called
                if do_not_delete is False:
                    cur_sheet.set_cell_contents(self,cell, '')

        #move to the new location - do this in two steps so dont overwrite before copying some
        for r in range(start_row, end_row+1):
            for c in range(start_col, end_col+1):
                cell = str(self._base_10_to_alphabet(r+delta_row))+str(c+delta_col)

                if to_sheet is None:
                    cur_sheet.set_cell_contents(self,cell,copy_dict[(r,c)])
                else:
                    to_sheet.set_cell_contents(self,cell,copy_dict[(r,c)])


        #!!!THIS MUST BE AT THE VERY END BECAUSE IT CHANGES THE to_sheet VALUE!!!
        #for every new cell, we need to set it to changed

        #once again r and c are backwards
        for r in range(start_row+delta_row, end_row+delta_row+1):
            for c in range(start_col+delta_col, end_col+delta_col+1):
                if to_sheet is None:
                    to_sheet = sheet_name
                location = self._base_10_to_alphabet(r) + str(c)
                sheet_location = to_sheet + '!' + location
                self.cell_changed_dict[sheet_location.lower()] = True



    def copy_cells(self, sheet_name, start_location,
            end_location, to_location, to_sheet = None):
        """Copy cells from one location to another, possibly copying them to
        another sheet.  All formulas in the area being copied will also have
        all relative and mixed cell-references updated by the relative
        distance each formula is being copied.

        Cells in the source area (that are not also in the target area) are
        left unchanged by the copy operation.

        The start_location and end_location specify the corners of an area of
        cells in the sheet to be copied.  The to_location specifies the
        top-left corner of the target area to copy the cells to.

        Both corners are included in the area being copied; for example,
        copying cells A1-A3 to B1 would be done by passing
        start_location="A1", end_location="A3", and to_location="B1".

        The start_location value does not necessarily have to be the top left
        corner of the area to copy, nor does the end_location value have to be
        the bottom right corner of the area; they are simply two corners of
        the area to copy.

        This function works correctly even when the destination area overlaps
        the source area.

        The sheet name matches are case-insensitive; the text must match but
        the case does not have to.

        If to_sheet is None then the cells are being copied to another
        location within the source sheet.

        If any specified sheet name is not found, a KeyError is raised.
        If any cell location is invalid, a ValueError is raised.

        If the target area would extend outside the valid area of the
        spreadsheet (i.e. beyond cell ZZZZ9999), a ValueError is raised, and
        no changes are made to the spreadsheet.

        If a formula being copied contains a relative or mixed cell-reference
        that will become invalid after updating the cell-reference, then the
        cell-reference is replaced with a #REF! error-literal in the formula.

        this is the same as the move function, except it does not delete the functions
        """

        global do_not_delete
        do_not_delete = True
        self.move_cells(sheet_name, start_location,
            end_location, to_location, to_sheet)
        do_not_delete = False


    def num_sheets(self):
        """Return the number of spreadsheets in the workbook."""
        return self.number_sheets

    def move_sheet(self, sheet_to_move, move_index):
        """Move the specified sheet to the specified index in the workbook's
        ordered sequence of sheets.  The index can range from 0 to
        workbook.num_sheets() - 1.  The index is interpreted as if the
        specified sheet were removed from the list of sheets, and then
        re-inserted at the specified index.

        The sheet name match is case-insensitive; the text must match but the
        case does not have to.

        If the specified sheet name is not found, a KeyError is raised.

        If the index is outside the valid range, an IndexError is raised.
        """

        if (move_index < 0 or move_index >= len(self.sheets)):
            raise IndexError()
        for e,i in enumerate(self.sheets):
            if i.sheet_name.lower() == sheet_to_move.lower():
                self.sheets.insert(move_index, i)
                self.sheets.pop(e+1)
                return
        raise KeyError()

    def reorder_sheets(self, sheet_to_move, move_index):
        """In the error messages, this function is referenced,
        so to make sure that the API supports everything,
        another function is added with the same functionality."""
        self.move_sheet(sheet_to_move, move_index)
        return

    def copy_sheet(self, sheet_to_copy):
        """Make a copy of the specified sheet, storing the copy at the end of the
        workbook's sequence of sheets.  The copy's name is generated by
        appending "_1", "_2", ... to the original sheet's name (preserving the
        original sheet name's case), incrementing the number until a unique
        name is found.  As usual, "uniqueness" is determined in a
        case-insensitive manner.

        The sheet name match is case-insensitive; the text must match but the
        case does not have to.

        The copy should be added to the end of the sequence of sheets in the
        workbook.  Like new_sheet(), this function returns a tuple with two
        elements:  (0-based index of copy in workbook, copy sheet name).  This
        allows the function to report the new sheet's name and index in the
        sequence of sheets.

        If the specified sheet name is not found, a KeyError is raised.
        """

        copy_index = -1
        for i, sheet in enumerate(self.sheets):
            if sheet.sheet_name.lower() == sheet_to_copy.lower():
                copy_index = i
                break

        copy_counter = 1
        if copy_index != -1:
            while True:
                new_sheet_name = sheet_to_copy + "_" + str(copy_counter)
                if new_sheet_name not in self.sheets:
                    (_,_) = self.new_sheet(new_sheet_name)
                    old_sheet = self.sheets[copy_index]
                    self.sheets[-1].cells = copy.deepcopy(old_sheet.cells)

                    self.number_sheets = self.number_sheets + 1
                    return
                else:
                    copy_counter = copy_counter + 1
        raise KeyError()


    def list_sheets(self): # list
        """Return a list of the spreadsheet names in the workbook, with the
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
        """Add a new sheet to the workbook.  If the sheet name is specified, it
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

        if sheet_name == "":
            raise ValueError()

        #if no name given
        if sheet_name is None:
            name_given = True
            auto_name = "Sheet"
            sheet_name = auto_name + str(self._create_name())
            new_sheet = Sheet(sheet_name)


        # no leading or trailing white space allowed
        if sheet_name[0] == " " or sheet_name[-1] == " ":
            raise ValueError(f'Invalid sheetname: {sheet_name}')

        for i in sheet_name:
            if not i.isalnum() and not i in self.allowed_characters:
                raise ValueError(f'Invalid sheetname: {sheet_name}')


        #cannot already be taken
        if name_given is False:
            for i in self.sheets:
                if i.sheet_name.lower() == sheet_name.lower():
                    raise ValueError(f'Invalid sheetname: {sheet_name}')

            new_sheet = Sheet(sheet_name)

        self.number_sheets += 1
        self.sheets.append(new_sheet)

        return (self.number_sheets-1, sheet_name) # '-1' is because index should start at 0

    def del_sheet(self, sheet_name: str):
        """Delete the spreadsheet with the specified name.

        The sheet name match is case-insensitive; the text must match but the
        case does not have to.

        If the specified sheet name is not found, a KeyError is raised.
        """

        all_sheet_names = []
        for _, sheet in enumerate(self.sheets):
            all_sheet_names.append(sheet.sheet_name.lower())

        if sheet_name.lower() not in all_sheet_names:
            raise KeyError()
        # try:
        for _, sheet in enumerate(self.sheets):
            #remove the sheet with sheet_name
            curr_sheet = sheet
            if curr_sheet.sheet_name.lower() == sheet_name.lower():
                self.sheets.remove(curr_sheet)
                self.number_sheets -= 1
                # Need to update cells here to have bad references since
                # sheet doesn't exist anymore right?
                return
        # except KeyError as e:
        #     raise

    def get_sheet_extent(self, sheet_name: str):
        """Return a tuple (num-cols, num-rows) indicating the current extent of
        the specified spreadsheet.

        The sheet name match is case-insensitive; the text must match but the
        case does not have to.

        If the specified sheet name is not found, a KeyError is raised.
        """
        # new code for getting the extent
        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                extent = [0,0]
                for key in i.cells:
                    if i.cells[key].contents is not None and key[0] > extent[0]:
                        extent[0] = key[0]
                    if i.cells[key].contents is not None and key[1] > extent[1]:
                        extent[1] = key[1]
                return (extent[0],extent[1])


        #if sheet name not found, raise key Error()
        raise KeyError()

    def _get_col_and_row(self,location):
        """Helper function to get absolute row/col of inputted location (AD42)."""
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

        return row, col #these should actually be swapped I think?

    def set_cell_contents(self, sheet_name: str, location: str,
                          contents: None):
        """Set the contents of the specified cell on the specified sheet.

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

        #create the changed dict or update it to True bc we are resetting the contents
        sheet_location = sheet_name+'!'+location
        self.cell_changed_dict[sheet_location.lower()] = True

        # check that the cell is either a string or None
        if not isinstance(contents, str) and contents is not None:
            raise TypeError('Content is not a string.')

        for i in self.sheets:
            #edit cell content of specified sheet
            if i.sheet_name is None:
                continue
            if not self._check_valid_cell(location):
                raise ValueError('Cell location invalid.')

            #set cell contents and notify parent cells
            if i.sheet_name.lower() == sheet_name.lower():
                #if want to set cell contents to empty
                if contents is None or (not self._is_float(contents) and contents.strip() == ''):
                    i.set_cell_contents(self, location.lower(), None)
                elif self._is_float(contents):
                    i.set_cell_contents(self, location.lower(), contents)
                else: #store normally
                    i.set_cell_contents(self, location.lower(), contents.strip())
                #completed task

                curr_cell = sheet_name.lower() + '!' + location.lower()

                #reset list of circ refs
                self.circ_refs = []

                self._tarjan()
                # #these are the cells that will be passed onto the notification functions
                # #needs to be reset each call
                self.notifying_cells = []
                # #and add the current cell
                self.notifying_cells.append((sheet_name, curr_cell.split('!')[1]))
                #get the list of changed cells
                self._notify_helper(sheet_name, curr_cell)
                #now we notify all of the functions of the cells that were changed
                for func in self.notification_functions:
                    #split_cell_string = curr_cell.split('!')
                    func(self, self.notifying_cells)

                
                #TODO (Dylan) DTP dont just update this cell, also update any dependencies
                
                self._update(curr_cell)
                
                #return is needed so we do not raise a key error
                return

        #no sheet found
        raise KeyError()


    def _update(self,curr_cell):
        #Iterate up through dependent cells of our current cell
        if curr_cell in self.children_dict and curr_cell not in self.circ_refs:
            dependents_list = self.children_dict[curr_cell]
            for dependent in dependents_list:
                dep_split = dependent.split('!')
                #evaluate the cell
                if self.cell_changed_dict[dependent] == True:
                    self.get_cell_value(dep_split[0],dep_split[1])
                    #recurse
                    self._update(dependent)


    def get_cell_contents(self, sheet_name: str, location: str):
        """Return the contents of the specified cell on the specified sheet.

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
        if not self._check_valid_cell(location):
            raise ValueError()

        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                self._check_valid_cell(location)
                return i.get_cell_contents(location)

        raise KeyError()



    def get_cell_value(self, sheet_name: str, location: str):
        """Return the evaluated value of the specified cell on the specified
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
        if not self._check_valid_cell(location):
            raise ValueError()


        for i in self.sheets:
            if i.sheet_name.lower() == sheet_name.lower():
                workbook_instance = self
                return i.get_cell_value(workbook_instance,location)

        #else raise a key error
        raise KeyError()

    def _check_valid_cell(self, location):
        """Check if the cell location is valid """
        if not isinstance(location, str):
            return False

        if not location.isalnum():
            return False

        #this is reverse but is still be good
        row, col = self._get_col_and_row(location)
        if row > MAX_ROW or col > MAX_COL:
            raise ValueError()

        digits = False
        for c in location:
            if not c.isdigit() and digits is False:
                continue
            elif c.isdigit() and digits is False:
                digits = True
            elif c.isdigit() and digits is True:
                continue
            elif c == ' ':
                return False
            else:
                return False
                # raise ValueError()

        for c in range(len(location)-1):
            if not location[c+1].isdigit() and location[c].isdigit():
                return False

        return True

    def _create_name(self,num = 1):
        """ finds an unused name """

        auto_name = "Sheet"

        for i in self.sheets:
            if i.sheet_name == auto_name + str(num):
                return self._create_name(num + 1)

        return num

    @staticmethod
    def load_workbook(fp): # : TextIO) -> Workbook:
        """This is a static method (not an instance method) to load a workbook
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

        try:
            data = json.load(fp)
        except json.decoder.JSONDecodeError:
            return Workbook()

        wb = Workbook()

        if 'sheets' not in data:
            raise KeyError("No 'sheets' key found in json file.")

        if not isinstance(data['sheets'], list):
            raise TypeError('Value for sheets is not a list')

        for sheet in data['sheets']:
            # check for empty stuff:
                # check cell validity
                # missing required fields
                # malperformed/unparseable json

            if 'name' not in sheet:
                raise KeyError("No 'name' key found in some sheet of the json file.")
            if 'cell-contents' not in sheet:
                raise KeyError("No 'cell-contents' key found in some sheet of the json file.")

            sheet_name = sheet['name']
            (_,_) = wb.new_sheet(sheet_name)

            # if not isinstance(data['cell-contents'], dict):
            #     raise TypeError('Value for cell-contents not a dictionary.')

            for location, content in sheet['cell-contents'].items():
                if not isinstance(content, str) and not content is None:
                    raise TypeError(f'Cell content ({content}) is invalid type ({type(content)})')

                wb.set_cell_contents(sheet_name, location, content)

        return wb

    def save_workbook(self, fp):
        """Instance method (not a static/class method) to save a workbook to a
        text file or file-like object in JSON format.  Note that the _caller_
        of this function is expected to have opened the file; this function
        merely writes the file.

        If an IO write error occurs (unlikely but possible), let any raised
        exception propagate through.
        """

        file = {"sheets":[]}

        for i in self.sheets:
            cells = {}
            for key, value in i.cells.items():
                cells[(self._base_10_to_alphabet(key[0])+str(key[1]))] = value.contents

            sheet = {"name": i.sheet_name, "cell-contents": cells}

            file["sheets"].append(sheet)

        json_string = json.dumps(file)
        fp.write(json_string)

    def rename_sheet(self, sheet_name, new_sheet_name):
        """Rename the specified sheet to the new sheet name.  Additionally, all
        cell formulas that referenced the original sheet name are updated to
        reference the new sheet name (using the same case as the new sheet
        name, and single-quotes iff [if and only if] necessary).

        The sheet_name match is case-insensitive; the text must match but the
        case does not have to.

        As with new_sheet(), the case of the new_sheet_name is preserved by
        the workbook.

        If the sheet_name is not found, a KeyError is raised.

        If the new_sheet_name is an empty string or is otherwise invalid, a
        ValueError is raised. As usual, the new sheet name must be both
        valid and unique in the workbook; if it is not, an exception is raised.
        Also as usual, the case of the new name is preserved by the workbook.
        """

        old_name = sheet_name
        new_name = new_sheet_name
        old_name_exists = False
        proper_old_name = None

        #check if the workbook name is a valid name
        if new_name == "":
            raise ValueError()
        for i in new_name:
            if not i.isalnum() and not i in self.allowed_characters:
                raise ValueError()
        # no leading or trailing white space allowed
        if new_name[0] == " " or new_name[-1] == " ":
            raise ValueError()


        # change the name of the sheet
        for i in self.sheets:
            #old name is case insensitive
            if i.sheet_name.lower() == old_name.lower():
                proper_old_name = i.sheet_name
                i.sheet_name = new_name
                old_name_exists = True
                break

        # old name not found
        if old_name_exists is False:
            raise KeyError()

        # change the formulas for every cell
        # Need to call on cells updated here as well
        updated_cells = []
        for s in self.sheets:
            for key in s.cells:
                #check if the cell is a formula
                if s.cells[key].type == "FORMULA":
                    #check if the formula contains the old_name
                    if proper_old_name+'!' in s.cells[key].contents:
                        s.cells[key].contents = s.cells[key].contents.replace(\
                            proper_old_name+'!',new_name+'!')
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
                                s.cells[key].contents = s.cells[key].contents.replace(\
                                    "'"+proper_old_name+"'!","'"+new_name+"'!")
                                break
                        if self._is_float(new_name[0]):
                            needed = True
                            s.cells[key].contents = s.cells[key].contents.replace(\
                                "'"+proper_old_name+"'!","'"+new_name+"'!")
                        if not needed: # not necessary
                            s.cells[key].contents = s.cells[key].contents.replace(\
                                "'"+proper_old_name+"'!",new_name+'!')


                        #remove other uneccesary '
                        contents_arr = s.cells[key].contents.split("'")
                        remove_apostrophe = []
                        for i, content in enumerate(contents_arr):
                            #make sure name doesnt start with a !
                            #find where there is a name broken by '
                            if (content[0] == '!' and contents_arr[i-1][0] != '!'):
                                remove_apostrophe.append(contents_arr[i-1])
                        for i in remove_apostrophe:
                            #check if the other equations need quotes
                            needed = False
                            for char in self.needs_quotes:
                                if char in i:
                                    needed = True
                                    break
                            #also needs quotes if starts with a number
                            if self._is_float(i[0]):
                                needed = True

                            #if needed do not change the name then
                            if needed:
                                continue
                            else: # other wise remove unecessary '
                                s.cells[key].contents = s.cells[key].contents.replace(\
                                    "'"+i+"'!",i+"!")
                updated_cells.append((new_name, s.cells[key]))

        #need to update sheetname in cell dependencies

        #TODO (Dylan) DTP
        #create a list of keys to change bc cannot change during
        change_keys = []
        for key, value in self.master_cell_dict.items():
            #check if one of the master cells has it as a value
            #everything should already be lower so not an issue
            old_name = old_name.lower()

            #the value is a list so need to iterate through the list
            for _,i in enumerate(value):
                i = i.replace(old_name,new_name.lower())
            #if old name is in the key now replace
            if old_name in key:
                change_keys.append(key)


        #change all the necesarry key values
        for key in change_keys:
            new_cell = key.replace(old_name,new_name)
            #create the new entry
            self.master_cell_dict[new_cell] = self.master_cell_dict[key]
            #delete the old entry
            self.master_cell_dict.pop(key)

        #now do the same for:
        #self.children_dict
        #self.cell_changed_dict

        change_keys = []
        for key, value in self.children_dict.items():
            #check if one of the master cells has it as a value
            #everything should already be lower so not an issue
            old_name = old_name.lower()

            #the value is a list so need to iterate through the list
            for _,i in enumerate(value):
                i = i.replace(old_name,new_name.lower())
            #if old name is in the key now replace
            if old_name in key:
                change_keys.append(key)


        #change all the necesarry key values
        for key in change_keys:
            new_cell = key.replace(old_name,new_name)
            #create the new entry
            self.children_dict[new_cell] = self.children_dict[key]
            #delete the old entry
            self.children_dict.pop(key)

        change_keys = []
        for key in self.cell_changed_dict:
            #check if one of the master cells has it as a value
            #everything should already be lower so not an issue
            old_name = old_name.lower()

            #if old name is in the key now replace
            if old_name in key:
                change_keys.append(key)


        #change all the necesarry key values
        for key in change_keys:
            new_cell = key.replace(old_name,new_name)
            #create the new entry
            self.cell_changed_dict[new_cell] = self.cell_changed_dict[key]
            #delete the old entry
            self.cell_changed_dict.pop(key)




    #helper fuction to determine if a value is a float
    def _is_float(self, element):
        """helper fuction to determine if a value is a float"""
        element = str(element)
        try:
            float(element)
            return True
        except ValueError:
            return False

    def _get_col_and_row(self,location):
        """Helper function to get absolute row/col of inputted location"""

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

    def notify_cells_changed(self, new_func):
        """This function adds notifications to a class variable"""
        self.notification_functions.append(new_func)

    def _notify_helper(self, sheet_name, curr_cell, call_origin = None):
        """add all of our cells to the evaluate again list if it
        is not in it already

        This function finds circ references as well as notifying
        all of the functions when a cell changes
        """
        #Iterate up through dependent cells of our current cell
        if curr_cell in self.children_dict and curr_cell not in self.circ_refs:
            dependents_list = self.children_dict[curr_cell]
            for dependent in dependents_list:
                split_cell_string = dependent.split('!')

                #tell all of the cells that they have changed
                self.cell_changed_dict[dependent] = True

                #add the cell to list of cells to be notified of
                if (split_cell_string[0],split_cell_string[1]) not in self.notifying_cells:
                    self.notifying_cells.append((split_cell_string[0],split_cell_string[1]))
                    #recurse
                    self._notify_helper(split_cell_string[0], dependent)



    def _base_10_to_alphabet(self, number):
        """Helper function: base 10 to alphabet
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

    def _tarjan_helper(self, u, low, found, in_stack, the_stack):

        found[u] = self.num_visits
        low[u] = self.num_visits
        self.num_visits += 1
        in_stack[u] = True
        the_stack.append(u)

        key_list = list(self.master_cell_dict.keys())
        value_list = list(self.master_cell_dict.values())

        #find the indices of the cells in value_list
        cells = value_list[u]
        idx = []
        for c in cells:
            #append where it is in the key list
            if c in key_list:
                idx.append(key_list.index(c))


        for v in idx:

            # If v is not found yet, then recurse for it
            if found[v] == -1 :

                self._tarjan_helper(v, low, found, in_stack, the_stack)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u

                low[u] = min(low[u], low[v])

            elif in_stack[v] is True:
                low[u] = min(low[u], found[v])

        # head node found
        # If length greater than 2, set contents of stack to CIRC_REF errors
        w = -1
        if low[u] == found[u]:
            connected = []
            while w != u:
                w = the_stack.pop()
                connected.append(value_list[w])
                in_stack[w] = False

            #then we have a strongly connected list
            if len(connected) > 1:
                for i in connected:
                    split_name = i[0].split('!')
                    for s in self.sheets:
                        if s.sheet_name.lower() == split_name[0]:
                            row,col = self._get_col_and_row(split_name[1])
                            s.cells[(row,col)].evaluated_value = CellError(
                                CellErrorType.CIRCULAR_REFERENCE,"Circular Reference", None)
                            self.circ_refs.append(i[0])
                            #make sure that it does not revaluate it
                            self.cell_changed_dict[i[0]] = False
                            #this break is just for efficiency so we dont need to keep checking
                            break


    def _tarjan(self):
        self.num_visits = 0

        #set everything to -1
        found = [-1] * len(self.master_cell_dict.keys())
        low = [-1] * len(self.master_cell_dict.keys())
        in_stack = [False] * len(self.master_cell_dict.keys())
        the_stack =[]


        # Call the helper function
        for i in range(len(self.master_cell_dict.keys())):
            if found[i] == -1:
                self._tarjan_helper(i, low, found, in_stack, the_stack)
