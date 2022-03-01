from sheets.cell_error import CellError, CellErrorType
from .sheet import Sheet
from .cell import Cell
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

#Boolean functions
def _and(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 and arg2

def _or(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 or arg2

def _not(arg1):
    if arg1 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return not arg1

#Don't know how to do this
def _xor(arg1, arg2):
    if arg1 is None or arg2 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return arg1 and arg2

#String match
def _matching_strings(arg1, arg2):
    if not isinstance(arg1,str) or not isinstance(arg2,str):
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    return str(arg1) == str(arg2)

#Conditional functions
def _if(cond, value1, value2 = None):
    if cond is None or value1 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    if cond:
        return value1 
    elif not cond and value2 is not None:
        return value2 
    return None

def _iferror(value1, value2 = None):
    if value1 is None:
        return CellError(CellErrorType.BAD_REFERENCE, "Invalid arguments")
    if not isinstance(value1, CellError):
        return value1 
    elif isinstance(value1, CellError) and value2 is not None:
        return value2
    return None

#Informational errors
def isblank(arg1):
    if not isinstance(arg1, Cell):
        return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
    if arg1.type == "NONE":
        return True
    return False

def iserror(arg1):
    if not isinstance(arg1, Cell):
        return CellError(CellErrorType.TYPE_ERROR, "Invalid arguments")
    if arg1.type == "ERROR":
        return True
    return False

def version():
    return None #sheet.version