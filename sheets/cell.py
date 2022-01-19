# Object class for individual cell

import lark
from .eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError

class Cell:
    def __init__ (self, contents, curr_sheet):
        # Determine Cell Type
        self.contents = contents

        if contents[0] == '=':
            self.type = "FORMULA"
            self.value = self.get_value_from_contents(contents) # TODO curr_sheet needed

        elif contents[0] == "'":
            self.type = "STRING"
            self.value = str(contents)

        elif (contents[0]).isdigit():
            self.type = "LITERAL"
            self.value = contents
        else:
            self.type = "NONE"
            self.value = None


    def get_value_from_contents(self, contents):
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')

        # trying to parse
        try:
            formula = parser.parse(contents)
        except:
            return CellError(CellErrorType.PARSE_ERROR,'#ERROR!','Parse Error')
            

        # trying to evaluate
        try: 
            evaluation = EvalExpressions().transform(formula)
        except lark.exceptions.VisitError as e:

            if isinstance(e.__context__, ZeroDivisionError):
                print('zero error') # TODO DIVIDE_BY_ZERO 
                exit()

            elif isinstance(e.__context__, NameError):
                print('type error') # TODO TYPE_ERROR 
                exit()

            else:
                print('other error')
                exit()

        return evaluation