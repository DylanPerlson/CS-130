# Object class for individual cell

import lark
from cell_error import CellErrorType, CellError

class Cell:
    def __init__ (self, contents, curr_sheet):
        # Determine Cell Type
        # self.contents = contents

        if contents[0] == '=':
            #check to make sure no obvious errors
            

            
            # if an error is encountered
            if contents.find('/0'):
                error = CellError(CellErrorType.DIVIDE_BY_ZERO, "Divide By Zero", "None")
                self.value = error
                
            else:
                self.type = "FORMULA"
                self.value = self.get_value_from_contents(contents)

        elif contents[0] == "'":
            self.type = "STRING"
            #self.value = str(contents)
        else:
            self.type = "LITERAL"
            #self.value = contents


    def get_value_from_contents(self, contents): # assume that contents is '=a1'  '=aa234 + 4 - b1'
        
        
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')
        formula = parser.parse(contents).pretty()

        #Parsing formula and pushing operations onto stack inside out
        stack = []
        for i in formula.splitlines(): 
            if len(stack) > 0:
                prev = stack[-1]
            
            if i == 'add_expr':
                stack.append()
                pass
            elif i == 'mul_expr':
                stack.append('*')
            elif i == 'number':
                pass    
            elif i == 'cell':
                # TODO check to make sure that the cell reference is valid, if not error
                
                # get_cell_contents
                pass     
            elif i == 'concat_expr':
                pass
            elif i == 'string':
                pass
            else:
                print('houston, we have a problem')
                pass
        
        #Pop off stack and calculate formula
        while (len(stack) > 0):
            pass
                

# add_expr
#   cell  A1
#   +
#   mul_expr
#     number      3
#     *
#     cell
#       test
#       A2


        for i in contents:
            if i == '=':
                continue
            elif i == ' ':
                continue
            # elif i ==  "'":
            #     # some string will be
            # elif i.isdigit():
            #     skip all the way to the end until no ore digits
            # elif i == string Char 

            #     a13+
            #     balance!a13+
            #     get every character following it that is a string and a number until there is somethign that isnt a number

        

        # balances!a3