# Object class for individual cell
import lark
import decimal
from .eval_expressions import EvalExpressions
from .cell_error import CellErrorType, CellError
from decimal import *

class Cell():
    def __init__ (self, contents):
        self.contents = contents

        # Determine Cell Type
        if str(contents)[0] == '=':
            self.type = "FORMULA"
            
            # self.value = self.get_cell_value(contents) # TODO curr_sheet needed
        # TODO if a number is given for contents an error should be raised
        elif str(contents)[0] == "'":
            #if string is a number,
            if self.is_float(str(contents[1:])):
                self.type = "LITERAL"
                self.value = decimal.Decimal(contents[1:])
                

            else:
                self.type = "STRING"
                self.value = str(contents[1:]) 
            
        elif self.is_float(str(contents)):
            self.type = "LITERAL"
            self.value = decimal.Decimal(contents)
        elif str(contents) == "" or str(contents).isspace():
            self.type = "NONE"
            self.content = None
            self.value = None

    

    def get_cell_value(self, workbook_instance, sheet_instance):
        parser = lark.Lark.open('sheets/formulas.lark', start='formula')

        #digit case
        if str(self.contents)[0] != '=' and str(self.contents)[0] != "'":
            return self.remove_trailing_zeros(self.value)
        #string case
        elif self.contents[0] == "'":
            return self.remove_trailing_zeros(self.value)

        # trying to parse
        try:
            formula = parser.parse(self.contents)
        except:
            return CellError(CellErrorType.PARSE_ERROR, 'Unable to parse formula' ,'Parse Error')
            
        # trying to evaluate
        try: 
            evaluation = EvalExpressions(workbook_instance,sheet_instance).transform(formula)
        except lark.exceptions.VisitError as e:
            if isinstance(e.__context__, ZeroDivisionError):
                """ Value you set is the cell error OBJECT
                String is what the user sees/inputs 
                if get_cell_value evaluates to error, return value will be cell error object
                Can manually set cell error via #DIV/0! and so on
                set cell contents should only take strings """

                evaluation = CellError(CellErrorType.DIVIDE_BY_ZERO, "Cannot divide by 0", ZeroDivisionError)
                # return the above error

            elif isinstance(e.__context__, NameError):
                evaluation = CellError(CellErrorType.BAD_NAME, "Unrecognized function name", NameError)

            else:
                evaluation = CellError(CellErrorType.BAD_REFERENCE, "#BAD_REF!", None)
        


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
