from events import *
from Tkinter import *

class ValidatingEntry(Entry): # base class for validating entry widgets
    def __init__(self, master,value="", row=None, column=None, **kw):
        apply(Entry.__init__, (self, master), kw)
        self.master = master
        self.__value = value
        self.__variable = StringVar()
        self.row = row
        self.column = column
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        self.validate()
        pass

    def change(self, event):
        self.focus_set()
        self.__value = str(find_in_grid(self.master, self.row, self.column).get())
        #self.value = find_in_grid(root, i+1, j).get()
        print "clicked at", self.row, self.column+1

    def checkChange(self, event):
        if str(find_in_grid(self.master, self.row, self.column).get()) != str(self.__value):
            self.config(bg="yellow")
        else:
            self.config(bg="white")
        self.validate()

    def validate(self):
        # override: return value, new value, or None if invalid
        return value

class IntegerEntry(ValidatingEntry): #Entry to check if entry cell data is integer
    def validate(self):
        self.__value = str(find_in_grid(self.master, self.row, self.column).get())
        try:
            if self.__value:
                v = int(self.__value)
            return self.__value
        except ValueError:
            self.config(bg="red")
            return None

# class FloatEntry(ValidatingEntry):#Entry to check if entry cell data is float

#     def validate(self, value):
#         try:
#             if value:
#                 v = float(value)
#             return value
#         except ValueError:
#             return None

# class MaxLengthEntry(ValidatingEntry): #Entry to check if entry cell data is less than n number of characters

#     def __init__(self, master, value="", maxlength=None, **kw):
#         self.maxlength = maxlength
#         apply(ValidatingEntry.__init__, (self,  master, value), kw)

#     def validate(self, value):
#         if self.maxlength is None or len(value) <= self.maxlength:
#             return value
#         return None # new value too long
