import lark
import os; os.system('clear')


contents = '=INDIRECT(B1 & "!A2:c4")'
parser = lark.Lark.open('sheets/formulas.lark', start='formula')
parsed_contents = parser.parse(contents)

print(parsed_contents.pretty())