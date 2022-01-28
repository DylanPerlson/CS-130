# object class for evaluating expressions

from ast import arg
import decimal
import lark
import decimal
from lark import Transformer, Visitor
from .cell_error import CellError, CellErrorType

error_literals = ['#REF!', '#ERROR!', '#CIRREF!', '#VALUE!', '#DIV/0!', '#NAME?']
class RetrieveReferences(Visitor):
    def __init__(self, sheet_instance):
        self.references = []
        self.sheet_instance = sheet_instance
        self.error_occurred = False

    def cell(self, args):
        args = args.children

        # getting the appropriate sheet name and cell location
        if len(args) == 1:      # if using the current sheet
            sheet_name = self.sheet_instance.sheet_name
            cell_location = args[0].value
        elif len(args) == 2:    # if using a different sheet
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                self.error_occurred = True
                sheet_name = ''
            cell_location = args[1].value
        else:
            self.error_occurred = True
            sheet_name = ''
            cell_location = ''

        self.references.append(str(sheet_name) + '!' + str(cell_location))


class EvalExpressions(Transformer):
    """ used to evaluate an expression from the parsed formula: """
    
    def __init__(self, workbook_instance, sheet_instance):
        self.workbook_instance = workbook_instance
        self.sheet_instance = sheet_instance

    def number(self, args):
        d = decimal.Decimal(args[0])
        return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()

    def string(self, args):
        return args[0][1:-1] # the '[1:-1]' is to remove the double quotes

    def unary_op(self, args):
        if args[0] == '+':
            return decimal.Decimal(args[1])
        elif args[0] == '-':
            return -decimal.Decimal(args[1])
        else:
            raise Exception

    def parens(self, args):
        return args[0]

    def add_expr(self, args):
        if (args[0] == None):
            args[0] = 0
        if (args[2] == None):
            args[2] = 0

        # if (args[0] in error_literals or args[2] in error_literals):
        #     return CellError(CellErrorType.BAD_REFERENCE, "Invalid cell reference")

        if args[1] == '+':
            return decimal.Decimal(decimal.Decimal(args[0])+decimal.Decimal(args[2]))
        elif args[1] == '-':
            return decimal.Decimal(decimal.Decimal(args[0])-decimal.Decimal(args[2]))
        else:
            raise Exception

    def mul_expr(self, args):
        if args[1] == '/' and str(args[2]) == '0':
            return CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by 0", 'division by zero')
        # if (args[0] in error_literals or args[2] in error_literals):
        #     return CellError(CellErrorType.BAD_REFERENCE, "Invalid cell reference")
        if args[1] == '*':
            return decimal.Decimal(decimal.Decimal(args[0])*decimal.Decimal(args[2]))
        elif args[1] == '/':
            return decimal.Decimal(decimal.Decimal(args[0])/decimal.Decimal(args[2]))
        else:
            raise Exception

    def concat_expr(self, args):
        if(args[0] == None):
            args[0] = ''
        if(args[1] == None):
            args[1] = ''   

        return str(str(args[0])+str(args[1]))

    def cell(self, args):
        # if using the current sheet
        if len(args) == 1:      
            sheet_name = self.sheet_instance.sheet_name
            cell = args[0]
        # if using a different sheet
        elif len(args) == 2:    
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                return CellError(CellErrorType.BAD_REFERENCE, "Invalid cell reference", None)
            cell = args[1]
        else:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid cell reference", None)

        try:
            cell_value = self.workbook_instance.get_cell_value(sheet_name, cell)
        except:
            return CellError(CellErrorType.BAD_REFERENCE, "Invalid cell reference", None)

        # if cell_value == None:
        #    cell_value = 0 # TODO "" for string

        return cell_value
