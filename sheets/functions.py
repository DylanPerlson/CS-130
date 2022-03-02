from sheets.cell_error import CellError, CellErrorType
# from .sheet import Sheet
# from .cell import Cell


class Functions:
    def __init__(self):
        pass

    def __call__(self, function, args):
        return getattr(self, function)(args)

    #Boolean functions
    def and_func(self, args):
        if args[0] is None or args[1] is None:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        return all(args)

    def or_func(self, args):
        if args[0] is None or args[1] is None:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        return any(args)

    def not_func(self, args):
        if args[0] is None:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        return not args[0]

    #Don't know how to do this
    def xor_func(self, args):
        if args[0] is None or args[1] is None:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        for i, arg in enumerate(args):
            args[i] = int(arg)
        return # TODO

    #String match
    def exact_func(self, args):
        if not isinstance(args[0],str) or not isinstance(args[1],str):
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        return str(args[0]) == str(args[1])

    #Conditional functions
    def if_func(self, args): # previously: cond, value1, value2 = None):
        cond = args[0]
        value1 = args[1]

        try:
            value2 = args[2]
        except IndexError:
            value2 = None

        if cond is None or value1 is None:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        if cond:
            return value1
        elif not cond and value2 is not None:
            return value2
        return None

    def iferror_func(self, args): # previously: value1, value2 = None):
        value1 = args[0]

        try:
            value2 = args[1]
        except IndexError:
            value2 = None

        if value1 is None:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
        if not isinstance(value1, CellError):
            return value1
        elif isinstance(value1, CellError) and value2 is not None:
            return value2
        return None

    #Informational errors
    def isblank_func(self, args):
        if not isinstance(args[0], Cell):
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if args[0].type == "NONE":
            return True
        return False

    def iserror_func(self, args):
        if not isinstance(args[0], Cell):
            return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
        if args[0].type == "ERROR":
            return True
        return False

    def version_func(self, args):
        return None #sheet.version