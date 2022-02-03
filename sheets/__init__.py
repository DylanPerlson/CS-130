# __init__.py

from .workbook import Workbook
from .cell_error import *

__all__ = ['Workbook', 'CellError', 'CellErrorType']

version = '1.1.0'