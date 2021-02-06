from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *

['bd', 'borderwidth', 'class', 'menu', 'relief', 'screen', 'use', 'background', 'bg', 'colormap', 'container', 'cursor', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx', 'pady', 'takefocus', 'visual', 'width']


            
# To get a widget property use w.cget("name")       name as string, always returns a string
# To set a widget property use w.config(name=val)


#####################################################################
###################    M A I N   W I N D O W
#####################################################################

class NCtkWindow(Tk):
    def __init__(self, x, y, w, h, title=""):
        Tk.__init__(self)
        self.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        #self.resizable(width=FALSE, height=FALSE)
        self.bind("<Configure>", self._resize_childs)
        if len(title):
            self.title(title)
            
    #TODO: implement the NCtkMisc class, which contains config, getwinfo, ecc
    # (common between windows and widget)
            
    def config_all(self, widget=None, **kw):
        prefix = "*" + widget[4:] + "." if widget else "*"
        for k, v in kw.items():
            self.option_add(prefix + k, v)
    
    def getwinfo(self, key, *kw):
        function = "winfo_" + key
        return getattr(Widget, function)(self, *kw)
    
    resizeflag = True
    
    def _resize_childs(self, event):
        if NCtkWindow.resizeflag:
            print("_resize_child() called on NCtkWindow")
            print("Window dimensions:", self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height())
            for w in self.winfo_children():
                if hasattr(w, "_update_dimensions"):
                    w._update_dimensions()
                else:
                    for w1 in w.winfo_children():
                        w1._update_dimensions()
                    
class NCtkToplevel(Toplevel):
    def __init__(self, parent, x, y, w, h, title="", modal=False):
        Toplevel.__init__(self, master=parent)
        xp = parent.winfo_x()
        yp = parent.winfo_y()
        self.geometry(str(w) + "x" + str(h) + "+" + str(x+xp) + "+" + str(y+yp))
        self.title(title)
        if modal:
            focus_set()
            grab_set()
            transient(parent)            


#####################################################################
###############    W I D G E T   W R A P P E R
#####################################################################

# Added by me to override tkinter Widget methods

_trans_opt =  { "abcolor":"activebackground", "afcolor":"activeforeground",
                "bcolor":"background", "dfcolor":"disabledforeground",
                "fcolor":"foreground", "hbcolor":"highlightbackground",
                "hcolor":"highlightcolor", "hborderwidth":"highlightthickness",
                "sbcolor":"selectbackground", "sfcolor":"selectforeground",
                "textvar":"textvariable"}    

class NCtkWidget(Widget):
    # call to base class ctor done by other classes
    def __init__(self, x, y, w, h, pad=0):
        self._orig_dim = (x, y, w, h, pad)
        #self.event_add("<<CHANGEDVAR>>")
    
    def hide(self):
        """Hides the widget. The widget will not be displayed, but its data remain managed; use show()
        to newly display the widget. if the widget was already hidden does nothing."""
        if self._extFrame.winfo_ismapped():
            self._extFrame.place_forget()
    
    def show(self):
        """Shows a previously hidden widget. If the widget was already shown does nothing."""        
        if not self._extFrame.winfo_ismapped(): 
            self._extFrame.place(x=self._extFrame.winfo_x(), y=self._extFrame.winfo_y())
            
    def visible(self):
        """Returns True if the widget is visible."""
        return self._extFrame.winfo_ismapped()
        
    def setcontent(self, content):
        if isinstance(content, str):
            self.config(text=content, textvariable=None, image="")
        elif isinstance(content, StringVar):
            self.config(text=content, textvariable=content, image='')
        elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            self.config(text='', textvariable=None, image=content)        
    
    def gettext(self):
        return self.cget("text")
    
    def config(self, cnf=None, **kw):
        trans_kw = {}
        for k, v in kw.items():
            if k in _trans_opt:
                newk = _trans_opt[k]
                trans_kw[newk] = v
            else:
                newk = k
                trans_kw[newk] = v
            # TODO: what other options must be config for the _extFrame???
            #if k == "bcolor" and hasattr(self, "_extFrame"):
            #    self._extFrame.config({newk:v})
        
        return self._configure('configure', cnf, trans_kw)
    
    def getconfig(self, key):
        if key in _trans_opt:
            key = _trans_opt[key]
        return self.cget(key)
    
    def getwinfo(self, key, *kw):
        if key == "parent" and hasattr(self, "_extFrame"):
                return self._extFrame.winfo_parent()
        function = "winfo_" + key
        return getattr(Widget, function)(self, *kw)
    
    def _calc_dimensions(self, parent, x, y, w, h, pad):
        #TODO: implement "rpack"
        NCtkWindow.resizeflag = False
        parent.update()
        NCtkWindow.resizeflag = True
        if not pad:
            padx, pady = (0, 0), (0, 0)
        elif not isinstance(pad, (list, tuple)):
            padx, pady = (pad, pad), (pad, pad)
        elif len(pad) == 2:
            padx, pady = (pad[0], pad[0]), (pad[1], pad[1])
        elif len(pad) == 4:
            padx, pady = (pad[0], pad[1]), (pad[2], pad[3])
        brothers = parent.winfo_children()
        self_t = self._extFrame if hasattr(self, "_extFrame") else self
        if self_t in brothers:              # we are resizing an already placed widget
            last_w = brothers[brothers.index(self_t) - 1] if brothers.index(self_t) > 0 else None
        else:                               # we are placing a new widget
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
            elif x == "center":
                tempw = w
                if isinstance(tempw, str):
                    if tempw == "fill":
                        raise
                    elif tempw.endswith("%"):
                        tempw = round(parent.winfo_width() * int(tempw[:-1]) / 100)
                    else:
                        raise TypeError
                x = round((parent.winfo_width() - tempw) / 2)
            elif x.endswith("%"):
                x = round(parent.winfo_width() * int(x[:-1]) / 100)
            else:
                raise TypeError
        if isinstance(y, str):
            if y == "pack":
                y = last_y
            elif y == "center":
                temph = h
                if isinstance(temph, str):
                    if temph == "fill":
                        raise
                    elif temph.endswith("%"):
                        temph = round(parent.winfo_height() * int(temph[:-1]) / 100)
                    else:
                        raise TypeError
                y = round((parent.winfo_height() - temph) / 2)            
            elif y.endswith("%"):
                y = round(parent.winfo_height() * int(y[:-1]) / 100)
            else:
                raise TypeError    
        if isinstance(w, str):
            if w == "fill":
                w = parent.winfo_width() - x
            elif w.endswith("%"):
                w = round(parent.winfo_width() * int(w[:-1]) / 100)
            else:
                raise TypeError
        elif w < 0:
            w = parent.winfo_width() - x + w
            if w < 0:
                raise ValueError
        if isinstance(h, str):
            if h == "fill":
                h = parent.winfo_height() - y
            elif h.endswith("%"):
                h = round(parent.winfo_height() * int(h[:-1]) / 100)
            else:
                raise TypeError
        elif h < 0:
            h = parent.winfo_height() - y + h
            if h < 0:
                raise ValueError        
        return x, y, w, h, padx, pady
    
    def _place_widget(self, x, y, w, h, padx, pady):
        self._extFrame.config(width=w, height=h)
        self._extFrame.place_forget()
        self._extFrame.place(x=x, y=y)
        self._extFrame.pack_propagate(False)
        self.pack(padx=padx, pady=pady, fill=BOTH, expand=True)
        
    def _update_dimensions(self):
        print("_update_dimensions called on", self.winfo_name())
        x, y, w, h, pad = self._orig_dim
        parent = self._nametowidget(self.getwinfo("parent"))         
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        if isinstance(self, (NCtkHorFrame, NCtkVerFrame)):
            self.place_forget()
            self.config(width=w, height=h)
            self.place(x=x, y=y)
        else:
            self._place_widget(x, y, w, h, padx, pady)
        if isinstance(self, (NCtkLabel, NCtkCheckbutton, NCtkRadiobutton)):
            self.config(wraplength=self._calc_wrap(self) - 20)    ### FIX IT!!! AS IN NCtkLabel
        for w in self.winfo_children():
            if hasattr(w, "_update_dimensions"):
                w._update_dimensions()
            else:
                for w1 in w.winfo_children():
                    if isinstance(w1, Scrollbar):
                        w.config(yscrollcommand=w1.set)
                        w1.config(command=w.yview)                        
                    if hasattr(w1, "_update_dimensions"):       ### Otherwise error with Scrollbar
                        w1._update_dimensions()
            

#####################################################################
#######################     F R A M E S
#####################################################################

class NCtkHorFrame(Frame, NCtkWidget):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        self.config(background=parent.cget("background"))
 
 
class NCtkVerFrame(Frame, NCtkWidget):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        self.config(background=parent.cget("background"))
        

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
    def __init__(self, parent, x, y, w, h, content=None, command=None, pad=None):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        Button.__init__(self, self._extFrame, text="Button")
        self._place_widget(x, y, w, h, padx, pady)
        #self.config(anchor=W, wraplength=w,justify=LEFT)
        self.setcontent(content)
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


class NCtkCheckbutton(Checkbutton, NCtkWidget):
    """Checkbutton widget which is either in on- or off-state.

    Valid resource names: activebackground, activeforeground, anchor,
    background, bd, bg, bitmap, borderwidth, command, cursor,
    disabledforeground, fg, font, foreground, height,
    highlightbackground, highlightcolor, highlightthickness, image,
    indicatoron, justify, offvalue, onvalue, padx, pady, relief,
    selectcolor, selectimage, state, takefocus, text, textvariable,
    underline, variable, width, wraplength."""    
    #def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
    
    def __init__(self, parent, x, y, w, h, content=None, command=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))        
        Checkbutton.__init__(self, self._extFrame, text="")
        self._place_widget(x, y, w, h, padx, pady)
        self._calc_wrap = lambda self: self.winfo_width() - 20  # Used to calculate text wraplength when resized
        self.config(anchor=W, justify=LEFT)
        self.setcontent(content)
        if command:
            self.bind("<Button-1>", command)
            
    def setvariable(self, variable=None, offvalue=None, onvalue=None):
        if variable:
            self.config(variable=variable)
        if offvalue:
            self.config(offvalue=offvalue)
        if onvalue:
            self.config(onvalue=onvalue)
            

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
    
    def trace_text(self, *args):
        self.event_generate("<<CHANGEDVAR>>")
        
    def __init__(self, parent, x, y, w, h, content=None, command=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        Entry.__init__(self, self._extFrame, text="Entry")
        self._place_widget(x, y, w, h, padx, pady)
        self.config(relief=SUNKEN)
        self.intStr = StringVar()
        if content:
            self.intStr.set(str(content))
        self.intStr.trace("w", self.trace_text)
        self.config(textvariable=self.intStr)
        if command:
            self.bind("<Return>", command)
        
    # overrides NCtkWidget methods!
    def setcontent(self, content):
        self.intStr.set(str(content))
        
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
    def __init__(self, parent, x, y, w, h, content=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        Label.__init__(self, self._extFrame, text="Label")
        self._place_widget(x, y, w, h, padx, pady)
        self._calc_wrap = lambda self: self.winfo_width() - 1  # Used to calculate text wraplength when resized
        self.config(anchor=W, justify=LEFT, relief=SUNKEN)
        self.setcontent(content)
        
    
class NCtkListbox(Listbox, NCtkWidget):
    """Listbox widget which can display a list of strings.

        Valid resource names: background, bd, bg, borderwidth, cursor,
        exportselection, fg, font, foreground, height, highlightbackground,
        highlightcolor, highlightthickness, relief, selectbackground,
        selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
        width, xscrollcommand, yscrollcommand, listvariable."""
    # and activestyle ???
    def __init__(self, parent, x, y, w, h, command=None, items=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        Listbox.__init__(self, self._extFrame)
        self._place_widget(x, y, w, x, padx, pady)
        self.config(justify=LEFT, relief=SUNKEN, activestyle="none")
        self.vscroll = Scrollbar(self._extFrame, orient=VERTICAL)
        self.config(yscrollcommand=self.vscroll.set)
        self.vscroll.config(command=self.yview)
        if command:
            self.bind("<<ListboxSelect>>", command)
        if items:
            for i in items:
                self.insert(END, i)
            
    def insert(self, index, *elements):
        self.update()
        Listbox.insert(self, index, *elements)
        offs, size = self.yview()
        if size - offs < 1.0:
            if not self.vscroll.winfo_ismapped():
                self.pack_forget()
                self.vscroll.pack(side=RIGHT, fill=Y)
                self.pack(side=LEFT, fill=BOTH, expand=True)                
            self.see(index)
            
    def delete(self, first, last=None):
        Listbox.delete(self, first, last=None)
        offs, size = self.yview()
        if size - offs == 1.0:        
            if self.vscroll.winfo_ismapped():
                self.vscroll.pack_forget()
                self.pack(fill=BOTH, expand=True)
                
    def getselected(self):
        if self.curselection() == "":
            return ()
        else:
            return self.curselection()


# Used by NCtkMenu
class _setitMenu:
    """Internal class. It wraps the command in the widget Menu."""
    def __init__(self, value, callback=None):
        self.__value = value
        self.__callback = callback
    def __call__(self, *args):
        if self.__callback:
            self.__callback(self.__value, *args)
            #self.__callback(*args)     
        
class NCtkMenu(Menu):
    """Menu widget which allows displaying menu bars, pull-down menus and pop-up menus.
        
        Valid resource names: activebackground, activeborderwidth,
        activeforeground, background, bd, bg, borderwidth, cursor,
        disabledforeground, fg, font, foreground, postcommand, relief,
        selectcolor, takefocus, tearoff, tearoffcommand, title, type."""
    def __init__(self, parent):
        Menu.__init__(self, parent, tearoff=0)
        
    # These override the Menu methods to have callbacks with the
    # item name as parameter
    def add(self, itemType, cnf={}, **kw):
        if "command" in cnf.keys():
            if "arg" in cnf.keys():
                cmd = _setitMenu(cnf["arg"], cnf["command"])
                cnf.pop("arg")
            else:
                cmd = _setitMenu(cnf["label"], cnf["command"])
            cnf.update({"command":cmd})
        self.tk.call((self._w, 'add', itemType) +
                 self._options(cnf, kw))     
    def insert(self, index, itemType, cnf={}, **kw):
        if "command" in cnf.keys():
            cmd = _setitMenu(cnf["label"], cnf["command"])
            cnf.update({"command":cmd})        
        self.tk.call((self._w, 'insert', index, itemType) +
                 self._options(cnf, kw))
    def entrycget(self, index, option):
        """Return the resource value of a menu item for OPTION at INDEX."""
        if option in _trans_opt:
            option = _trans_opt["option"]
        return self.tk.call(self._w, 'entrycget', index, '-' + option)
    entrygetconfig = entrycget
    def entryconfigure(self, index, cnf=None, **kw):
        """Configure a menu item at INDEX."""
        trans_kw = {}
        if isinstance(cnf, dict):
            for k, v in cnf.items():
                if k in _trans_opt:
                    trans_kw[_trans_opt[k]] = v
                else:
                    trans_kw[k] = v        
        for k, v in kw.items():
            if k in _trans_opt:
                trans_kw[_trans_opt[k]] = v
            else:
                trans_kw[k] = v        
        return self._configure(('entryconfigure', index), trans_kw, {})
    entryconfig = entryconfigure
    
# MenuButton and Message obsolete in tkinter


class NCtkRadiobutton(Radiobutton, NCtkWidget):
    """Radiobutton widget which shows only one of several buttons in on-state.

        Valid resource names: activebackground, activeforeground, anchor,
        background, bd, bg, bitmap, borderwidth, command, cursor,
        disabledforeground, fg, font, foreground, height,
        highlightbackground, highlightcolor, highlightthickness, image,
        indicatoron, justify, padx, pady, relief, selectcolor, selectimage,
        state, takefocus, text, textvariable, underline, value, variable,
        width, wraplength."""
    def __init__(self, parent, x, y, w, h, content=None, command=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        Radiobutton.__init__(self, self._extFrame, text="Button")
        self._place_widget(x, y, w, h, padx, pady)
        self._calc_wrap = lambda self: self.winfo_width() - 20  # Used to calculate text wraplength when resized
        self.config(anchor=W, justify=LEFT)
        #self.master=parent
        #if isinstance(content, str):
            #self.config(text=content)
        #elif isinstance(content, StringVar):
            #self.config(textvariable=content)
        #elif isinstance(content, PhotoImage) or isinstance(content, BitmapImage):
            #self.config(image=content)
        #if command:
            #self.bind("<Button-1>", command)    
        ##Checkbutton.__init__(self, master=None, cnf={}, **kw):


class NCtkScale(Scale, NCtkWidget):
    """Scale widget which can display a numerical scale.

        Valid resource names: activebackground, background, bigincrement, bd,
        bg, borderwidth, command, cursor, digits, fg, font, foreground, from,
        highlightbackground, highlightcolor, highlightthickness, label,
        length, orient, relief, repeatdelay, repeatinterval, resolution,
        showvalue, sliderlength, sliderrelief, state, takefocus,
        tickinterval, to, troughcolor, variable, width."""
    def __init__(self, parent, x, y, w, h, content=None, command=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        hv = HORIZONTAL if w >= h else VERTICAL
        Scale.__init__(self, self._extFrame, orient=hv)
        self._place_widget(x, y, w, h, padx, pady)


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


class NCtkText(Text, NCtkWidget):
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
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        Text.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        #self.update()                   ### These were used in ther widgets for wrapping
        #realw = self.winfo_width() - 1  ### TODO: see if these are needed here (see NCtkLabel for example)
        self.config(relief=SUNKEN)
        
    def settext(self, t):
        self.clear()
        self.insert('end', t)
    
    def gettext(self):
        return self.get('1.0', 'end')
    
    def clear(self):
        self.delete('1.0', 'end')

    def tag_config(self, tagName, cnf=None, **kw):
        trans_kw = {}
        for k, v in kw.items():
            if k in _trans_opt:
                newk = _trans_opt[k]
                trans_kw[newk] = v
            else:
                newk = k
                trans_kw[newk] = v
        return self._configure(('tag', 'configure', tagName), cnf, trans_kw)
    
    
# Copied widgets from __init__ until Text (line 3172 of __init__)
# I don't know if others are to be modified

# Spinbox is unneeded (it is a variant of the entry)


# Used by NCtkCombobox. 
class _setitCombobox:
    """Internal class. It wraps the command in the widget OptionMenu."""
    def __init__(self, var, value, callback=None):
        self.__value = value
        self.__var = var
        self.__callback = callback
    def __call__(self, *args):
        self.__var.set(self.__value)
        if self.__callback:
            self.__callback(self.__value, *args)
            #self.__callback(*args)

class NCtkCombobox(OptionMenu, NCtkWidget):
    """Combobox which allows the user to select a value from a menu.
       It is the equivalent (renamed) of the OptionMenu class in tkinter
    """  
    def __init__(self, parent, x, y, w, h, command=None, items=[], pad=0):
        """Construct an optionmenu widget with the parent MASTER, with
        the resource textvariable set to VARIABLE, the initially selected
        value VALUE, the other menu values VALUES and an additional
        keyword argument command."""
        
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        self.intStr = StringVar()
        OptionMenu.__init__(self, self._extFrame, self.intStr, None)
        self._place_widget(x, y, w, x, padx, pady)
        #self.config(justify=LEFT, relief=SUNKEN, activestyle="none")
        self["menu"].delete(0)
        for value in items:
            self["menu"].add_command(label=value,
                                     command= _setitCombobox(self.intStr, value, command))
            

        """Construct menu widget with the parent MASTER.

        Valid resource names: activebackground, activeborderwidth,
        activeforeground, background, bd, bg, borderwidth, cursor,
        disabledforeground, fg, font, foreground, postcommand, relief,
        selectcolor, takefocus, tearoff, tearoffcommand, title, type."""

    #def activate(self, index):
        #"""Activate entry at INDEX."""
        #self.tk.call(self._w, 'activate', index)
    def add(self, item, cnf={}, **kw):
        if "command" in cnf.keys():
            cnf.delete("command")
        cnf.update({"label":item})
        self["menu"].add_command(cnf, kw)  
    def insert(self, index, item, cnf={}, **kw):
        if "command" in cnf.keys():
            cnf.delete("command")
        cnf.update({"label":item})        
        self["menu"].insert_command(index, cnf, **kw)    
    #def add(self, itemType, cnf={}, **kw):
        #"""Internal function."""
        #self.tk.call((self._w, 'add', itemType) +
                 #self._options(cnf, kw))
    #def add_command(self, cnf={}, **kw):
        #"""Add command menu item."""
        #self.add('command', cnf or kw)
    #def insert(self, index, itemType, cnf={}, **kw):
        #"""Internal function."""
        #self.tk.call((self._w, 'insert', index, itemType) +
                 #self._options(cnf, kw))
    #def insert_command(self, index, cnf={}, **kw):
        #"""Add command menu item at INDEX."""
        #self.insert(index, 'command', cnf or kw)
    def delete(self, index1, index2=None):
        """Delete menu items between INDEX1 and INDEX2 (included)."""
        self["menu"].delete(index1, index2)
    def entrycget(self, index, option):
        """Return the resource value of a menu item for OPTION at INDEX."""
        if option in _trans_opt:
            option = _trans_opt["option"]        
        return self["menu"].tk.call(self["menu"]._w, 'entrycget', index, '-' + option)
    entrygetconfig = entrycget
    def entryconfigure(self, index, cnf=None, **kw):
        """Configure a menu item at INDEX."""
        trans_kw = {}
        if isinstance(cnf, dict):
            for k, v in cnf.items():
                if k in _trans_opt:
                    trans_kw[_trans_opt[k]] = v
                else:
                    trans_kw[k] = v        
        for k, v in kw.items():
            if k in _trans_opt:
                trans_kw[_trans_opt[k]] = v
            else:
                trans_kw[k] = v        
        return self["menu"]._configure(('entryconfigure', index), trans_kw, {})
    entryconfig = entryconfigure
    def index(self, index):
        """Return the index of a menu item identified by INDEX."""
        i = self["menu"].tk.call(self["menu"]._w, 'index', index)
        if i == 'none': return None
        return self["menu"].tk.getint(i)
    def invoke(self, index):
        """Invoke a menu item identified by INDEX and execute
        the associated command."""
        return self["menu"].tk.call(self["menu"]._w, 'invoke', index)
    #def type(self, index):
        #"""Return the type of the menu item at INDEX."""
        #return self["menu"].tk.call(self["menu"]._w, 'type', index)


class NCtkSpinbox(Spinbox, NCtkWidget, XView):
    """spinbox widget."""
    
    def trace_text(self, *args):
        self.event_generate("<<CHANGEDVAR>>")
        #val = self.cget("values")
        #if val:
            #pass
    
        """

        STANDARD OPTIONS

            activebackground, background, borderwidth,
            cursor, exportselection, font, foreground,
            highlightbackground, highlightcolor,
            highlightthickness, insertbackground,
            insertborderwidth, insertofftime,
            insertontime, insertwidth, justify, relief,
            repeatdelay, repeatinterval,
            selectbackground, selectborderwidth
            selectforeground, takefocus, textvariable
            xscrollcommand.

        WIDGET-SPECIFIC OPTIONS

            buttonbackground, buttoncursor,
            buttondownrelief, buttonuprelief,
            command, disabledbackground,
            disabledforeground, format, from,
            invalidcommand, increment,
            readonlybackground, state, to,
            validate, validatecommand values,
            width, wrap,
        """
            
    def __init__(self, parent, x, y, w, h, limits=None, command=None, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        Spinbox.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        self.config(relief=SUNKEN)
        self.intStr = StringVar()
        if isinstance(limits, (list, tuple)):
            if isinstance(limits[0], str):
                self.config(values=limits)
            elif isinstance(limits[0], (int, float)):
                self.config(from_=limits[0], to=limits[1])
                if len(limits) == 3:
                    self.config(increment=limits[2])
                
        self.intStr.set(str(limits[0]))
        self.intStr.trace("w", self.trace_text)
        self.config(textvariable=self.intStr)
        if command:
            self.bind("<<CHANGEDVAR>>", command)
            
    # overrides NCtkWidget method!
    def setcontent(self, content):
        pass  # TODO
    
    def gettext(self):
        return self.get()


class NCtkNotebook(ttk.Notebook, NCtkWidget):
    """Ttk Notebook widget manages a collection of windows and displays
    a single one at a time. Each child window is associated with a tab,
    which the user may select to change the currently-displayed window."""
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        ttk.Notebook.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        #self.update()                   ### These were used in ther widgets for wrapping
        #realw = self.winfo_width() - 1  ### TODO: see if these are needed here (see NCtkLabel for example)
