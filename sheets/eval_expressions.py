"""object class for evaluating expressions"""

import decimal

from lark import Transformer, Visitor

from .cell_error import CellError, CellErrorType

error_literals = ['#REF!', '#ERROR!', '#CIRCREF!', '#VALUE!', '#DIV/0!', '#NAME?']

def generate_error_object(error_arg, return_arg = False):
    """Helper function to generate error objects when parsing formulas
    Error literals are strings
    Might be creating cellerror objects
    """
    # if isinstance(error_arg, CellError):
    #     cell_error_obj = error_arg
    if error_arg == '#REF!':
        return CellError(CellErrorType.BAD_REFERENCE, "204: Invalid cell reference")
    elif error_arg == '#ERROR!':
        return CellError(CellErrorType.PARSE_ERROR, "Parse Error")
    elif error_arg == '#CIRCREF!':
        return CellError(CellErrorType.CIRCULAR_REFERENCE, "Circular reference")
    elif error_arg == '#VALUE!':
        return CellError(CellErrorType.TYPE_ERROR, "Incompatible types for operation")
    elif error_arg == '#DIV/0!':
        return CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by 0")
    elif error_arg == '#NAME?':
        return CellError(CellErrorType.BAD_NAME, "Unrecognized function name")

    # assert False, 'Unrecognized error literal'

    if return_arg:
        return

    assert return_arg, 'Unrecognized error literal'

def _is_float(element):
    """ helper fuction to determine if a value is a float """
    element = str(element)
    try:
        float(element)
        return True
    except ValueError:
        return False

def _get_value_as_number(curr_arg):
    if isinstance(curr_arg, CellError) or isinstance(curr_arg, decimal.Decimal):
        return curr_arg
    elif curr_arg is None:
        return 0
    elif isinstance(curr_arg, str):
        if _is_float(curr_arg):
            return decimal.Decimal(curr_arg)
        else:
            return CellError(CellErrorType.TYPE_ERROR, "String cannot be parsed into a number")
    else:
        return CellError(CellErrorType.TYPE_ERROR, f"Invalid operation with argument: {curr_arg}")

def _get_value_as_string(curr_arg):
    if isinstance(curr_arg, CellError) or isinstance(curr_arg, str):
        return curr_arg
    elif curr_arg is None:
        return ''
    elif isinstance(curr_arg, decimal.Decimal):
        return str(curr_arg)
    else:
        return CellError(CellErrorType.TYPE_ERROR, "Argument is not a string")

#Use this somewhere

class RetrieveReferences(Visitor):
    """This class is used to retrieve all cell references
    It acts as a visitor on a lark object.
    """

    def __init__(self, sheet_instance):
        """Initializes class."""
        self.references = []
        self.sheet_instance = sheet_instance
        self.error_occurred = False

    def cell(self, args):
        """The cell value is returned."""
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
        """Initializes class."""
        self.workbook_instance = workbook_instance
        self.sheet_instance = sheet_instance

    def error(self, args):
        """If an error is encountered, the error is propagated"""
        return generate_error_object(args[0])

    def number(self, args):
        """If a number is encountered, it is put into the right format."""
        d = decimal.Decimal(args[0])
        return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()

    def string(self, args):
        """If a string is encountered, it is put into the right format."""
        return args[0][1:-1] # the '[1:-1]' is to remove the double quotes

    def unary_op(self, args):
        """Unitary operator is applied when encountered in parsed formula."""
        if isinstance(args[1], CellError):
            return args[1]
        if args[0] == '+':
            return decimal.Decimal(args[1])
        elif args[0] == '-':
            return decimal.Decimal(-args[1])
        else:
            raise Exception(f'Unexpected unary operator {args[0]}')

    def parens(self, args):
        """Parentheses are applied on the parsed formula."""
        return args[0]

    def add_expr(self, args):
        """Additive operation is applied on parsed formula."""
        args0 = _get_value_as_number(args[0])
        args2 = _get_value_as_number(args[2])
        if isinstance(args0, CellError):
            return args0
        if isinstance(args2, CellError):
            return args2

        if args[1] == '+':
            return args0+args2
        elif args[1] == '-':
            return args0-args2
        else:
            raise Exception(f'Unexpected addition operator {args[1]}')

    def mul_expr(self, args):
        """Multiplicative operation is applied on parsed formula."""
        args0 = _get_value_as_number(args[0])
        args2 = _get_value_as_number(args[2])
        if isinstance(args0, CellError):
            return args0
        if isinstance(args2, CellError):
            return args2

        if args[1] == '*':
            return args0 * args2
        elif args[1] == '/':
            if args2 != 0:
                return args0 / args2
            else:
                return CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by zero")
        else:
            raise Exception(f'Unexpected multiplication operator {args[1]}')

    def concat_expr(self, args):
        """Concatenation operation is applied on parsed formula."""
        args0 = _get_value_as_string(args[0])
        args1 = _get_value_as_string(args[1])

        if isinstance(args0, CellError):
            return args0
        if isinstance(args1, CellError):
            return args1

        return args0 + args1

    def cell(self, args):
        """The cell value is returned."""

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
                return CellError(CellErrorType.BAD_REFERENCE, "200: Invalid cell reference")
            cell = args[1]
        else:
            return CellError(CellErrorType.BAD_REFERENCE, "201: Invalid cell reference")

        # delete the dollar sign from the cell reference
        cell = cell.replace("$","")

        return self.workbook_instance.get_cell_value(sheet_name, cell)

    #### METHODS FOR BOOLEAN STUFF:

    def bool_lit(self, args):
        print(args[0].lower())
        if args[0].lower() == "true":
            print('here')
            return True
        elif args[0].lower() == "false":
            return False
        else:
            return CellError(CellErrorType.PARSE_ERROR,
            f"Boolean value is not recognized: {args[0]}")

    def bool_oper(self, args):
        operation = args[1]
        args0 = args[0]
        args2 = args[2]

        if operation == "=" or operation == "==":
            pass

        elif operation == "<>" or operation == "!=":
            pass

        elif operation == ">":
            pass

        elif operation == "<":
            pass

        elif operation == ">=":
            pass

        elif operation == "<=":
            pass


    # def bool_func(self, args):
        # pseudocode:
        #     import some new module
        #     pass args to module
        #     return the solution