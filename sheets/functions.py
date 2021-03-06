"""Implements boolean functions."""
import decimal
from sheets.cell_error import CellError, CellErrorType

def _is_integer(d):
    """Checks whether input d is an integer.
    True if so, False otherwise."""
    return d == d.to_integral_value()


class Functions:
    """Contains all functions that can be used."""

    def __init__(self):
        """Initializes the class."""

    def __call__(self, function, args):
        """This is necessary for elegant function calls."""
        return getattr(self, function)(args)

    # def _flat(self, args):
    #     flat_list = []
    #     for sublist in args:
    #         if isinstance(sublist, list):
    #             for item in sublist:
    #                 flat_list.append(self._flat(item))
    #         else:
    #             flat_list.append(sublist)
    #     return flat_list

    def _flat(self, list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self._flat(list_of_lists[0]) + self._flat(list_of_lists[1:])
        return list_of_lists[:1] + self._flat(list_of_lists[1:])

    def _args(self,args):
        old_args = args
        args = []
        for i in old_args:
            if i is None:
                args.append(i)
            if isinstance(i,list):
                if len(i) > 1 and isinstance(i[1],bool):
                    args.append(i)
                    continue
                #get rid of not for this case
                if len(i) > 1 and isinstance(i[0],decimal.Decimal) and\
                not isinstance(i[-1],decimal.Decimal):
                    args.append(i[0])
                    continue
                else:
                    args.append(i)
            else:
                args.append(i)
        return args

    def _get_value_as_string(self, curr_arg):
        if isinstance(curr_arg, CellError) or isinstance(curr_arg, str):
            return curr_arg
        elif curr_arg is None:
            return ''
        elif isinstance(curr_arg, decimal.Decimal):
            return str(curr_arg)
        elif isinstance(curr_arg, bool):
            return str(curr_arg).upper()

    def _get_value_as_bool(self, curr_arg):
        if isinstance(curr_arg, CellError) or isinstance(curr_arg, bool):
            return curr_arg
        elif curr_arg is None:
            return False
        elif isinstance(curr_arg, str):
            if curr_arg.lower() == 'true':
                return True
            elif curr_arg.lower() == 'false':
                return False
        elif isinstance(curr_arg, decimal.Decimal):
            if curr_arg == 0:
                return False
            else:
                return True

        return CellError(CellErrorType.TYPE_ERROR, "Argument is not a boolean")

    def _get_value_as_number(self, curr_arg):
        if isinstance(curr_arg, CellError) or isinstance(curr_arg, decimal.Decimal):
            return curr_arg
        elif curr_arg is None:
            return decimal.Decimal('0')
        elif isinstance(curr_arg, str):
            if self._is_float(curr_arg):
                return decimal.Decimal(curr_arg)
            else:
                return CellError(CellErrorType.TYPE_ERROR, "String cannot be parsed into a number")
        elif isinstance(curr_arg, bool):
            return int(curr_arg)

        return CellError(CellErrorType.TYPE_ERROR, f"Invalid operation with argument: {curr_arg}")

    def _is_float(self, element):
        """ helper fuction to determine if a value is a float """
        element = str(element)
        try:
            float(element)
            return True
        except ValueError:
            return False

    #new range functions
    def sum_func(self,args):
        """This function calculates the sum of its inputs."""

        args = self._args(args)
        args = self._flat(args)

        if len(args) == 0:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {args}")

        # filter out None values and convert to number
        args = [x for x in args if x is not None]
        args = [self._get_value_as_number(x) for x in args]

        # check for errors in args and return the error
        for arg in args:
            if isinstance(arg, CellError):
                return arg

        # if there are no arguments; return 0
        if args == []:
            return 0

        # [self._get_value_as_number(x) for x in args]

        try:
            decimal.Decimal
            return decimal.Decimal(sum(args))
        except TypeError:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to number")


    def avg_func(self,args):
        """This function calculates the average of its inputs."""

        args = self._args(args)
        args = self._flat(args)

        if len(args) == 0:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {args}")

        # filter out None values and convert to number
        args = [x for x in args if x is not None]
        args = [self._get_value_as_number(x) for x in args]

        # check for errors in args and return the error
        for arg in args:
            if isinstance(arg, CellError):
                return arg

        # if there are no arguments; return 0
        if args == []:
            return CellError(CellErrorType.DIVIDE_BY_ZERO, f"Invalid number of arguments: {args}")

        try:
            return decimal.Decimal(str(sum(args)))/decimal.Decimal(str(len(args)))
        except TypeError:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to number")


    def min_func(self,args):
        """This function calculates the minimum of its inputs."""

        #call _args again for case of it not being a cell range
        args = self._args(args)
        args = self._flat(args)

        if len(args) == 0:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {args}")

        # filter out None values and convert to number
        args = [x for x in args if x is not None]
        args = [self._get_value_as_number(x) for x in args]

        # check for errors in args and return the error
        for arg in args:
            if isinstance(arg, CellError):
                return arg

        # if there are no arguments; return 0
        if args == []:
            return 0

        try:
            return min(args) # the list converts to decimal
        except TypeError:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to number")


    def max_func(self,args):
        """This function calculates the sum of its inputs."""

        #call _args again for case of it not being a cell range
        args = self._args(args)
        args = self._flat(args)

        if len(args) == 0:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {args}")

        # filter out None values and convert to number
        args = [x for x in args if x is not None]
        args = [self._get_value_as_number(x) for x in args]

        # check for errors in args and return the error
        for arg in args:
            if isinstance(arg, CellError):
                return arg

        # if there are no arguments; return 0
        if args == []:
            return 0

        try:
            return max(args) # the list converts to decimal
        except decimal.InvalidOperation:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to number")


  #Boolean functions

    def and_func(self, args):
        """Implements AND function.
        True if all arguments are True."""

        args = self._flat(args)
        args = [self._get_value_as_bool(x) for x in args]

        for arg in args:
            if isinstance(arg, CellError):
                return arg

        try:
            return all(args)
        except TypeError:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to boolean")


    def or_func(self, args):
        """Implements OR function.
        True if one argument is True."""
        args = self._flat(args)
        args = [self._get_value_as_bool(x) for x in args]

        for arg in args:
            if isinstance(arg, CellError):
                return arg

        try:
            return any(args)
        except TypeError:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to boolean")


    def not_func(self, args):
        """Implements NOT function.
        Returns True for False and vice versa."""
        args = self._flat(args)

        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {args}")

        args = self._get_value_as_bool(args[0])
        if isinstance(args, CellError):
            return args

        return not self._get_value_as_bool(args)


    def xor_func(self, args):
        """Implements XOR function.
        True if odd number of arguments are True."""
        args = self._flat(args)

        odd_count = 0

        converted_args = []
        for i, arg in enumerate(args):
            new_arg = self._get_value_as_bool(arg)
            if isinstance(new_arg, CellError):
                return new_arg
            converted_args.append(new_arg)

        try:
            for i, _ in enumerate(converted_args):
                if converted_args[i] is True:
                    odd_count = odd_count + 1

            if odd_count % 2 != 0:
                return True
            return False
        except TypeError:
            return CellError(CellErrorType.TYPE_ERROR, "Input cannot be converted to boolean")

    #String match
    def exact_func(self, args):
        """Implements EXACT function.
        True if two arguments are equal."""
        if len(args) != 2:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        # if not isinstance(args[0],str) or not isinstance(args[1],str):
        #     return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")

        args0 = args[0]
        args1 = args[1]

        # Determine return error based on priority in cell_error.py
        if isinstance(args0, CellError) and isinstance(args1, CellError):
            if args0.get_type().value < args1.get_type().value:
                return args0
            else:
                return args1

        if isinstance(args0, CellError):
            return args0
        if isinstance(args1, CellError):
            return args1

        return self._get_value_as_string(args[0]) == self._get_value_as_string(args[1])

    #Conditional functions
    def if_func(self, args): # previously: cond, value1, value2 = None):
        """Implements IF function.
        Returns one of the inputs."""
        if len(args) < 2 or len(args) > 3:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        cond = args[0]
        value1 = args[1]

        try:
            value2 = args[2]
        except IndexError:
            value2 = False

        if cond is not True and cond is not False:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if cond:
            return value1
        # elif not cond and value2 is not None:
        #     return value2
        return value2

    def iferror_func(self, args): # previously: value1, value2 = None):
        """Implements IFERROR function.
        Returns some argument depending on whether first argument is an error."""
        if len(args) < 1 or len(args) > 2:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        value1 = args[0]

        try:
            value2 = args[1]
        except IndexError:
            value2 = ''

        # if value1 is None:
        #     return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if not isinstance(value1, CellError):
            return value1
        # elif isinstance(value1, CellError) and value2 is not None:
        #     return value2
        return value2

    def choose_func(self, args):
        """Implements CHOOSE function.
        Select one of the arguments using first argument."""
        if len(args) <= 2:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {len(args)}")
        try:
            choose_index = decimal.Decimal(args[0])
        except decimal.InvalidOperation:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid index argument: {args[0]}")

        choices = args[1:]
        if choose_index < 1 or choose_index > len(choices) or not _is_integer(choose_index):
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid index argument: {choose_index}")
        return choices[int(choose_index) - 1]

    #Informational errors
    def isblank_func(self, args):
        """Implements ISBLANK function.
        True if argument is empty."""
        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        if args[0] is None:
            return True
        return False

    def iserror_func(self, args):
        """Implements ISERROR function.
        True if argument is error."""
        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if isinstance(args[0], CellError):
            return True
        return False

    def version_func(self, args):
        """Implements VERSION function.
        Returns version number."""
        if len(args) != 0:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        return '1.4' #sheet.version

    def indirect_func(self, args):
        """The cell value is returned."""
        if len(args) != 5:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")

        # workbook_instance = args[1]
        # sheet_instance = args[2]
        cell_signal = args[3]
        eval_expressions = args[4]

        # if a cell is passed, then it will already have been evaluated
        #   in that case: just return the input argument
        if cell_signal:
            return args[0]

        # in case of a range
        #   the requested cell is probably given as string
        #   in that case: evaluate using helper function
        elif ':' in args[0]:
            return self._indirect_range(args)

        # else, the requested cell is probably given as string
        #   in that case: evaluate
        else:
            args = args[0].split('!')

            try:
                value = eval_expressions.cell(args)
            except UnboundLocalError: # in case of a string
                return CellError(CellErrorType.BAD_REFERENCE, "201: Invalid cell reference")

            if isinstance(value, list):
                value = value[0]

            if value is None:
                return CellError(CellErrorType.BAD_REFERENCE, "201: Invalid cell reference")
            return value


    def hlookup_func(self, args):
        """HLOOKUP(key, range, index) searches horizontally through a range of cells.
        The function searches through the first (i.e. topmost) row in range, looking
        for the first column that contains key in the search row (exact match, both
        type and value). If such a column is found, the cell in the index-th row of the
        found column. The index is 1-based; an index of 1 refers to the search row.
        If no column is found, the function returns a TYPE_ERROR."""

        if len(args) != 3:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")

        key = args[0]
        matrix = args[1]
        index = int(args[2] - 1) # 1-indexed

        try:
            for count, value in enumerate(matrix[0]):
                if key == value and type(key) is type(value):

                    return matrix[index][count]
        except TypeError: # if it is not possible to process matrix
            return CellError(CellErrorType.TYPE_ERROR, "No matching column found")

        # if no match is found
        return CellError(CellErrorType.TYPE_ERROR, "No matching column found")

    def vlookup_func(self, args):
        """VLOOKUP(key, range, index) searches vertically through a range of cells.
        The function searches through the first (i.e. leftmost) column in range, looking
        for the first row that contains key in the search column (exact match, both type
        and value). If such a column is found, the cell in the index-th column of the
        found row. The index is 1-based; an index of 1 refers to the search column.
        If no row is found, the function returns a TYPE_ERROR."""

        if len(args) != 3:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")

        key = args[0]
        matrix = args[1]
        index = int(args[2] - 1) # 1-indexed
        # matrix = [list(x) for x in zip(*matrix)] # transpose matrix

        # transpose matrix
        try:
            matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
        except TypeError: # if it is not possible to process matrix
            return CellError(CellErrorType.TYPE_ERROR, "No matching column found (error 42)")

        for count, value in enumerate(matrix[0]):
            if key == value and type(key) is type(value):
                return matrix[index][count]

        # if no match is found
        return CellError(CellErrorType.TYPE_ERROR, "No matching column found")

    def _indirect_range(self, args):
        workbook_instance = args[1]
        sheet_instance = args[2]
        x = args[0].split('!', 1)
        sheet_name = x[0]
        args = x[1].split(':', 1)

        #check if it is in another sheet
        if sheet_instance.sheet_name.lower() != sheet_name:
            #need to change sheet instance to proper one
            for s in workbook_instance.sheets:
                if s.sheet_name.lower() == sheet_name:
                    updated_sheet_instance = s
                    break
            else:
                return CellError(CellErrorType.BAD_REFERENCE, "Bad reference: no sheet found")

        #otherwise treat normally
        else:
            updated_sheet_instance = sheet_instance

        p1 = args[0]
        p2 = args[1]
        r1,c1 = updated_sheet_instance.get_col_and_row(p1)
        r2,c2 = updated_sheet_instance.get_col_and_row(p2)

        edge1 = (min(r1,r2),min(c1,c2))
        edge2 = (max(r1,r2),max(c1,c2))

        r1 = edge1[0]
        c1 = edge1[1]
        r2 = edge2[0]
        c2 = edge2[1]
        vals = []

        # this code returns a matrix instead of a flat list
        for count, row in enumerate(range(r1, r2+1)):
            vals.append([])
            for col in range(c1, c2+1):
                try:
                    val = updated_sheet_instance.cells[row,col].evaluated_value
                except KeyError:
                    val = None
                vals[count].append(val)

        # transpose matrix
        # because of row v col inconsistency
        vals = [[row[i] for row in vals] for i in range(len(vals[0]))]

        return vals
