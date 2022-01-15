import os 
clear = lambda: os.system('cls'); clear() # clear the command window
print('################## NEW RUN ##################\n')

import lark
from lark import Tree, Transformer

contents = '=5*4+10+5*5'

parser = lark.Lark.open('sheets/formulas.lark', start='formula')
formula = parser.parse(contents)

# used to evaluate an expression from the parsed formula
class EvalExpressions(Transformer):
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
        return 1 # TODO somehow use get_cell_value() here

    def parens(self, args):
        pass
    
# print(formula.pretty())

evaluation = EvalExpressions().transform( formula )
print('below should be:', eval(contents[1:]))
print('evaluation:', evaluation)


''' to implement:
parens
concat_exxpr
string
unary_op
'''
        
''' example code from the documentation:
t = Tree('a', [Tree('expr', ['1+2'])])
print(t)
print(EvalExpressions().transform(t))
'''
