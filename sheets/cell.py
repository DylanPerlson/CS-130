# Object class for individual cell

import lark
import decimal
from .eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError
from decimal import *

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
            self.value = decimal.Decimal(contents)
        elif str(contents) == "" or str(contents).isspace():
            self.type = "NONE"
            self.content = None
            self.value = None
        else:
            self.type = "LITERAL"
            self.value = str(contents)


    def get_cell_value(self, workbook_instance, sheet_instance):
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')

        #digit case
        if str(self.contents)[0] != '=' and str(self.contents)[0] != "'":
            return self.value
        #string case
        elif self.contents[0] == "'":
            # return self.contents[1:]
            return self.value
        # print(self.contents)
        # trying to parse
        try:
            formula = parser.parse(self.contents)
        except:
            return CellError(CellErrorType.PARSE_ERROR,'#ERROR!','Parse Error')
            
        # print(formula.pretty())
        # trying to evaluate
        try: 
            evaluation = EvalExpressions(workbook_instance,sheet_instance).transform(formula)
            # print('\n\n',type(evaluation))
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
        
        # if isinstance(evaluation,decimal.Decimal):
        #     print('###')
        #     print(evaluation)
            
        #     evaluation = decimal.Decimal(str(evaluation).strip('0'))
        #     print(evaluation)

        return evaluation