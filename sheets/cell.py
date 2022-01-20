# Object class for individual cell

import lark
from .eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError

class Cell():
    def __init__ (self, contents):
        # Determine Cell Type
        self.contents = contents

        if str(contents)[0] == '=':
            self.type = "FORMULA"
            #self.value = self.get_cell_value(contents) # TODO curr_sheet needed

        elif str(contents)[0] == "'":
            self.type = "STRING"
            self.value = str(contents[1:]) 
            # TODO bring back if there is an error here
        elif str(contents)[0].isdigit():
            self.type = "LITERAL"
            self.value = contents
        else:
            self.type = "NONE"
            self.value = None


    def get_cell_value(self, workbook_instance, sheet_instance):
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')

        #digit case
        if str(self.contents)[0] != '=' and str(self.contents)[0] != "'":
            return self.contents
        #string case
        elif self.contents[0] == "'":
            return self.contents[1:]
        # trying to parse
        try:
            
            formula = parser.parse(self.contents)
        except:
            return CellError(CellErrorType.PARSE_ERROR,'#ERROR!','Parse Error')
            

        # trying to evaluate
        try: 
            evaluation = EvalExpressions(workbook_instance,sheet_instance).transform(formula)
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