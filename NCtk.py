from tkinter import *


def calc_dimensions(parent, w, h, padx, pady):
    parent.update()
    if isinstance(w, str):
        if w == "fill":
            w = parent.winfo_width() - 2 * padx
        elif w.endswith("%"):
            w = round((parent.winfo_width() - padx) * int(w[:-1]) / 100, 0)
    if isinstance(h, str):
        if h == "fill":
            h = parent.winfo_height() - 2 * pady
        elif h.endswith("%"):
            h = round((parent.winfo_height() - pady) * int(h[:-1]) / 100, 0)
    return w, h
            


class MtkiWindow(Tk):
    def __init__(self, w, h, x=100, y=100, title=""):
        Tk.__init__(self)
        self.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        self.resizable(width=FALSE, height=FALSE)
        if len(title):
            self.title(title)
        self.data = []
        
        

class MtkiLabel(Label):
    def __init__(self, parent, w, h, x=10, y=10, content=None):
        w, h = calc_dimensions(parent, w, h, x, y)
        self.intFrame = Frame(parent, width=w, height=h)
        self.intFrame.place(x=x, y=y)
        Label.__init__(self, self.intFrame, text="Label")
        self.intFrame.pack_propagate(False)
        self.pack(fill=BOTH, expand=1)
        self.config(anchor=W, wraplength=w,justify=LEFT, relief=SUNKEN)
        if isinstance(content, str):
            self.config(text=content)
        elif isinstance(content, StringVar):
            self.config(textvariable=content)
        elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            self.config(image=content)
        self.data = []
        
    def hide(self):
        self.place_forget()
        self.visible = 0
    
    def show(self):
        #x = int(self.intFrame.cget("x"))
        #y = int(self.intFrame.cget("y"))
        self.intFrame.place()
        
    def settext(self, t):
        self.config(text=t)
    
    def gettext(self):
        return self.text
        



class MtkiButton(Button):
    def __init__(self, parent, w, h, x=10, y=10, content=None, command=None):
        w, h = calc_dimensions(parent, w, h, x, y)
        self.intFrame = Frame(parent, width=w, height=h)
        self.intFrame.place(x=x, y=y)
        Button.__init__(self, self.intFrame, text="Button")
        self.intFrame.pack_propagate(False)
        self.pack(fill=BOTH, expand=1)
        
        
        #self.config(anchor=W, wraplength=w,justify=LEFT)
        if isinstance(content, str):
            self.config(text=content)
        elif isinstance(content, StringVar):
            self.config(textvariable=content)
        elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            self.config(image=content)
        if command:
            self.bind("<Button-1>", command)
        self.data = []

class MtkiEntry(Entry):
    def __init__(self, parent, w, h, x=10, y=10, content=None, command=None):
        self.intFrame = Frame(parent, width=w, height=h)
        self.intFrame.place(x=x, y=y)
        Entry.__init__(self, self.intFrame, text="Entry")
        self.intFrame.pack_propagate(False)
        self.pack(fill=BOTH, expand=1)
        self.config(relief=SUNKEN)
        if content and isinstance(content, StringVar):
            self.intStr = content
        else:
            self.intStr = StringVar()
        if command:
            self.bind("<Return>", command)
        self.config(textvariable=self.intStr)
        self.data = []

    def hide(self):
        self.place_forget()
        self.visible = 0
    
    def show(self):
        #x = int(self.intFrame.cget("x"))
        #y = int(self.intFrame.cget("y"))
        self.intFrame.place()
        
    def settext(self, t):
        self.config(text=t)
    
    def gettext(self):
        return self.get()
    