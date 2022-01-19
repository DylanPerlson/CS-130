# Object class for individual cell

from asyncio.windows_events import NULL
from collections import defaultdict
import lark
from .sheet import Sheet
from cell_error import CellErrorType, CellError

class Cell:
    def __init__ (self, contents, curr_sheet):
        # Determine Cell Type
        self.contents = contents
        if contents[0] == '=':
            self.type = "FORMULA"
            parser = lark.Lark.open('sheets/formulas.lark', start='formula')
            self.formula = parser.parse(self.contents).pretty()
            self.value = self.get_value_from_contents(contents)
        elif contents[0] == "'":
            self.type = "STRING"
            self.value = str(contents)
        else:
            self.type = None
            self.value = None
        self.parent_sheet = curr_sheet
    
    def check_errors(self):
        #Check for Parse Error
        if self.formula == NULL:
            self.value = CellError(CellErrorType.PARSE_ERROR, "Formula could not be parsed", "None")
        
        #Check for Circular Reference Error
        # need to be able to pass cell location in cell here, this is temporary for logic purposes
        # Easiest way, track its references/dependencies in a list parameter
        # Strongly connected components algorithm to check 
        # Node like structure with directed edges 
        # Store a graph somewhere 
        if ('A2') in self.contents:
            self.value = CellError(CellErrorType.CIRCULAR_REFERENCE, "Circular reference to same cell in formula", "None")

    def get_value_from_contents(self, contents):
        #Throw parse error if formula can't be translated via lark
        if self.formula == NULL:
            self.value = CellError(CellErrorType.PARSE_ERROR, "Formula could not be parsed", "None")
            return
        
        #Parsing formula and pushing operations onto stack inside out
        return