from sheets.cell_error import CellError, CellErrorType
from .sheet import Sheet

#Comparative functions
def equal_to(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 == arg2

def not_equal_to(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 != arg2

def greater_than(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 > arg2

def less_than(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 < arg2

def greater_or_equal(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 >= arg2

def less_or_equal(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 <= arg2