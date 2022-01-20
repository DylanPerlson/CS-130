# Object class for individual cell
from asyncio.windows_events import NULL
from collections import defaultdict
import lark
from .eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError

class Cell():
    def __init__ (self, contents):
        # Determine Cell Type
        self.contents = contents
<<<<<<< HEAD
        if contents[0] == '=':
=======

        if str(contents)[0] == '=':
>>>>>>> 09901bd968c93a64c3752088f345d6965a07f6d7
            self.type = "FORMULA"
            #self.value = self.get_cell_value(contents) # TODO curr_sheet needed

        elif str(contents)[0] == "'":
            self.type = "STRING"
            self.value = str(contents[1:]) 
            # TODO bring back if there is an error here
        elif str(contents)[0].isdigit():
            self.type = "LITERAL"
<<<<<<< HEAD
            #self.value = contents
        self.edges = []
    
    # function to add an edge to graph
    # Need to call this if formula is updated to reference another cell
    def add_cell_dependency(self,v):
        new_edge = (self, v)
        self.edges.append(v)
=======
            self.value = contents
        else:
            self.type = "NONE"
            self.value = None
>>>>>>> 09901bd968c93a64c3752088f345d6965a07f6d7


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
<<<<<<< HEAD
            parse_error = CellError(CellErrorType.PARSE_ERROR, "#ERROR!", "Parse Error")
            exit()
=======
            return CellError(CellErrorType.PARSE_ERROR,'#ERROR!','Parse Error')
            
>>>>>>> 09901bd968c93a64c3752088f345d6965a07f6d7

        # trying to evaluate
        try: 
            evaluation = EvalExpressions(workbook_instance,sheet_instance).transform(formula)
        except lark.exceptions.VisitError as e:
            if isinstance(e.__context__, ZeroDivisionError):
                # Value you set is the cell error OBJECT
                # String is what the user sees/inputs 
                # if get_cell_value evaluates to error, return value will be cell error object
                # Can manually set cell error via #DIV/0! and so on
                # set cell contents should only take strings
                div_zero_error = CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by 0", ZeroDivisionError)
                # return the above error
                evaluation = '#DIV/0!'
                #print('zero error') # TODO DIVIDE_BY_ZERO 
                exit()

            elif isinstance(e.__context__, NameError):
                div_zero_error = CellError(CellErrorType.BAD_NAME, "Unrecognized function name", NameError)
                evaluation = '#NAME?'
                #print('type error') # TODO TYPE_ERROR 
                exit()

            else:
                bad_ref_error = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
                #print('other error')
                exit()

        return evaluation
