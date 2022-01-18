# Object class for individual cell

import lark
from eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError

class Cell:
    def __init__ (self, contents, curr_sheet):
        # Determine Cell Type
        # self.contents = contents

        if contents[0] == '=':
            self.type = "FORMULA"
            self.value = self.get_value_from_contents(contents)

        elif contents[0] == "'":
            self.type = "STRING"
            #self.value = str(contents)

        else:
            self.type = "LITERAL"
            #self.value = contents


    def get_value_from_contents(self, contents):
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')

        try:
            formula = parser.parse(contents)
        except:
            print('error') # TODO error
            exit()

        evaluation = EvalExpressions().transform(formula)
        
        return evaluation