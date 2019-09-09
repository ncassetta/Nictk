from tkinter import *


def calc_dimensions(parent, x, y, w, h, padx, pady):
    parent.update()
    last_w = parent.winfo_children()[-1] if parent.winfo_children() else None
    if isinstance(parent, NCtkHorFrame) and last_w:
        last_x, last_y = last_w.winfo_x() + last_w.winfo_width(), 0
    elif isinstance(parent, (NCtkVerFrame, NCtkWindow)) and last_w:
        last_x, last_y = 0, last_w.winfo_y() + last_w.winfo_height()
    else:
        last_x, last_y = 0, 0
    if isinstance(x, str):
        if x == "pack":
            x = last_x
        elif x.endswith("%"):
            x = round((parent.winfo_width() - padx) * int(x[:-1]) / 100)
        else:
            raise TypeError
    if isinstance(y, str):
        if y == "pack":
            y = last_y
        elif y.endswith("%"):
            y = round((parent.winfo_height() - pady) * int(y[:-1]) / 100)
        else:
            raise TypeError    
    if isinstance(w, str):
        if w == "fill":
            w = parent.winfo_width() - x - 2 * padx
        elif w.endswith("%"):
            w = round((parent.winfo_width() - last_x - padx) * int(w[:-1]) / 100)
        else:
            raise TypeError
    if isinstance(h, str):
        if h == "fill":
            h = parent.winfo_height() - y - 2 * pady
        elif h.endswith("%"):
            h = round((parent.winfo_height() - last_y - pady) * int(h[:-1]) / 100)
        else:
            raise TypeError    
    return x, y, w, h
            


class NCtkWindow(Tk):
    def __init__(self, x, y, w, h, title=""):
        Tk.__init__(self)
        self.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        self.resizable(width=FALSE, height=FALSE)
        if len(title):
            self.title(title)
        self.data = []
        

class NCtkHorFrame(Frame):
    def __init__(self, parent, x, y, w, h, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        self.configure(relief=SUNKEN)
        

class NCtkVerFrame(Frame):
    def __init__(self, parent, x, y, w, h, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        self.configure(relief=SUNKEN)
        
        
        

class NCtkLabel(Label):
    def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        # we need an external Frame to obtain the w, h in pixels, because
        # the silly Tk assumes them in characters
        self.extFrame = Frame(parent, width=w, height=h)
        self.extFrame.place(x=x, y=y)
        self.extFrame.pack_propagate(False)
        Label.__init__(self, self.extFrame, text="Label")
        self.pack(fill=BOTH, expand=True)
        self.config(anchor=W, wraplength=w,justify=LEFT, relief=SUNKEN)
        if isinstance(content, str):
            self.config(text=content)
        elif isinstance(content, StringVar):
            self.config(textvariable=content)
        elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            self.config(image=content)
        
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
        



class NCtkButton(Button):
    def __init__(self, parent, x, y, w, h, content=None, command=None, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        Button.__init__(self, parent, width=w, height=h, text="Button")
        self.place(x=x, y=y)
                
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


class NCtkEntry(Entry):
    def __init__(self, parent, x, y, w, h, content=None, command=None, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
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
    