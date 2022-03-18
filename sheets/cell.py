"""Object class for individual cell"""
#from binascii import a2b_base64
import decimal

import lark
from lark import Visitor
from .cell_error import CellError, CellErrorType
from .eval_expressions import EvalExpressions
from .eval_expressions import generate_error_object


class Cell():
    """Class that defines a cell object."""
    def __init__ (self, contents):
        self.contents = contents
        self.parse_necessary = True
        self.evaluated_value = None
        self.parsed_contents = ''
        self.type = ''
        self.references = []






    def get_cell_value(self, workbook_instance, sheet_instance, location):
        """Get the value of this cell."""

        sheet_location = sheet_instance.sheet_name + '!' + location

        if sheet_location.lower() in workbook_instance.cell_changed_dict:
            if workbook_instance.cell_changed_dict[sheet_location.lower()]\
                is False and self.contents is not None:
                return self.evaluated_value


        #otherwise now we need to re-evaluate
        #set changed to False, because we will evaluate it now
        workbook_instance.cell_changed_dict[sheet_location.lower()] = False


        ## move the determination of type to get cell_val



        # check that the cell is either a string or None
        if not isinstance(self.contents, str) and self.contents is not None:
            raise TypeError('Content is not a string.')

        # Determine Cell Type
        elif str(self.contents) == "" or str(self.contents).isspace() or self.contents is None:
            self.type = "NONE"
            self.evaluated_value = None
            self.references = []
            return self.evaluated_value
        elif str(self.contents)[0] == '=':
            self.type = "FORMULA"
        elif str(self.contents)[0] == "'":
            self.type = "STRING"
            self.evaluated_value = str(self.contents[1:].replace("''","'"))
            self.evaluated_value = self.remove_trailing_zeros(self.evaluated_value)
            return self.evaluated_value
        elif self.is_float(str(self.contents)):
            self.type = "NUMBER"
            self.evaluated_value = decimal.Decimal(str(self.contents))
            self.evaluated_value = self.remove_trailing_zeros(self.evaluated_value)
            return self.evaluated_value
        elif isinstance(generate_error_object(self.contents, return_arg = True), CellError):
            self.type = "ERROR"
            self.evaluated_value = generate_error_object(self.contents)
            return self.evaluated_value
        elif str(self.contents).lower() == "true" or str(self.contents).lower() == "false":
            self.type = "BOOLEAN"
            if str(self.contents).lower() == "true":
                self.evaluated_value = True
            else:
                self.evaluated_value = False
            return self.evaluated_value
        #ONLY VALUE CAN BE CELLERROR OBJECTS, CONTENTS CANNOT BE CELLERROR OBJECTS
        #CONTENTS CAN BE ERROR STRING REPRESENTATIONS BUT NOT THE CELLERROR OBJECT
        else:
            self.type = "STRING"
            self.evaluated_value = str(self.contents)
            return self.evaluated_value

        # if self.type != "FORMULA":
        #     raise TypeError(f'Cell object has unrecognized type: {self.type}')

        ### fyi: at this point, it is known that the cell contains a formula

        # parsing the contents
        #would have returned by this point if it was not a formula
        if self.parse_necessary:
            # trying to parse

            try:

                self.parsed_contents = workbook_instance.parser.parse(self.contents)
                self.parse_necessary = False

                ref = RetrieveReferences(sheet_instance)
                ref.visit(self.parsed_contents)
                self.references = ref.references 
                #eturn ref.reference
            except lark.exceptions.LarkError:
                self.evaluated_value = CellError(CellErrorType.PARSE_ERROR,
                'Unable to parse formula', lark.exceptions.LarkError)
                self.references = []
                return self.evaluated_value

        # trying to evaluate
        try:
            evaluation =\
                    EvalExpressions(workbook_instance,sheet_instance).transform(
                        self.parsed_contents)
            if isinstance(evaluation,list):
                evaluation = evaluation[0]
            if evaluation is None:
                self.evaluated_value = decimal.Decimal('0')
                return self.evaluated_value
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
      

        self.evaluated_value = self.remove_trailing_zeros(evaluation)

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
        """Removes trailing zero of a decimal.Decimal value."""
        if isinstance(d,decimal.Decimal):
            d = str(d)
            d_split = d.split('.')
            #case of no decimal points
            if len(d_split) == 1:
                return decimal.Decimal(d)
            #case of decimal
            else:
                if 'E' not in d:
                    d_split[1] = d_split[1].rstrip('0')
                    d = d_split[0] + '.' + d_split[1]
                    return decimal.Decimal(d)
                else:
                    return decimal.Decimal(d)
        else:
            return d

class RetrieveReferences(Visitor):
    """This class is used to retrieve all cell references
    It acts as a visitor on a lark object.
    """

    def __init__(self, sheet_instance):
        """Initializes class."""
        self.references = []
        self.sheet_instance = sheet_instance
        self.error_occurred = False

    def cell(self, args):
        """this get the cell references"""
        args = args.children

        # getting the appropriate sheet name and cell location
        if len(args) == 1:      # if using the current sheet
            sheet_name = self.sheet_instance.sheet_name
            cell_location = args[0].value
        elif len(args) == 2:    # if using a different sheet
            # in case of quotes around sheet name
            if args[0][0] == "'" and args[0][-1] == "'":
                sheet_name = args[0][1:-1]
            elif not args[0][0] == "'" and not args[0][-1] == "'":
                sheet_name = args[0]
            else:
                self.error_occurred = True
                sheet_name = ''
            cell_location = args[1].value
        else:
            self.error_occurred = True
            sheet_name = ''
            cell_location = ''

        self.references.append(str(sheet_name) + '!' + str(cell_location))
