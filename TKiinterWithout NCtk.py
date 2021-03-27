import tkinter as tk


def entrycallback(event):
    s = labTest.cget("text")
    s += entTest.get()
    labTest.config(text=s)


class SampleMain(tk.Tk):
    def __init__(self, x, y, w, h, title=""):
        tk.Tk.__init__(self)
        self.geometry("{}x{}+{}+{}".format(w, h, x, y))
        #self.bind("<Configure>", self._resize_children) 
        #self.resizable(width=FALSE, height=FALSE)
        self.title(title)
        
        
class SampleEntry(tk.Entry):
    """Entry widget which allows displaying simple text.
    
    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand."""
    
    
    def trace_callback(self, a, b, c):
        self.event_generate("<<CHANGEDVAR>>")
        
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        #x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        #self._extFrame = tk.Frame(parent, width=w, height=h)
        #self._extFrame.config(background=parent.cget("background"))
        tk.Entry.__init__(self, parent)
        self.place(x=x, y=y, width=w, height=h,)
        #if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            #parent.get_active().children.append(self._extFrame)
        self.config(relief="sunken")
        #self._get_parent_config()
        self.intStr = tk.StringVar(name="var_"+self._name)
        if content:
            self.intStr.set(str(content))
        #self.intStr.trace("w", self.trace_callback)
        self.config(textvariable=self.intStr)
        if command:
            self.bind("<Return>", command)
            

class SampleLabel(tk.Label):
    """Label widget which can display text and bitmaps.

       STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground,
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, takefocus, text,
            textvariable, underline, wraplength

       WIDGET-SPECIFIC OPTIONS

            height, state, width

        """    
    def __init__(self, parent, x, y, w, h, pad=0, content=None):
        #x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        #self._extFrame = tk.Frame(parent, width=w, height=h)
        #self._extFrame.config(background=parent.cget("background"))
        tk.Label.__init__(self, parent)
        self.place(x=x, y=y, width=w, height=h)
        #if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            #parent.get_active().children.append(self._extFrame)
        self.config(anchor="w", justify="left", relief="sunken", wraplength=w-1)
        #self._get_parent_config()
        #self.setcontent(content)
        self.config(text=content)

winMain = SampleMain(100, 100, 400, 300, "prova")
labTest = SampleLabel(winMain, 20, 20, 150, 30, content="Label")
entTest = SampleEntry(winMain, 180, 20, 150, 30, command=entrycallback)


tk.mainloop()

