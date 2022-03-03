from sheets.cell_error import CellError, CellErrorType

class Functions:
    def __init__(self):
        pass

    def __call__(self, function, args):
        return getattr(self, function)(args)

    #Boolean functions
    def and_func(self, args):
        return all(args)

    def or_func(self, args):
        return any(args)

    def not_func(self, args):
        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        return not args[0]

    def xor_func(self, args):
        # for i, arg in enumerate(args):
        #     args[i] = int(arg)

        odd_count = 0
        for i in len(args):
            if args[i] == True:
                odd_count = odd_count + 1

        if odd_count % 2 != 0:
            return True
        return False

    #String match
    def exact_func(self, args):
        if len(args) != 2:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        if not isinstance(args[0],str) or not isinstance(args[1],str):
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        return str(args[0]) == str(args[1])

    #Conditional functions
    def if_func(self, args): # previously: cond, value1, value2 = None):
        if len(args) < 2 or len(args) > 3:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        cond = args[0]
        value1 = args[1]

        try:
            value2 = args[2]
        except IndexError:
            value2 = None

        if cond is None or value1 is None:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if cond:
            return value1
        elif not cond and value2 is not None:
            return value2
        return False

    def iferror_func(self, args): # previously: value1, value2 = None):
        if len(args) < 1 or len(args) > 2:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        value1 = args[0]

        try:
            value2 = args[1]
        except IndexError:
            value2 = None

        if value1 is None:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if not isinstance(value1, CellError):
            return value1
        elif isinstance(value1, CellError) and value2 is not None:
            return value2
        return False

    def choose(self, args):
        if len(args) < 2:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid number of arguments")
        choose_index = args[0]
        choices = args[1:]
        if choose_index < 1 or choose_index > len(choices) or not isinstance(choose_index, int):
            return CellError(CellErrorType.TYPE_ERROR, "Invalid index argument")
        return choices[choose_index - 1]

    #Informational errors
    def isblank_func(self, args):
        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if args[0] is None:
            return True
        return False

    def iserror_func(self, args):
        if len(args) != 1:
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if isinstance(args[0], CellError):
            return True
        return False

    def version_func(self, args):
        return None #sheet.version