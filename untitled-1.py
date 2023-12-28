import tkinter as tk
import Nictk as Ntk
from Nictk.constants import *


# T H I S   W O R K S ! ! ! 

#class ScrollFrame(tk.Frame):
    #def __init__(self, parent, x, y, w, h):
        #super().__init__(parent)
        #self.place(x=x, y=y, width=w, height=h)
        #self.config(background="#D000D0")
        #self._canvas = tk.Canvas(self)
        #self._canvas.config(background="#00D0D0")
        #self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #self._scb = tk.Scrollbar(self, orient=VERTICAL, command=self._canvas.yview)
        #self._canvas.config(yscrollcommand=self._scb.set)
        #self._canvas.bind(
            #'<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox(tk.ALL)))       
        #self._scb.pack(side=tk.RIGHT, fill=tk.Y)
        #self._int_frame = tk.Frame(self._canvas)
        #self._int_window = self._canvas.create_window((10, 0), window=self._int_frame, anchor=tk.N)
        #self._int_frame.config(background="#D0D000")



#winMain = Ntk.Main(100, 100, 800, 600)
#vfr1 = ScrollFrame(winMain, 10, 10, 600, 500)
## an example grid with some data
#for y in range(50):
    #for x in range(8):
        #tk.Label(vfr1._int_frame, text=f'{y}:{x}', borderwidth=1, relief=tk.SOLID, width=10).grid(column=x, row=y)

#tk.mainloop()


class ScrollFrame(tk.Frame):
    def __init__(self, parent, x, y, w, h):
        super().__init__(parent)
        self.place(x=x, y=y, width=w, height=h)
        self.config(background="#D000D0")
        self._canvas = Ntk.Canvas(self, 0, 0, FILL, FILL)
        self._canvas.config(background="#00D0D0", borderwidth=0)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self._scb = tk.Scrollbar(self, orient=VERTICAL, command=self._canvas.yview)
        self._canvas.config(yscrollcommand=self._scb.set)
             
        self._scb.pack(side=tk.RIGHT, fill=tk.Y)
        self._int_frame = tk.Frame(self._canvas)
        self._int_window = self._canvas.create_window((10, 0), window=self._int_frame, anchor=tk.N)
        self._int_frame.config(background="#D0D000")
        self._int_frame.bind(
            '<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox(tk.ALL)))         



winMain = Ntk.Main(100, 100, 800, 600)
vfr1 = ScrollFrame(winMain, 10, 10, 600, 500)
# an example grid with some data
vfr1._int_frame.config(width=300, height=800) 
for y in range(30):
#for x in range(8):
        #tk.Label(vfr1._int_frame, text=f'{y}:{x}', borderwidth=1, relief=tk.SOLID, width=10).grid(column=x, row=y)
    
      
    lab = tk.Label(vfr1._int_frame, text=f'{y}', borderwidth=1, relief=tk.SOLID, width=30, height=30).place(x=20, y=10 + 40 * y)
        
        


tk.mainloop()