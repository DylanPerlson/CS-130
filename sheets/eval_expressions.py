import os
clear = lambda: os.system('cls'); clear() # clear the command window
print('################## NEW RUN ##################\n')

import lark
from lark import Tree, Transformer

# contents = '="hello" & "world" & "test" & 6 & 4+3'
# contents = '="test"'
# contents = "='test_ 9'!aa33+3"
contents = "='test_ 9'!aa33+3"
# contents = '="hello"'
# contents = "='hello'"
# contents = '=a1'
# contents = "='test' & 'concat'"

parser = lark.Lark.open('sheets/formulas.lark', start='formula')
try:
    formula = parser.parse(contents)
except:
    print('error') # TODO error
    exit()

# used to evaluate an expression from the parsed formula
class EvalExpressions(Transformer):
    # def __init__(self):



    def mul_expr(self, args):
        t = str(args[0])+args[1]+str(args[2])

        # print('args:',args)
        # print('t:',t)

        return eval(t)

    def number(self, args):

        # print('number args:', args[0])
        
        return args[0]

    def add_expr(self, args):

        t = str(args[0])+args[1]+str(args[2])

        # print('add args:',args)
        # print('t:',t)

        return eval(t)

    def cell(self, args):
        if len(args) == 1:
            sheet_name = 'current' 
            cell = args[0]
        elif len(args) == 2:
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                pass # TODO error
            cell = args[1]
        else:
            pass # TODO error

        print('sheet:', sheet_name)
        print('cell:', cell)

        cell_value = 1 # TODO get_cell_value(sheet_name, cell)

        if cell_value == 'None':
            cell_value = 0 # TODO "" for string

        return cell_value

    def parens(self, args):
        return args[0]

    def unary_op(self, args):
        return str(args[0]+args[1])

    def string(self, args):
        # pass
        return args[0][1:-1] # the '[1:-1]' is to remove the double quotes

    def concat_expr(self, args):
        # pass
        print(args[0])
        print(args[1])
        # return str('"'+args[0]+args[1]+'"')
        return str(args[0]+args[1])
    
print(formula.pretty())

evaluation = EvalExpressions().transform( formula )
# print('below should be:', eval(contents[1:]))
print('evaluation:', evaluation)


''' to implement:
'''
        
''' example code from the documentation:
t = Tree('a', [Tree('expr', ['1+2'])])
print(t)
print(EvalExpressions().transform(t))
'''
