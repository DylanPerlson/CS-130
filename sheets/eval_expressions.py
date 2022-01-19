# object class for evaluating expressions

import lark
from lark import Transformer
from sheets.cell import Cell
from sheets.cell_error import CellError, CellErrorType
# from exceptions import VisitError

# used to evaluate an expression from the parsed formula
class EvalExpressions(Transformer):

    def number(self, args):
        return args[0]

    def string(self, args):
        return args[0][1:-1] # the '[1:-1]' is to remove the double quotes

    def unary_op(self, args):
        return str(args[0]+args[1])

    def parens(self, args):
        return args[0]

    def add_expr(self, args):
        t = str(args[0])+args[1]+str(args[2])

        return eval(t)

    def mul_expr(self, args):
        t = str(args[0])+args[1]+str(args[2])

        return eval(t)

    def concat_expr(self, args):
        return str(args[0]+args[1])

    def cell(self, args):
        # getting the appropriate sheet name and cell location
        if len(args) == 1:      # if using the current sheet
            sheet_name = 'current' # TODO fix
            cell = args[0]
        elif len(args) == 2:    # if using a different sheet
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                bad_ref_error = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
                pass # TODO BAD_REFERENCE
            cell = args[1]
        else:
            bad_ref_error = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
            pass # TODO BAD_REFERENCE

        try:
            cell_value = 1 # TODO get_cell_value(sheet_name, cell) here
        except:
            bad_ref_error = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
            # TODO BAD_REFERENCE 
            exit()

        if cell_value == 'None':
            cell_value = 0 # TODO "" for string

        return cell_value

""" 
# import os; clear = lambda: os.system('cls'); clear() # clear the command window

# testing options
# contents = "=5++4*(6+5)/5*-1-4"
# contents = '="hello" & 5 + "test"'
# contents = '=5 & 3'
contents = '=3/0'
# contents = '=3 * "abc"'
# contents = '="hello" & "world" & "test" & 6 & 4+3'
# contents = '="test"'
# contents = "='test_ 9'!aa33+3"
# contents = "='test_ 9'!aa33+3"
# contents = '="hello"'
# contents = "='hello'"
# contents = '=a1'
# contents = "='test' & 'concat'"

parser = lark.Lark.open('sheets/formulas.lark', start='formula')
try:
    formula = parser.parse(contents)
except:
    print('parse error') # TODO PARSE_ERROR 
    exit()

try: 
    evaluation = EvalExpressions().transform( formula )
except lark.exceptions.VisitError as e:
    if isinstance(e.__context__, ZeroDivisionError):
        print('zero error') # TODO DIVIDE_BY_ZERO 
    elif isinstance(e.__context__, NameError):
        # print(e)
        print('name error')
    else:
        print('other error')

# print(formula.pretty())
# print('evaluation should be:\t', eval(contents[1:]))
# print('evaluation gives:\t', evaluation)
 """