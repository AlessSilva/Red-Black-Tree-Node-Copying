class Node:

    def __init__(self, value):
         
        self.value  = value
        self.red  = True
        self.parent = None
        self.child0  = None
        self.child1 = None 
        self.copy_ = None
        self.change = {"value":None, "field":None, "T":-1}
        self.T = None