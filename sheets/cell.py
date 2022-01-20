# Object class for individual cell
from asyncio.windows_events import NULL
from collections import defaultdict
import lark
from eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError

class Cell:
    def __init__ (self, contents, curr_sheet):
        # Determine Cell Type
        self.contents = contents
        if contents[0] == '=':
            self.type = "FORMULA"
            self.value = self.get_value_from_contents(contents)

        elif contents[0] == "'":
            self.type = "STRING"
            #self.value = str(contents)

        else:
            self.type = "LITERAL"
            #self.value = contents
        self.edges = []
    
    # function to add an edge to graph
    # Need to call this if formula is updated to reference another cell
    def add_cell_dependency(self,v):
        new_edge = (self, v)
        self.edges.append(v)


    def get_value_from_contents(self, contents):
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')

        # trying to parse
        try:
            formula = parser.parse(contents)
        except:
            parse_error = CellError(CellErrorType.PARSE_ERROR, "#ERROR!", "Parse Error")
            exit()

        # trying to evaluate
        try: 
            evaluation = EvalExpressions().transform(formula)
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
