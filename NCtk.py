from tkinter import *

['bd', 'borderwidth', 'class', 'menu', 'relief', 'screen', 'use', 'background', 'bg', 'colormap', 'container', 'cursor', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx', 'pady', 'takefocus', 'visual', 'width']


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
            w = round((parent.winfo_width() - padx) * int(w[:-1]) / 100)
        else:
            raise TypeError
    if isinstance(h, str):
        if h == "fill":
            h = parent.winfo_height() - y - 2 * pady
        elif h.endswith("%"):
            h = round((parent.winfo_height() - pady) * int(h[:-1]) / 100)
        else:
            raise TypeError    
    return x, y, w, h
            
# To get a widget property use w.cget("name")       name as string, always returns a string
# To set a widget property use w.config(name=val)


#####################################################################
###############****    M A I N   W I N D O W
#####################################################################

class NCtkWindow(Tk):
    def __init__(self, x, y, w, h, title=""):
        Tk.__init__(self)
        self.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        self.resizable(width=FALSE, height=FALSE)
        if len(title):
            self.title(title)
            
    def config_all(self, widget=None, **kw):
        prefix = "*" + widget[4:] + "." if widget else "*"
        for k, v in kw.items():
            self.option_add(prefix + k, v)    


#####################################################################
###############    W I D G E T   W R A P P E R
#####################################################################

# Added by me to override tkinter Widget methods

class NCtkWidget(Widget):
    # call to base class ctor done by other classes
    def __init__(self):
        pass
    
    trans_opt =  { "abcolor":"activebackground", "afcolor":"activeforeground",
                   "bcolor":"background", "dfcolor":"disabledforeground",
                   "fcolor":"foreground", "hbcolor":"highlightbackground",
                   "hcolor":"highlightcolor", "hborderwidth":"highlightthickness",
                   "textvar":"textvariable"}    
    
    def hide(self):
        if self.extFrame.winfo_ismapped():
            self.extFrame.place_forget()
    
    def show(self):
        if not self.extFrame.winfo_ismapped(): 
            self.extFrame.place(x=self.extFrame.winfo_x(), y=self.extFrame.winfo_y())
            
    def visible(self):
        return self.extFrame.winfo_ismapped()
        
    def settext(self, t):
        self.config(text=t)
    
    def gettext(self):
        return self.cget("text")
    
    def config(self, cnf=None, **kw):
        trans_kw = {}
        for k, v in kw.items():
            if k in NCtkWidget.trans_opt:
                trans_kw[NCtkWidget.trans_opt[k]] = v
            else:
                trans_kw[k] = v
        return self._configure('configure', cnf, trans_kw)
        
    

#####################################################################
#######################     F R A M E S
#####################################################################

class NCtkHorFrame(Frame, NCtkWidget):
    def __init__(self, parent, x, y, w, h, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
 
 
class NCtkVerFrame(Frame, NCtkWidget):
    def __init__(self, parent, x, y, w, h, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        

#####################################################################
############       tkinter WIDGETS SUPERCLASSES
#####################################################################

# We must enclose all widgets in an external Frame to obtain their width and
# height in pixels, because otherwise the silly Tk would assume them in
# characters        

class NCtkButton(Button, NCtkWidget):
    """Button widget

    STANDARD OPTIONS

        activebackground, activeforeground, anchor,
        background, bitmap, borderwidth, cursor,
        disabledforeground, font, foreground
        highlightbackground, highlightcolor,
        highlightthickness, image, justify,
        padx, pady, relief, repeatdelay,
        repeatinterval, takefocus, text,
        textvariable, underline, wraplength

    WIDGET-SPECIFIC OPTIONS

        command, compound, default, height,
        overrelief, state, width
    """    
    def __init__(self, parent, x, y, w, h, content=None, command=None, padx=0, pady=0):
        NCtkWidget.__init__(self)
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        self.extFrame = Frame(parent, width=w, height=h)
        self.extFrame.place(x=x, y=y)
        self.extFrame.pack_propagate(False)
        Button.__init__(self, self.extFrame, text="Button")
        self.pack(fill=BOTH, expand=True)
        #self.config(anchor=W, wraplength=w,justify=LEFT)
        if isinstance(content, str):
            self.config(text=content)
        elif isinstance(content, StringVar):
            self.config(textvariable=content)
        elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            self.config(image=content)
        if command:
            self.bind("<Button-1>", command)


class NCTkCanvas(Canvas):
    """Canvas widget to display graphical elements like lines or text.

    Valid resource names: background, bd, bg, borderwidth, closeenough,
    confine, cursor, height, highlightbackground, highlightcolor,
    highlightthickness, insertbackground, insertborderwidth,
    insertofftime, insertontime, insertwidth, offset, relief,
    scrollregion, selectbackground, selectborderwidth, selectforeground,
    state, takefocus, width, xscrollcommand, xscrollincrement,
    yscrollcommand, yscrollincrement.
    """    
    def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
        pass

class NCtkCheckbutton(Checkbutton):
    """Checkbutton widget which is either in on- or off-state.

    Valid resource names: activebackground, activeforeground, anchor,
    background, bd, bg, bitmap, borderwidth, command, cursor,
    disabledforeground, fg, font, foreground, height,
    highlightbackground, highlightcolor, highlightthickness, image,
    indicatoron, justify, offvalue, onvalue, padx, pady, relief,
    selectcolor, selectimage, state, takefocus, text, textvariable,
    underline, variable, width, wraplength."""    
    #def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
    
    def __init__(self, parent, x, y, w, h, content=None, command=None, padx=0, pady=0):
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        self.extFrame = Frame(parent, width=w, height=h)
        self.extFrame.place(x=x, y=y)
        self.extFrame.pack_propagate(False)
        Checkbutton.__init__(self, self.extFrame, text="Button")
        self.pack(fill=BOTH, expand=True)
        self.config(anchor=N, wraplength=w,justify=LEFT)
        #if isinstance(content, str):
            #self.config(text=content)
        #elif isinstance(content, StringVar):
            #self.config(textvariable=content)
        #elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            #self.config(image=content)
        #if command:
            #self.bind("<Button-1>", command)    
        ##Checkbutton.__init__(self, master=None, cnf={}, **kw):


class NCtkEntry(Entry, NCtkWidget):
    """Entry widget which allows displaying simple text.
    
    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand."""    
    def __init__(self, parent, x, y, w, h, content=None, command=None, padx=0, pady=0):
        NCtkWidget.__init__(self)
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        self.extFrame = Frame(parent, width=w, height=h)
        self.extFrame.place(x=x, y=y)
        Entry.__init__(self, self.extFrame, text="Entry")
        self.extFrame.pack_propagate(False)
        self.pack(fill=BOTH, expand=1)
        self.config(relief=SUNKEN)
        if content and isinstance(content, StringVar):
            self.intStr = content
        else:
            self.intStr = StringVar()
        if command:
            self.bind("<Return>", command)
        self.config(textvariable=self.intStr)
        
    # overrides NCtkWidget method!
    def gettext(self):
        return self.get()        


# class Frame substituted by NCtkHorFrame, NCtkVerFrame   
    
class NCtkLabel(Label, NCtkWidget):
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
    def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
        NCtkWidget.__init__(self)
        x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
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
        elif isinstance(content, (PhotoImage, BitmapImage)):
            self.config(image=content)
    
    
class NCtkListbox(Listbox):
    """Listbox widget which can display a list of strings.

        Valid resource names: background, bd, bg, borderwidth, cursor,
        exportselection, fg, font, foreground, height, highlightbackground,
        highlightcolor, highlightthickness, relief, selectbackground,
        selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
        width, xscrollcommand, yscrollcommand, listvariable."""
    def __init__(self, master, cnf={}, **kw):
        pass
        
        
class NCtkMenu(Menu):
    """Menu widget which allows displaying menu bars, pull-down menus and pop-up menus.
        
        Valid resource names: activebackground, activeborderwidth,
        activeforeground, background, bd, bg, borderwidth, cursor,
        disabledforeground, fg, font, foreground, postcommand, relief,
        selectcolor, takefocus, tearoff, tearoffcommand, title, type."""
    def __init__(self, parent):
        #x, y, w, h = calc_dimensions(parent, x, y, w, h, padx, pady)
        #self.extFrame = Frame(parent, width=w, height=h)
        #self.extFrame.place(x=x, y=y)
        #self.extFrame.pack_propagate(False)
        Menu.__init__(self, parent, tearoff=0)
        #self.place(x=x, y=y, width=w, height=h)
        #self.pack(fill=BOTH, expand=True)        
    
# MenuButton and Message obsolete in tkinter


class NCtkRadiobutton(Radiobutton):
    """Radiobutton widget which shows only one of several buttons in on-state.

        Valid resource names: activebackground, activeforeground, anchor,
        background, bd, bg, bitmap, borderwidth, command, cursor,
        disabledforeground, fg, font, foreground, height,
        highlightbackground, highlightcolor, highlightthickness, image,
        indicatoron, justify, padx, pady, relief, selectcolor, selectimage,
        state, takefocus, text, textvariable, underline, value, variable,
        width, wraplength."""
    def __init__(self, master, cnf={}, **kw):
        pass


class NCtkScale(Scale):
    """Scale widget which can display a numerical scale.

        Valid resource names: activebackground, background, bigincrement, bd,
        bg, borderwidth, command, cursor, digits, fg, font, foreground, from,
        highlightbackground, highlightcolor, highlightthickness, label,
        length, orient, relief, repeatdelay, repeatinterval, resolution,
        showvalue, sliderlength, sliderrelief, state, takefocus,
        tickinterval, to, troughcolor, variable, width."""
    def __init__(self, master=None, cnf={}, **kw):
        pass


class NCtkScrollbar(Scrollbar):
    """Scrollbar widget which displays a slider at a certain position.

        Valid resource names: activebackground, activerelief,
        background, bd, bg, borderwidth, command, cursor,
        elementborderwidth, highlightbackground,
        highlightcolor, highlightthickness, jump, orient,
        relief, repeatdelay, repeatinterval, takefocus,
        troughcolor, width."""
    def __init__(self, master=None, cnf={}, **kw):
        pass


class NCtkText(Text):
    """Text widget which can display text in various forms.

        STANDARD OPTIONS

            background, borderwidth, cursor,
            exportselection, font, foreground,
            highlightbackground, highlightcolor,
            highlightthickness, insertbackground,
            insertborderwidth, insertofftime,
            insertontime, insertwidth, padx, pady,
            relief, selectbackground,
            selectborderwidth, selectforeground,
            setgrid, takefocus,
            xscrollcommand, yscrollcommand,

        WIDGET-SPECIFIC OPTIONS

            autoseparators, height, maxundo,
            spacing1, spacing2, spacing3,
            state, tabs, undo, width, wrap,

        """
    def __init__(self, master=None, cnf={}, **kw):
        pass
    
    
# Copied widgets from __init__ until Text (line 3172 of __init__)
# I don't know if others are to be modified

