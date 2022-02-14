# Object class for individual cell
import lark
import decimal
from .eval_expressions import EvalExpressions, generate_error_object
from .cell_error import CellErrorType, CellError
from decimal import *

class Cell():
    def __init__ (self, contents):
        self.contents = contents
        self.parse_necessary = True

        # check that the cell is either a string or None
        if not isinstance(contents, str) and contents != None:
            raise TypeError('Content is not a string.')

        # TODO if a number is given for contents an error should be raised
        # Determine Cell Type
        if str(contents)[0] == '=':
            self.type = "FORMULA"
            # self.value = self.get_cell_value(contents) # TODO curr_sheet needed
        elif str(contents)[0] == "'":
            #if string is a number,
            if self.is_float(str(contents[1:])):
                self.type = "LITERAL"
                self.value = decimal.Decimal(str(contents[1:]))
            else:
                self.type = "STRING"
                self.value = str(contents[1:]) 
        elif self.is_float(str(contents)):
            self.type = "LITERAL"
            self.value = decimal.Decimal(str(contents))
        elif str(contents) == "" or str(contents).isspace():
            self.type = "NONE"
            self.content = None
            self.value = None
        #ONLY VALUE CAN BE CELLERROR OBJECTS, CONTENTS CANNOT BE CELLERROR OBJECTS
        #CONTENTS CAN BE ERROR STRING REPRESENTATIONS BUT NOT THE CELLERROR OBJECT
        else:
            self.type = "LITERAL"
            self.value = str(contents)
        self.parent_cells = {}
        self.children_cells = {}
        self.parent_sheet = None
    
    def get_children_cells(self):
        return self.children_cells
    
    def add_child_cell(self, location, value):
        self.children_cells[location] = value

    def get_cell_value(self, workbook_instance, sheet_instance):

        #digit case
        if str(self.contents)[0] != '=' and str(self.contents)[0] != "'":
            return self.remove_trailing_zeros(self.value)
        #string case
        elif self.contents[0] == "'":
            return self.remove_trailing_zeros(self.value)
        
        if self.parse_necessary:
            # trying to parse
            try:
                parser = lark.Lark.open('sheets/formulas.lark', start='formula')
                self.parsed_contents = parser.parse(self.contents)
                self.parse_necessary = False
            except:
                return CellError(CellErrorType.PARSE_ERROR, 'Unable to parse formula' ,'Parse Error')
            
        # trying to evaluate
        try: 
            evaluation = EvalExpressions(workbook_instance,sheet_instance).transform(self.parsed_contents)
            if isinstance(evaluation, CellError):
                return evaluation
        except lark.exceptions.VisitError as e:
            
            if isinstance(e.__context__, ZeroDivisionError):
                """ Value you set is the cell error OBJECT
                String is what the user sees/inputs 
                if get_cell_value evaluates to error, return value will be cell error object
                Can manually set cell error via #DIV/0! and so on
                set cell contents should only take strings """

                evaluation = CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by 0", ZeroDivisionError)
                # return the above error

            elif isinstance(e.__context__, TypeError):
                evaluation = CellError(CellErrorType.TYPE_ERROR, "Incompatible types for operation")

            elif isinstance(e.__context__, NameError):
                evaluation = CellError(CellErrorType.BAD_NAME, "Unrecognized function name", NameError)

            else:
                evaluation = CellError(CellErrorType.BAD_REFERENCE, "206: Invalid Cell Reference", None)
        


        return self.remove_trailing_zeros(evaluation)
  
    def is_float(self, element):
        """ helper fuction to determine if a value is a float """
        element = str(element)
        try:
            float(element)
            return True
        except ValueError:
            return False

    def remove_trailing_zeros(self, d):
        """ 
        helper function to remove trailing zeros from decimal.Decimal() 
        from: https://docs.python.org/3/library/decimal.html#decimal-faq
        """
        if isinstance(d,decimal.Decimal):
            return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()
        else:
            return d
