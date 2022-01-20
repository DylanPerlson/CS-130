# object class for evaluating expressions

from ast import arg
import lark
from lark import Transformer, Visitor
from .cell_error import CellError, CellErrorType

class RetrieveReferences(Visitor):
    def __init__(self):
        self.references = []

    def cell(self, args):
        args = args.children

        # getting the appropriate sheet name and cell location
        if len(args) == 1:      # if using the current sheet
            sheet_name = 'current' # TODO fix
            cell = args[0].value
        elif len(args) == 2:    # if using a different sheet
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                cell = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
                print('error1') # TODO BAD_REFERENCE
            cell = args[1].value
        else:
            cell = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
            print('error2') # TODO BAD_REFERENCE

        try:
            cell = 1 # TODO get_cell_value(sheet_name, cell) here
        except:
            cell = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
            # TODO BAD_REFERENCE 
            exit()

        # self.references.append([sheet_name, cell])
        self.references.append(str(sheet_name) + '!' + str(cell))


# used to evaluate an expression from the parsed formula
class EvalExpressions(Transformer):
    def __init__(self, workbook_instance, sheet_instance):
        self.workbook_instance = workbook_instance
        self.sheet_instance = sheet_instance

    def number(self, args):
        return args[0]

    def string(self, args):
        return args[0][1:-1] # the '[1:-1]' is to remove the double quotes

    def unary_op(self, args):
        return str(args[0]+args[1])

    def parens(self, args):
        return args[0]

    def add_expr(self, args):
        if (args[0] == None):
            args[0] = 0
        if (args[2] == None):
            args[2] = 0
        t = str(args[0])+args[1]+str(args[2])
        return eval(t)

    def mul_expr(self, args):
        if args[1] == '/' and str(args[2]) == '0':
            return CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by 0", 'division by zero')
        t = str(args[0])+args[1]+str(args[2])
        return eval(t)

    def concat_expr(self, args):
        if(args[0] == None):
            args[0] = ''
        if(args[1] == None):
            args[1] = ''    
        return str(args[0]+args[1])

    def cell(self, args):
        # getting the appropriate sheet name and cell location
        if len(args) == 1:      # if using the current sheet
            sheet_name = self.sheet_instance.sheet_name # TODO fix
            cell = args[0]
        elif len(args) == 2:    # if using a different sheet
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                # TODO fix here
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                cell_value = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
                pass # TODO BAD_REFERENCE
            cell = args[1]
        else:
            cell_value = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
            pass # TODO BAD_REFERENCE

        try:
            cell_value = self.workbook_instance.get_cell_value(sheet_name, cell)
        except:
            cell_value = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
            # TODO BAD_REFERENCE 
            exit()

        #if cell_value == None:
        #    cell_value = 0 # TODO "" for string

        return cell_value
