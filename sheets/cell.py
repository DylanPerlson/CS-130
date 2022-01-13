# Object class for individual cell


class Cell:
    def __init__ (self, contents, curr_sheet):
        # Determine Cell Type
        self.contents = contents

        if contents[0] == '=':
            self.type = "FORMULA"
            self.value = get_value_from_contents(contents)
        elif contents[0] == "'":
            self.type = "STRING"
            self.value = str(contents)
        else:
            self.type = "LITERAL"
            self.value = contents


    def get_value_from_contents(self, contents): # assume that contents is '=a1'  '=aa234 + 4 - b1'
        for i in contents:
            if i == '=':
                continue
            elif i == ' ':
                continue
            # elif i ==  "'":
            #     # some string will be
            # elif i.isdigit():
            #     skip all the way to the end until no ore digits
            # elif i == string Char 

            #     a13+
            #     balance!a13+
            #     get every character following it that is a string and a number until there is somethign that isnt a number

        

        # balances!a3