"""object class for evaluating expressions"""

import decimal

from lark import Transformer, Token #Visitor was removed here

from .cell_error import CellError, CellErrorType
from .functions import Functions

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

#TODO (Dylan) DTP FIX THIS
def _get_value_as_number(curr_arg):
    if isinstance(curr_arg, CellError) or isinstance(curr_arg, decimal.Decimal):
        return curr_arg
    elif curr_arg is None:
        return decimal.Decimal('0')
    elif isinstance(curr_arg, str):
        if _is_float(curr_arg):
            return decimal.Decimal(curr_arg)
        else:
            return CellError(CellErrorType.TYPE_ERROR, "String cannot be parsed into a number")
    elif isinstance(curr_arg, bool):
        return int(curr_arg)

    return CellError(CellErrorType.TYPE_ERROR, f"Invalid operation with argument: {curr_arg}")

def _get_value_as_string(curr_arg):
    if isinstance(curr_arg, CellError) or isinstance(curr_arg, str):
        return curr_arg
    elif curr_arg is None:
        return ''
    elif isinstance(curr_arg, decimal.Decimal):
        return str(curr_arg)
    elif isinstance(curr_arg, bool):
        return str(curr_arg).upper()

    return CellError(CellErrorType.TYPE_ERROR, "Argument is not a string")

def _get_value_as_bool(curr_arg):
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

def _order_types(a):
    if isinstance(a, bool):
        return 3 # highest priority
    elif isinstance(a, str):
        return 2 # second highest priority
    elif isinstance(a, decimal.Decimal):
        return 1 # lowest priority
    else:
        return 0

def _compare(a, op, b):
    if op ==  '<':
        return a < b
    elif op ==  '>':
        return a > b
    elif op ==  '<=':
        return a <= b
    elif op ==  '>=':
        return a >= b


