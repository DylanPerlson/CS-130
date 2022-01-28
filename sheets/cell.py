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
        
<<<<<<< HEAD
        """ trying to strip trailing zeros of decimal objects
        if isinstance(evaluation,decimal.Decimal):
            print('###')
            print(evaluation)
            
            evaluation = decimal.Decimal(str(evaluation).strip('0'))
            print(evaluation) """

        return evaluation
=======
        # trying to strip trailing zeros of decimal objects
        # if isinstance(evaluation,decimal.Decimal):
        #     print(str(evaluation))
        #     evaluation = self.remove_trailing_zeros(evaluation)
        #     print(str(evaluation))
        
        # print('here')
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
>>>>>>> 993bc359c396309baba3d0ca9f2659b91795f148
