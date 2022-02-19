"""Object class for individual cell"""
#from binascii import a2b_base64
import decimal
#from locale import ABDAY_1

import lark

from .cell_error import CellError, CellErrorType
from .eval_expressions import EvalExpressions


class Cell():
    """Class that defines a cell object."""
    def __init__ (self, contents):
        self.contents = contents
        self.parse_necessary = True
        self.evaluated_value = None #TODO is this the way to use the evaluated value???
        self.value = None
        self.parsed_contents = ''
        
        

        # check that the cell is either a string or None
        if not isinstance(contents, str) and contents is not None:
            raise TypeError('Content is not a string.')

        # Determine Cell Type
        if str(contents) == "" or str(contents).isspace():
            self.type = "NONE"
            self.content = None
            self.value = None
        elif str(contents)[0] == '=':
            self.type = "FORMULA"
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

        #ONLY VALUE CAN BE CELLERROR OBJECTS, CONTENTS CANNOT BE CELLERROR OBJECTS
        #CONTENTS CAN BE ERROR STRING REPRESENTATIONS BUT NOT THE CELLERROR OBJECT
        else:
            self.type = "LITERAL"
            self.value = str(contents)


    def get_cell_value(self, workbook_instance, sheet_instance, location):
        """Get the value of this cell."""
        sheet_location = sheet_instance.sheet_name + '!' + location
        
        #if that cell has been changed just return the evaluated value
        
        
        if workbook_instance.cell_changed_dict[sheet_location.lower()] == False and self.contents is not None:
            return self.evaluated_value #TODO we need to change this



        #otherwise now we need to re-evaluate
        #set changed to False, because we will evaluate it now
        #TODO move this???
        #workbook_instance.cell_changed_dict[sheet_location.lower()] = False

        #None case
        if self.type == "NONE":
            self.evaluated_value = 0
            return self.evaluated_value
        #digit case
        elif str(self.contents)[0] != '=' and str(self.contents)[0] != "'":
            self.evaluated_value = self.remove_trailing_zeros(self.value)
            return self.evaluated_value
        #string case
        elif self.contents[0] == "'":
            self.evaluated_value = self.remove_trailing_zeros(self.value)
            return self.evaluated_value

        if self.parse_necessary:
            # trying to parse
            try:
                parser = lark.Lark.open('sheets/formulas.lark', start='formula')
                self.parsed_contents = parser.parse(self.contents)
                self.parse_necessary = False
            except lark.exceptions.LarkError:
                self.evaluated_value = CellError(CellErrorType.PARSE_ERROR,
                'Unable to parse formula', lark.exceptions.LarkError)
                return self.evaluated_value

        # trying to evaluate
        try:
            evaluation =\
                EvalExpressions(workbook_instance,sheet_instance).transform(self.parsed_contents)
            if isinstance(evaluation, CellError):
                self.evaluated_value = evaluation
                return self.evaluated_value
        except ZeroDivisionError:
            # Value you set is the cell error OBJECT
            # String is what the user sees/inputs
            # if get_cell_value evaluates to error, return value will be cell error object
            # Can manually set cell error via #DIV/0! and so on
            # set cell contents should only take strings
            self.evaluated_value = CellError(CellErrorType.DIVIDE_BY_ZERO,
            "Cannot divide by 0", ZeroDivisionError)

            return self.evaluated_value
            # return the above error

        except TypeError:
            self.evaluated_value = CellError(CellErrorType.TYPE_ERROR,
            "Incompatible types for operation")

            return self.evaluated_value

        except NameError:
            self.evaluated_value = CellError(CellErrorType.BAD_NAME,
            "Unrecognized function name", NameError)

            return self.evaluated_value

        except RuntimeError or RecursionError:
             
            self.evaluated_value =  CellError(CellErrorType.CIRCULAR_REFERENCE, 
            "Circular Reference", None)
            return self.evaluated_value 
        except Exception as e: #TODO bad practice
            print(e)
            self.evaluated_value = CellError(CellErrorType.BAD_REFERENCE, 
            "206: Invalid Cell Reference", None)
            return self.evaluated_value

        self.evaluated_value = self.remove_trailing_zeros(evaluation)
       

        if self.evaluated_value is None: #this will always be none
            self.evaluated_value  = 0
            return self.evaluated_value

        
        return self.evaluated_value

        
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
