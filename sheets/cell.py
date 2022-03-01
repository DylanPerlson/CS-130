"""Object class for individual cell"""
#from binascii import a2b_base64
import decimal

import lark

from .cell_error import CellError, CellErrorType
from .eval_expressions import EvalExpressions
from .eval_expressions import generate_error_object


class Cell():
    """Class that defines a cell object."""
    def __init__ (self, contents):
        self.contents = contents
        self.parse_necessary = True
        self.evaluated_value = None
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
            self.type = "STRING"
            self.value = str(contents[1:].replace("''","'"))
        elif self.is_float(str(contents)):
            self.type = "NUMBER"
            self.value = decimal.Decimal(str(contents))
        elif isinstance(generate_error_object(contents, return_arg = True), CellError):
            self.type = "ERROR"
            self.value = generate_error_object(contents)
        elif str(contents).lower() == "true" or str(contents).lower() == "false":
            self.type = "BOOLEAN"
            if str(contents).lower() == "true":
                self.value = True
            else:
                self.value = False
        #ONLY VALUE CAN BE CELLERROR OBJECTS, CONTENTS CANNOT BE CELLERROR OBJECTS
        #CONTENTS CAN BE ERROR STRING REPRESENTATIONS BUT NOT THE CELLERROR OBJECT
        else:
            self.type = "STRING"
            self.value = str(contents)

    def get_cell_value(self, workbook_instance, sheet_instance, location):
        """Get the value of this cell."""
        #DELTE THIS. THIS IS TESTING PERFORMANCE
        
        sheet_location = sheet_instance.sheet_name + '!' + location

        if workbook_instance.cell_changed_dict[sheet_location.lower()] == False and self.contents is not None:
            return self.evaluated_value 


        #otherwise now we need to re-evaluate
        #set changed to False, because we will evaluate it now
        workbook_instance.cell_changed_dict[sheet_location.lower()] = False
        #self.not_changed = True


        #None case
        if self.type == "NONE":
            self.evaluated_value = None
            return self.evaluated_value
        # digit case
        elif self.type == "NUMBER": #str(self.contents)[0] != '=' and str(self.contents)[0] != "'":
            self.evaluated_value = self.remove_trailing_zeros(self.value)
            return self.evaluated_value
        #string case
        elif self.type == "STRING": #self.contents[0] == "'":
            self.evaluated_value = self.remove_trailing_zeros(self.value)
            return self.evaluated_value
        elif self.type == "BOOLEAN":
            self.evaluated_value = self.value
            return self.evaluated_value
        elif self.type == "ERROR":
            self.evaluated_value = self.value
            return self.evaluated_value
        else:
            if self.type != "FORMULA":
                raise TypeError(f'Cell object has unrecognized type: {self.type}')

        ### fyi: at this point, it is known that the cell contains a formula

        # parsing the contents
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
            self.evaluated_value = CellError(CellErrorType.DIVIDE_BY_ZERO,
            "Cannot divide by 0", ZeroDivisionError)

            return self.evaluated_value
        except TypeError:
            self.evaluated_value = CellError(CellErrorType.TYPE_ERROR,
            "Incompatible types for operation")

            return self.evaluated_value
        except NameError:
            self.evaluated_value = CellError(CellErrorType.BAD_NAME,
            "Unrecognized function name", NameError)

            return self.evaluated_value
        except(RuntimeError, RecursionError): # this happens if the error is either of those
            self.evaluated_value =  CellError(CellErrorType.CIRCULAR_REFERENCE,
            "Circular Reference", None)
            return self.evaluated_value

        self.evaluated_value = self.remove_trailing_zeros(evaluation)

        # why was this code here?? (Pieter)
        # if self.evaluated_value is None and self.type == 'NONE': #this will always be none
        #     self.evaluated_value = 0
        #     return self.evaluated_value

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
