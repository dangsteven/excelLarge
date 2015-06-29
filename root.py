import Tkinter as tk
from validation import *
import random
import events
from dataRetriever import connectOracle

class Widgy(tk.Frame):
    def __init__(self, root, data):
        # initializes the canvas and variables
        tk.Frame.__init__(self, root)
        self.data = data
        self.height = len(self.data)
        self.width = len(self.data[1])
        self.canvas = tk.Canvas(root, borderwidth=0, width=850, height=500, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        # Initializes the vertical and horizontal scroll bars.
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.frame.bind("<Configure>", self.OnFrameConfigure)


        # Initializes the top labels for each column
        tk.Label(self.frame, text="REGION").grid(row=0, column=0, sticky=W)
        tk.Label(self.frame, text="GOVAGG").grid(row=0, column=1, sticky=W)
        tk.Label(self.frame, text="STATUS").grid(row=0, column=2, sticky=W)
        tk.Label(self.frame, text="ID").grid(row=0, column=3, sticky=W)
        tk.Label(self.frame, text="Number").grid(row=0, column=4, sticky=W)
        self.populate()

    # Populates data on behalf of the data taken from the sql query
    def populate(self):
        '''Put in some fake data'''
        for i in range(1,self.height+1): #Rows
            for j in range(self.width): #Columns
                rand = random.randrange(1,9999)
                cell = IntegerEntry(self.frame, value=str(self.data[i-1][j]), row=i, column=j)
                #cell = IntegerEntry(self.frame, value=str(rand), row=i, column=j)
                cell.grid(row=i, column=j)
                cell.bind("<FocusIn>", cell.change)
                cell.bind("<FocusOut>", cell.checkChange)
        excelise = Button(self.frame, text="Excelise!", command=lambda:events.writeToExcel(self.frame, self.height, self.width)).grid(row=1, column=self.width+1)
        xmlise = Button(self.frame, text="XMLise!", command=lambda:events.writeToXML(self.frame, self.height, self.width)).grid(row=2, column=self.width+1)
        validate = Button(self.frame, text="Validate", command=self.validateGrid).grid(row=3, column=self.width+1)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units")

    # Makes sure that each cell is of the correct data type.
    def validateGrid(self):
        for i in range(1,self.height+1): #Rows
            for j in range(self.width): #Columns
                find_in_grid(self.frame, i, j).validate()

if __name__ == "__main__":
    query = connectOracle()
    root=tk.Tk()
    Widgy(root, query).pack(side="top", fill="both", expand=True)
    root.mainloop()