class EvalExpressions(Transformer):
    """Used to evaluate an expression from the parsed formula:"""

    def __init__(self, workbook_instance, sheet_instance):
        """Initializes class."""
        self.workbook_instance = workbook_instance
        self.sheet_instance = sheet_instance
        self.functions = Functions()
        self.cell_signal = False

    def error(self, args):
        """If an error is encountered, the error is propagated"""
        #get the old arg values
        args = self._args(args)

        return generate_error_object(args[0])

    def number(self, args):
        """If a number is encountered, it is put into the right format."""
        #get the old arg values
        args = self._args(args)

        d = decimal.Decimal(args[0])
        return self.remove_trailing_zeros(d)


    def string(self, args):
        """If a string is encountered, it is put into the right format."""
        #get the old arg values
        args = self._args(args)

        return args[0][1:-1] # the '[1:-1]' is to remove the double quotes

    def unary_op(self, args):
        #get the old arg values
        args = self._args(args)

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
        #get the old arg values
        args = self._args(args)

        return args[0]

    def add_expr(self, args):
        """Additive operation is applied on parsed formula."""
        args = self._args(args)

        args0 = _get_value_as_number(args[0])
        args2 = _get_value_as_number(args[2])
        # Determine return error based on priority in cell_error.py
        if isinstance(args0, CellError) and isinstance(args2, CellError):
            if args0.get_type().value < args2.get_type().value:
                return args0
            else:
                return args2
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
        args = self._args(args)

        args0 = _get_value_as_number(args[0])
        args2 = _get_value_as_number(args[2])
        # Determine return error based on priority in cell_error.py
        if isinstance(args0, CellError) and isinstance(args2, CellError):
            if args0.get_type().value < args2.get_type().value:
                return args0
            else:
                return args2

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

    def cell_range(self, args):

        #check if it is in another sheet
        if self.sheet_instance.sheet_name.lower() != args[0][1].lower():
            #need to change sheet instance to proper one
            for s in self.workbook_instance.sheets:
                if s.sheet_name.lower() == args[0][1].lower():
                    sheet_inst = s

        #otherwise treat normally
        else:
            sheet_inst = self.sheet_instance

        p1 = args[0][2]
        p2 = args[1][2]
        r1,c1 = sheet_inst._get_col_and_row(p1)
        r2,c2 = sheet_inst._get_col_and_row(p2)

        edge1 = (min(r1,r2),min(c1,c2))
        edge2 = (max(r1,r2),max(c1,c2))

        r1 = edge1[0]
        c1 = edge1[1]
        r2 = edge2[0]
        c2 = edge2[1]
        vals = []

        # #now get every value in the range
        # for cell in sheet_inst.cells:
        #     cell_row, cell_col = cell[0],cell[1]
        #     if cell_row <= r2 and cell_row >= r1 and cell_col <= c2 and cell_col >= c1:
        #         vals.append(sheet_inst.cells[cell_row,cell_col].evaluated_value)

        # this code returns a matrix instead of a flat list
        for count, row in enumerate(range(r1, r2+1)):
            vals.append([])
            for col in range(c1, c2+1):
                try:
                    val = sheet_inst.cells[row,col].evaluated_value
                except KeyError:
                    val = None
                # print(val)
                vals[count].append(val)

        # transpose matrix
        # because of row v col inconsistency
        vals = [list(x) for x in zip(*vals)]

        return vals


    def concat_expr(self, args):
        """Concatenation operation is applied on parsed formula."""
        #get the old arg values
        args = self._args(args)

        args0 = _get_value_as_string(args[0])
        args1 = _get_value_as_string(args[1])


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
        self.cell_signal = True
        
        for s in self.workbook_instance.sheets:
            if s.sheet_name.lower() == sheet_name.lower():
                return [s.get_cell_value(self.workbook_instance, cell),sheet_name[:], cell]

    #### METHODS FOR BOOLEAN STUFF:

    def bool_lit(self, args):
        """Takes a boolean as string and returns actual bool."""
        #get the old arg values
        args = self._args(args)

        if args[0].lower() == "true":
            return True
        elif args[0].lower() == "false":
            return False
        else:
            return CellError(CellErrorType.PARSE_ERROR,
            f"Boolean value is not recognized: {args[0]}")

    def bool_oper(self, args):
        """Performs boolean operations: ==, <, >, etc."""
        #get the old arg values
        args = self._args(args)

        operation = args[1]
        args0 = args[0]
        args2 = args[2]

        if isinstance(args0, CellError) and isinstance(args2, CellError):
            if args0 < args2:
                return args0
            else:
                return args2
        elif isinstance(args0, CellError):
            return args0
        elif isinstance(args2, CellError):
            return args2

        if args0 is None and args2 is None:
            if operation in ['=', '==', '>=', '<=']:
                return True
            else:
                return False

        if args0 is None:
            if isinstance(args2, str):
                args0 = _get_value_as_string(args0)
            elif isinstance(args2, decimal.Decimal):
                args0 = _get_value_as_number(args0)
            elif isinstance(args2, bool):
                args0 = _get_value_as_bool(args0)

        if args2 is None:
            if isinstance(args2, str):
                args2 = _get_value_as_string(args2)
            elif isinstance(args2, decimal.Decimal):
                args2 = _get_value_as_number(args2)
            elif isinstance(args2, bool):
                args2 = _get_value_as_bool(args2)

        if operation == "=" or operation == "==":
            if not type(args0) is type(args2): # TODO test
                return False
            elif isinstance(args0, str) and isinstance(args2, str):
                return args0.lower() == args2.lower()
            else:
                return args0 == args2

        elif operation == "<>" or operation == "!=":
            if not type(args0) is type(args2): # TODO test
                return True
            elif isinstance(args0, str) and isinstance(args2, str):
                return args0.lower() != args2.lower()
            else:
                return args0 != args2

        elif operation == ">" or \
                operation == "<" or \
                operation == ">=" or \
                operation == "<=":
            if isinstance(args0, str) and isinstance(args2, str):
                return _compare(args0.lower(), operation, args2.lower())
            elif type(args0) is not type(args2):
                args0 = _order_types(args0)
                args2 = _order_types(args2)

            return _compare(args0, operation, args2)

        else:
            CellError(CellErrorType.TYPE_ERROR, f"Invalid operator: {operation}")


    def remove_trailing_zeros(self, d):
        """Removes trailing zeros of decimal.Decimals."""
        #are big numbers getting rounded wrong?? DTP
        if isinstance(d,decimal.Decimal):
            d = str(d)
            d_split = d.split('.')
            #case of no decimal points
            if len(d_split) == 1:
                return decimal.Decimal(d)
            #case of decimal
            else:
                if ('E' not in d):
                    d_split[1] = d_split[1].rstrip('0')
                    d = d_split[0] + '.' + d_split[1]
                    return decimal.Decimal(d)
                else:
                    return decimal.Decimal(d)
        else:
            return d

    def bool_func(self, args):
        #get the old arg values
        args = self._args(args)



        """Performs boolean functions: AND, OR, etc."""
        # pseudocode:
        #     import some new module
        #     pass args to module
        #     return the solution

        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                args[i] = args[i].value

        function_key = args[0]
        if len(args) == 1 and function_key != "VERSION":
            return CellError(CellErrorType.TYPE_ERROR, "At least 1 argument must be present")

        args = args[1:]

        if function_key not in self.workbook_instance.function_directory.keys():
            return CellError(CellErrorType.BAD_NAME, f'"{function_key}" not recognized as function')

        function_val = self.workbook_instance.function_directory[function_key]

        if function_key == "INDIRECT":
            args.extend([self.workbook_instance, self.sheet_instance, self.cell_signal])
            self.cell_signal = False

        # args is now a nice list with the entries
        return self.functions(function_val, args)

    def _args(self,args):
        old_args = args
        args = []
        for i in old_args:
            if i is None:
                continue
            if isinstance(i,list):
                if len(i) > 1 and isinstance(i[1],bool):
                    args.append(i)
                    continue
                if len(i) > 1 and isinstance(i[1],str):
                    args.append(i[0])
                    continue
                else:
                     args.append(i)
            else:
                args.append(i)
        return args
