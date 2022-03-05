"""Implements boolean functions."""
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

    #Boolean functions
    def and_func(self, args):
        """Implements AND function.
        True if all arguments are True."""
        return all(args)

    def or_func(self, args):
        """Implements OR function.
        True if one argument is True."""
        return any(args)

    def not_func(self, args):
        """Implements AND function.
        Returns True for False and vice versa."""
        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, f"Invalid number of arguments: {args}")
        return not args[0]

    def xor_func(self, args):
        """Implements XOR function.
        True if odd number of arguments are True."""
        # for i, arg in enumerate(args):
        #     args[i] = int(arg)

        odd_count = 0
        for i in len(args):
            if args[i] is True:
                odd_count = odd_count + 1

        if odd_count % 2 != 0:
            return True
        return False

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

        return str(args[0]) == str(args[1])

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
        choose_index = args[0]
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
        return '1.3' #sheet.version

    def indirect_func(self, args):
        """The cell value is returned."""
        if len(args) != 4:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")


        workbook_instance = args[1]
        sheet_instance = args[2]
        cell_signal = args[3]

        if cell_signal:
            return args[0]

      
        args = args[0].split('!')

        # if using the current sheet
        if len(args) == 1:
            sheet_name = sheet_instance.sheet_name
            cell = args[0]
        # if using a different sheet
        elif len(args) == 2:
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                return CellError(CellErrorType.BAD_REFERENCE, "200: Invalid cell reference")
            cell = args[1]
        else:
            return CellError(CellErrorType.BAD_REFERENCE, "201: Invalid cell reference")

        # delete the dollar sign from the cell reference
        cell = cell.replace("$","")
        try:
            value = (workbook_instance.get_cell_value(sheet_name, cell))
        except UnboundLocalError: # in case of a string
            return CellError(CellErrorType.BAD_REFERENCE, "201: Invalid cell reference")

        if value is None:
            return CellError(CellErrorType.BAD_REFERENCE, "201: Invalid cell reference")
        return value
