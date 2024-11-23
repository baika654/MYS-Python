class templateAnswerClass:
    
    
    # only simple version needed at the moment; will look to use other versions later
    def __init__(self, cellRefTuple, value):
        self.cellRefTuple = cellRefTuple
        self.value = value


    #def __init__(self, name, sheet, refAddress, value):
    #    self.refAddress = refAddress
    #    self.sheet = sheet
    #    self.value = value
    #    self.name = name
    #    self.cellRefTuple = None

    ## not used at present

    #def __init__(self, cellRefTuple, sheet, value):
    #    self.sheet = sheet
    #    self.value = value
    #    self.cellRefTuple= cellRefTuple
    #    self.name =""
    #    self.columnLetter =""
    #    self.refAddress=""
    #    self.columnLetter = self.colnum_string(self.cellRefTuple[0])
    #    self.refAddress = "${0}${1}".format(self.columnLetter,self.cellRefTuple[1])
        
    
    #def colnum_string(self, n):
    #    string = ""
    #    while n > 0:
    #        n, remainder = divmod(n - 1, 26)
    #        string = chr(65 + remainder) + string
    #    return string

    



