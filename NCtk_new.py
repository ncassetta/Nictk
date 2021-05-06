##
# \file
# 
# The main file of the library
##

import tkinter as tk
from  tkinter import ALL, BOTH, BOTTOM, CENTER, DISABLED, E, END, FIRST, FLAT, GROOVE, HIDDEN, HORIZONTAL, LAST, \
LEFT, N, NE, NO, NORMAL, NS, NSEW, NW, RAISED, RIDGE, RIGHT, ROUND, S, SE, SEL, SINGLE, SOLID, SUNKEN, SW, TOP, \
VERTICAL, W, IntVar, StringVar, BooleanVar, mainloop
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb

PACK, FILL = "pack", "fill"

['bd', 'borderwidth', 'class', 'menu', 'relief', 'screen', 'use', 'background', 'bg', 'colormap', 'container', 'cursor', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx', 'pady', 'takefocus', 'visual', 'width']


            
# To get a widget property use w.cget("name")       name as string, always returns a string
# To set a widget property use w.config(name=val)


#####################################################################
###################    M I X I N   C L A S S E S
#####################################################################

class NCtkMisc:
    """Base class for windows and widgets.
    
It defines methods common for windows and interior widgets."""
    
   #TODO: what other methods should go here?
    _trans_opt =  { "abcolor":"activebackground", "afcolor":"activeforeground",
                    "bcolor":"background", "dfcolor":"disabledforeground",
                    "fcolor":"foreground", "hbcolor":"highlightbackground",
                    "hfcolor":"highlightcolor", "hborderwidth":"highlightthickness",
                    "rbcolor":"readonlybackground", "sbcolor":"selectbackground",
                    "sfcolor":"selectforeground", "textvar":"textvariable"}
    
    _del_opt = ["width", "height"]

    def config(self, cnf=None, **kw):
        """Configures resources of a widget.

    The values for resources are specified as keyword arguments. To get an overview
    about the allowed keyword arguments call the method keys().
    This method redefine tkinter config() to allow some changes in resource names;
    for detail see \ref ATTRIBUTES.
    \param cnf, kw the options
    \return"""
        if isinstance(cnf, dict):
            cnf.update(kw)
        elif cnf is None and kw:
            cnf = kw
        if cnf is None:
            trans_cnf = None
        else:
            trans_cnf = {}
            for k, v in cnf.items():
                if k in NCtkMisc._del_opt:
                    raise ValueError
                newk = NCtkMisc._trans_opt[k] if k in NCtkMisc._trans_opt else k
                trans_cnf[newk] = v
                # TODO: what other options must be config for the _extFrame???
                #if k == "bcolor" and hasattr(self, "_extFrame"):
                #    self._extFrame.config({newk:v})
        
        return self._configure('configure', trans_cnf, None)
    
    def getconfig(self, key):
        """Returns the value for the _key_ resource"""
        if key in self._trans_opt:
            key = self._trans_opt[key]
        return self.cget(key)
    
    def parent(self):
        """Returns the widget parent. See /ref WIDGET_INFO"""
        return self.master
    
    def toplevel(self):
        """Returns the widget toplevel container (a NCtkWindow or NCtkMain).
        See /ref WIDGET_INFO"""
        return self.nametowidget(self.winfo_toplevel())
            
    def getwinfo(self, key):
        """Returns the widget info for the item _key_.
        
        See /ref WIDGET_INFO"""
        function = "winfo_" + key
        return getattr(tk.Widget, function)(self)
    
    def winfo_x(self):
        """Redefines the tk function. The base function returns wrong values
        until you call update() or update_idletasks(), this gives the value
        calculated by the constructor.
        \note This method takes care of the pad you indicate in the constructor,
        if you must use it for spacing widgets you may want to use the value of
        the widget bounding box with winfo_bx()"""
        return self._curr_dim[0] + self._curr_dim[4][0]
    
    def winfo_y(self):
        """Redefines the tk function. See /ref winfo_x()"""
        return self._curr_dim[1] + self._curr_dim[4][1]
    
    def winfo_width(self):
        """Redefines the tk function. See /ref winfo_x()"""
        return self._curr_dim[2] - self._curr_dim[4][0] - self._curr_dim[4][2]
    
    def winfo_height(self):
        """Redefines the tk function. See /ref winfo_x()"""
        return self._curr_dim[3] - self._curr_dim[4][1] - self._curr_dim[4][3]
    
    def winfo_bx(self):
        """Returns the x coordinate of the widget bounding box topleft corner.
        See /ref winfo_x()"""
        return self._curr_dim[0]
    
    def winfo_by(self):
        """Returns the y coordinate of the widget bounding box topleft corner.
        See /ref winfo_x()"""        
        return self._curr_dim[1]
    
    def winfo_bwidth(self):
        """Returns the width of the widget bounding box.
        See /ref winfo_x()"""        
        return self._curr_dim[2]
    
    def winfo_bheight(self):
        """Returns the height of the widget bounding box.
        See /ref winfo_x()"""        
        return self._curr_dim[3]
    
    def winfo_bpad(self):
        """Returns the list of the four pad amounts (E-N-W-S).
        See /ref winfo_x()""" 
        return self._curr_dim[4]
        


class NCtkContainer:
    """Base class for widgets which can contain other widgets."""
    def __init__(self):
        """The constructor.
        
It only defines some internal variables used by its methods."""
        #elf.update()
        self._oldw, self._oldh = self.winfo_width(), self.winfo_height()
        #self.bind("<Configure>", self._resize_children)       ONLY FOR WINDOWS!!!
        self._cnfchildren = []
    
    def config_children(self, which, **kw):
        """Configures resources for all children.
    
All widgets which will be added to the container will be configured
with the selected values. If a child container calls config_children ()
in turn, the options dict is updated: if a resource receives a new
value it replaces the previous one, otherwise it remains unchanged.
\param self the widget instance
\param which you can indicate "all" for all children, or the name of a
widget class (for example "NCtkENtry" or "NCtkButton") or a tuple of
names for configuring only specific widgets.
\param kw a list of named options for the resources to be configured"""
        l = [item["which"] for item in self._cnfchildren]
        if which not in l:
            item = {"which":which, "options":kw}
            self._cnfchildren.append(item)
        else:
            self._cnfchildren[l.index(which)]["options"].update(kw)
        
    def _resize_children(self, event=None):
        """Internal function. Resizes all children when the container is resized."""
        #print("_resize_children() called by", self.winfo_name())
        #self.update()       # needed for updating w and h
        print ("_resize_children() called on", self.__str__())
        if isinstance(self, BaseWindow) and self.winfo_ismapped():
            self._curr_dim = (super().winfo_x(), super().winfo_y(), super().winfo_width(),
                             super().winfo_height(), (0, 0, 0, 0))
        if self._oldw != self.winfo_width() or self._oldh != self.winfo_height() or event is None:
            self._oldw, self._oldh = self.winfo_width(), self.winfo_height()
            for w in self.winfo_children():
                if hasattr(w, "_update_dimensions"):
                    w._update_dimensions()
                    if hasattr(w, "_resize_children"):
                        w._resize_children(event)                    
    


# Added by me to override tkinter Widget methods

class NCtkWidget(NCtkMisc):
    """Base class which defines methods common for all NCtk widgets."""
    def __init__(self, parent, x, y, w, h, pad, ctor, **kw):
        """The constructor."""
        self._orig_dim = (x, y, w, h, pad)      # tk.Widget.__init__ does nothing
        ctor(self, parent, kw)
        self._calc_dimensions()                 # sets _curr_dim
        self._place_widget()
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)): 
            parent.get_active().children.append(self)       
        
    def hide(self):
        """Hides the widget.

The widget will not be displayed, but its data remain managed; use show()
to newly display the widget. if the widget was already hidden it does nothing."""
        #if self.winfo_ismapped():
        self.place_forget()
    
    def show(self):
        """Shows a previously hidden widget.
        
If the widget was already shown it does nothing."""        
        if not self.visible():
            self._place_widget()
            #self.config(width=self.winfo_width(), height=self.winfo_height())
            #print("x=")
            
    def visible(self):
        """Returns True if the widget is visible."""
        return self.winfo_ismapped()
    
    def getcontent(self):
        return self.cget("text")
        
    def setcontent(self, content):
        if isinstance(content, str):
            self.config(text=content, textvariable=None, image="")
        elif isinstance(content, tk.StringVar):
            self.config(text=content, textvariable=content, image="")
        elif isinstance(content, tk.PhotoImage) or isinstance(content, tk.BitmapImage):
            self.config(text="", textvariable=None, image=content)        
    
    #def gettext(self):
    #    return self.cget("variable")
    
    def resize(self, x=None, y=None, w=None, h=None, pad=None):
        self._orig_dim = (
            self._orig_dim[0] if x is None else x,
            self._orig_dim[1] if y is None else y,
            self._orig_dim[2] if w is None else w,
            self._orig_dim[3] if h is None else h,
            self._orig_dim[4] if pad is None else pad)
        self.parent()._resize_children()
        
    
    def _calc_dimensions(self):                 #TODO: implement "rpack"
        """Internal function.
        Translates the coordinates given by the user into numerical values."""
        #parent.update_idletasks()
        
        x, y, w, h, pad = self._orig_dim
        if not pad:                             # transform pad into a quadruple (ENWS)
            pad = (0, 0, 0, 0)
        elif isinstance(pad, int):
            pad = (pad, pad, pad, pad)
        elif isinstance(pad, (tuple, list)):
            if len(pad) == 2:
                pad = (pad[0], pad[1], pad[0], pad[1])
            elif len(pad) == 4:
                pad = (pad[0], pad[1], pad[2], pad[3])
            else:
                raise ValueError
        else:
            raise TypeError
            
        offs_x, offs_y = 0, 0
        parent = self.parent()
        if isinstance(parent, NCtkRowFrame):                                                 
            parent = parent.get_active()
            offs_y = parent.winfo_y()
        elif isinstance(parent, (NCtkColFrame)):                                              
            parent = parent.get_active()
            offs_x = parent.winfo_x()
        
        # find the last widget from whom calculate coords
        brothers = [w for w in parent.winfo_children() if not isinstance(w, tk.Menu)]
        if self in brothers:                    # we are resizing an already placed widget
            last_wdg = brothers[brothers.index(self) - 1] if brothers.index(self) > 0 else None
        else:                                   # we are placing a new widget
            last_wdg = brothers[-1] if len(brothers) else None
        last_x, last_y = 0, 0
        if isinstance(parent, (NCtkHorFrame, _framerow))and last_wdg:
            last_x = last_wdg.winfo_bx() + last_wdg.winfo_bwidth()
        elif isinstance(parent, (NCtkVerFrame, _framecol, NCtkMain, NCtkWindow)) and last_wdg:
            last_y = last_wdg.winfo_by() + last_wdg.winfo_bheight() 
        #print ("parent name:", parent.winfo_name(), "   width:", parent.winfo_width(), "height:", parent.winfo_height(),
               #"reqwidth:", parent.winfo_width(), "reqheight:", parent.winfo_height())
        
        if isinstance(x, str):                  # calculate x
            if x == "pack":
                x = last_x
            elif x == "center":
                tempw = w
                if isinstance(tempw, str):
                    if tempw == "fill":
                        raise TypeError
                    elif tempw.endswith("%"):
                        tempw = round(parent.winfo_width() * int(tempw[:-1]) / 100)
                    else:
                        raise TypeError
                x = round((parent.winfo_bwidth() - tempw) / 2)
            elif x.endswith("%"):
                x = round(parent.winfo_width() * int(x[:-1]) / 100)
        elif x < 0:
            x = parent.winfo_width() + x
            if x < 0:
                raise ValueError
        if isinstance(y, str):                  # calculate y
            if y == "pack":
                y = last_y
            elif y == "center":
                temph = h
                if isinstance(temph, str):
                    if temph == "fill":
                        raise ValueError
                    elif temph.endswith("%"):
                        temph = round(parent.winfo_height() * int(temph[:-1]) / 100)
                    else:
                        raise TypeError
                y = round((parent.winfo_height() - temph) / 2)            
            elif y.endswith("%"):
                y = round(parent.winfo_height() * int(y[:-1]) / 100)
        elif y < 0:
            y = parent.winfo_height() + y
            if y < 0:
                raise ValueError
        if isinstance(w, str):                  # calculate w
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
        if isinstance(h, str):                  # calculate h
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
            
        x += offs_x
        y += offs_y
        self._curr_dim = (x, y, w, h, pad)
        
    def _update_dimensions(self):
        #print("_update_dimensions called on", self.winfo_name())
        self._calc_dimensions()
        if self.winfo_ismapped():
            print("Eseguo _place_widget() su", self.getwinfo("name"))
            self._place_widget()         
            
    def _place_widget(self):
        """Internal function.
    
Places the widget, once _calc_dimensions() has translated the
user coordinates into numerical values"""
        self.place_forget()
        x = self.winfo_x()
        y = self.winfo_y()
        w = self.winfo_width()
        h = self.winfo_height()
        self.place(x=x, y=y, width=w, height=h)       
        if isinstance(self, (NCtkLabel, NCtkCheckbutton, NCtkRadiobutton)):
            self.config(wraplength=self._calc_wrap())
        if hasattr(self, "_vscroll"):
            self._auto_yscroll()        
            
    def _auto_yscroll(self):
        if hasattr(self, "_vscroll"):
            self.update_idletasks()
            offs, size = self.yview()
            if size - offs < 1.0 and not self._vscroll.winfo_ismapped():                
                self._vscroll.pack(side=RIGHT, fill=BOTH)                 
            elif size - offs == 1.0 and self._vscroll.winfo_ismapped():
                self._vscroll.pack_forget()
            self.update_idletasks()         # needed for drawing the scrollbar
    
    def _get_parent_config(self):
        cl = "NCtk" + self.winfo_class()
        p = self.parent()
        while p:
            if hasattr(p, "_cnfchildren"):
                for item in p._cnfchildren:
                    wh = item["which"]
                    try:
                        if isinstance(wh, str) and (wh == "all" or wh == cl):
                            self.config(item["options"])
                        elif isinstance(wh, (list, tuple)) and cl in wh:
                            self.config(item["options"])
                    except (ValueError, TclError):
                        pass
            p = p.parent()

         
# Used by various widgets for calling with command with an event parameter. 
class _setitCommand:
    """Internal class. It wraps the command in widgets which have a command option."""
    def __init__(self, widget, callback=None, value=None):
        self._widget = widget
        self._callback = callback
        self._value = value
        
    def __call__(self):
        if self._callback:
            ev = tk.Event
            ev.type = tk.EventType.VirtualEvent
            ev.widget = self._widget
            ev.x = self._widget.winfo_pointerx()
            ev.y = self._widget.winfo_pointery()            
            ev.value = self._value
            self._callback(ev)



#####################################################################
###################    M A I N   W I N D O W S
#####################################################################

class BaseWindow(NCtkMisc, NCtkContainer):
    """Base class for both NCtkMain and NCtkWindow.
    
It implements some common methods."""
    def __init__(self, x, y, w, h, title=""):
        """Common constructor for NCtkMain and NCtkWindow.
        
\param self the object instance
\param x, y, w, h see \ref PLACING_WIDGETS
\param title the window title"""
        self.geometry("{}x{}+{}+{}".format(w, h, x, y))
        self._curr_dim = (x, y, w, h, (0, 0, 0, 0))
        NCtkContainer.__init__(self)
        super().bind("<Configure>", self._resize_children) 
        #self.resizable(width=FALSE, height=FALSE)
        self.title(title)
        
    # we must redefine bind() and unbind(): if the user is binding to "<Configure>"
    # event we must mantain the binding to _resize_children
    
    def bind(self, sequence=None, func=None, add=None):
        """Redefines the Misc.bind() method for this class."""
        # If sequence has more than one event, they must happen in sequence
        # for the func is triggered. So sequence="<Configure><Enter>" does not
        # affect <Configure>
        if sequence == "<Configure>":
            return super().bind(sequence, func, add=True)
        else:
            return super().bind(sequence, func, add)
            
    
    def unbind(self, sequence, funcid=None):
        """Redefines the Misc.unbind method for this class."""
        super().unbind(sequence, funcid)
        if sequence == "<Configure>" and not funcid:
            super().bind("<Configure>", self._resize_children)   
            
            
            
                
        
        
    
class NCtkMain(BaseWindow, tk.Tk):
    """The main window of the app.
    
    This is the main window (derived from the tkinter Tk class).
    It has an associated Tcl interpreter"""
    def __init__(self, x, y, w, h, title=""):
        """The constructor.
        
    \param self the object instance
    \param x, y, w, h see \ref PLACING_WIDGETS
    \param title the window title"""           
        tk.Tk.__init__(self)
        BaseWindow.__init__(self, x, y, w, h, title)
        
                    
class NCtkWindow(BaseWindow, tk.Toplevel):
    """A window (derived from the tkinter Toplevel class).
    
    You can use this for dialogs"""    
    def __init__(self, parent, x, y, w, h, title="", modal=NORMAL):
        """The constructor.
        
\param self the object instance
\param parent TODO
\param x, y, w, h see \ref PLACING_WIDGETS
\param title the window title
\param modal if True the window mantains the focus until
you close it"""        
        tk.Toplevel.__init__(self, master=parent)
        #xp = parent.winfo_x()
        #yp = parent.winfo_y()
        BaseWindow.__init__(self, x, y, w, h, title)
        self._modal = modal
        self.show()
            
    def show(self):
        if self._modal == "modal":
            self.transient(self.parent())
            self.focus_force() # added
            self.grab_set()      
        elif self._modal == "persistent":
            self.attributes('-topmost', 'true')
        else:
            self.attributes('-topmost', 'false')
        self.deiconify()
            
    def hide(self):
        self.grab_release()
        self.withdraw()
        
    def setmodal(self, t):
        self._modal = t
    


#####################################################################
#######################     F R A M E S
#####################################################################

class NCtkHorFrame(NCtkWidget, NCtkContainer, ttk.LabelFrame):
    """A container in which you can stack children widgets horizontally.

This is done by using PACK as the x parameter in their constructor. The
frame is initialized with the same color of its parent and no border,
being so invisible. However you can set a border and also a label to be
shown on it.
\warning setting a border reduces the space inside the frame"""
    
    def __init__(self, parent, x, y, w, h, pad=0):
        """The constructor.
        
\param self
\param parent the frame parent
\param x, y, w, h, see \ref ***
\param pad this is ignored, you cannot have a padding on frames"""        
        NCtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        self.config(background=parent.cget("background"), relief=FLAT)
        NCtkContainer.__init__(self)
 
 
class NCtkVerFrame(NCtkWidget, NCtkContainer, ttk.LabelFrame):
    """A container in which you can stack children widgets vertically.
    
This is done by using PACK as the y parameter in their constructor. The
frame is initialized with the same color of its parent and no border,
being so invisible. However you can set a border and also a label to be
shown on it.
\warning setting a border reduces the space inside the frame"""
    def __init__(self, parent, x, y, w, h, pad=0):
        """The constructor.    
    
\param self
\param parent the frame parent
\param x, y, w, h, see \ref ***
\param pad this is ignored, you cannot have a padding on frames"""                
        NCtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        self.config(background=parent.cget("background"), relief=FLAT)
        NCtkContainer.__init__(self)
        
        
class _framerow():
    """! Internal class."""
    def __init__(self, parent, h):
        self._master = parent
        self.num = len(parent._rows)
        self.children = []
        self._orig_h = h
        self._calc_dimensions()

    #def __str__(self):
    #    return str({"master":self.master,"num":self.num, "y":self.y,
    #                "origh":self.orig_h, "h":self.h, "toth":self.tot_h })
        
    def parent(self):
        return self._master
    
    def winfo_children(self):
        """Returns the list of the row children."""
        return self.children

    def winfo_x(self):
        """Returns the x coordinate of the row topleft with respect to parent.
        Actually it is always 0."""
        return 0

    winfo_bx = winfo_x

    def winfo_y(self):
        """Returns the y coordinate of the row topleft with respect to parent."""
        return self._curr_dim[1]

    winfo_by = winfo_y
    
    def winfo_width(self):
        """Returns width of the row. Actually it is the same of the parent."""
        return self._curr_dim[2]

    winfo_bwidth = winfo_width

    def winfo_height(self):
        """Returns the height of the row."""
        return self._curr_dim[3]
    
    winfo_bheight = winfo_height

    def winfo_name(self):
        return "_framerow"
        
    def _calc_dimensions(self):
        """Internal function.
        Translates the coordinates given by the user into numerical values."""
        #parent.update_idletasks()
        n, h = self.num, self._orig_h
        parent = self.parent()
        if n == len(parent._rows):                  # we are placing a new row
            y = 0 if not len(parent._rows) else parent._rows[-1].tot_h
        else:                                       # already placed row
            y = 0 if n == 0 else parent._rows[n - 1].tot_h
        if isinstance(h, str):
            if h.endswith("%"):
                h = round(parent.winfo_height() * int(h[:-1]) / 100)
            elif h == "fill":
                if n == len(parent._rows):
                    h = parent.winfo_height() if not len(parent._rows) else \
                        parent.winfo_height() - parent._rows[-1].tot_h
                else:
                    h = parent.winfo_height() if n == 0 else \
                        parent.winfo_height() - parent._rows[n - 1].tot_h
        elif isinstance(h, int):
            if h < 0:
                h = parent.winfo_height() - y + h
                if h < 0:
                    raise ValueError
        else:
            raise TypeError
        self._curr_dim = (0, y, parent.winfo_width(), h)
        self.tot_h = y + h
        #print(self) 
        
    def _resize_children(self, event=None):
        """Internal function. Resizes all children when the container is resized."""
        oldactivenum = self.parent().get_active().num
        self.parent().set_active(self.num)
        for w in self.winfo_children():
            if hasattr(w, "_update_dimensions"):
                w._update_dimensions()
                if hasattr(w, "_resize_children"):
                    w._resize_children(event)
        self.parent().set_active(oldactivenum)


class _framecol:
    pass


class NCtkRowFrame(NCtkWidget, NCtkContainer, ttk.LabelFrame):
    """A container in which you can stack rows vertically.
    
Each row behaves like a NCtkHorFrame, allowing to stack children
widgets horizontally (using PACK as the x parameter in their constructor).
You can add rows to the frame, obtaining thus a disposition similar
to a matrix.
The frame is initialized with the same color of its parent and no border,
being so invisible. However you can set a border and also a label to be
shown on it.
\warning setting a border reduces the space inside the frame"""    
    def __init__(self, parent, x, y, w, h, pad=0):
        """The constructor.
        
The frame has initially no rows, and you must add them with the
add_row() method.
\param self
\param parent the frame parent
\param x, y, w, h, see \ref PLACING_WIDGETS
\param pad this is ignored, you cannot have a padding on frames"""         
        NCtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        self.config(background=parent.cget("background"), relief=FLAT)
        NCtkContainer.__init__(self)
        self._rows = []
        self._active = None
        
    def add_row(self, h):
        """Adds a row to the frame.
        
Rows are stacked vertically from top to bottom. This also sets
the new row as the active one: newly created widgets will belong
to this row.
\param self
\param h the height of the row (the width coincides with the frame one)"""
        self._rows.append(_framerow(self, h))
        self._active = self._rows[-1].num
        
    def set_active(self, n):
        if 0 <= n < len(self._rows):
            self._active = n
            
    def get_active(self):
        if self._active is None:
            raise ValueError
        return self._rows[self._active]
        
    def _resize_children(self, event=None):
        for row in self._rows:
            row._calc_dimensions()        
            row._resize_children()
                    
    
class NCtkColFrame(NCtkWidget, NCtkContainer, ttk.LabelFrame):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        self.config(background=parent.cget("background"), relief=FLAT)
        NCtkContainer.__init__(self)
        self._cols = []
        self._active = None
        
    def add_col(self, h):
        self._cols.append(_framerow(self, h))
        self._active = self._cols[-1]
        
    def set_active(self, n):
        if 0 <= n < len(self._cols):
            self._active = n
                
            

#####################################################################
############       tkinter WIDGETS SUPERCLASSES
#####################################################################     

class NCtkButton(NCtkWidget, ttk.Button):
    """Button widget.

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
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Button.__init__)
        self.config(anchor=CENTER, justify=LEFT)
        self._get_parent_config()
        self.setcontent(content)
        self.commandwrap = None
        if command:
            self.config(command=command)
            
    def config(self, cnf=None, **kw): # override for command
        if "command" in kw.keys():
            cback = kw.pop("command")
            if "value" in kw.keys():
                value = kw.pop("value")
                self.value = value
                self.commandwrap = _setitCommand(self, cback, value)
            else:
                self.commandwrap = _setitCommand(self, cback)
            super().config(command=self.commandwrap)
        return super().config(cnf,**kw)     


class NCTkCanvas(tk.Canvas):
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


class NCtkCheckbutton(NCtkWidget, ttk.Checkbutton):     ## TODO: manage command
    """Checkbutton widget which is either in on- or off-state.

    Valid resource names: activebackground, activeforeground, anchor,
    background, bd, bg, bitmap, borderwidth, command, cursor,
    disabledforeground, fg, font, foreground, height,
    highlightbackground, highlightcolor, highlightthickness, image,
    indicatoron, justify, offvalue, onvalue, padx, pady, relief,
    selectcolor, selectimage, state, takefocus, text, textvariable,
    underline, variable, width, wraplength."""    
    #def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
    
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Checkbutton.__init__)
        self.config(anchor=W, justify=LEFT, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.setcontent(content)
        self._cmd_callback = None
        if command:
            self.config(command=command)
            
    def setvariable(self, variable=None, offvalue=None, onvalue=None):
        if variable:
            self.config(variable=variable)
        if offvalue:
            self.config(offvalue=offvalue)
        if onvalue:
            self.config(onvalue=onvalue)
    
    def getvariable(self):
        return self.cget("variable")
    
    def config(self, cnf=None, **kw): # override for command
        if "command" in kw.keys():
            cback = kw.pop("command")
            if "value" in kw.keys():
                value = kw.pop("value")
                self.value = value
                self.commandwrap = _setitCommand(self, cback, value)
            else:
                self.commandwrap = _setitCommand(self, cback)
            super().config(command=self.commandwrap)
        return super(NCtkCheckbutton, self).config(cnf,**kw)
    
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        self.update_idletasks()         # sets correct sizes
        return self.winfo_width() - 20    
            

class NCtkEntry(NCtkWidget, ttk.Entry):
    """Entry widget which allows displaying simple text.
    
    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand."""
    
        
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Entry.__init__)
        self.config(relief=SUNKEN)
        self._get_parent_config()
        self.intStr = tk.StringVar(name="var_"+self._name)
        if content:
            self.intStr.set(str(content))
        self.intStr.trace("w", lambda *args: self.event_generate("<<CHANGEDVAR>>"))
        self.config(textvariable=self.intStr)
        if command:
            self.bind("<Return>", command)
        
    # overrides NCtkWidget methods!
    def setcontent(self, content):
        self.intStr.set(str(content))
        
    def getcontent(self):
        return self.intStr.get()        


# class Frame substituted by NCtkHorFrame, NCtkVerFrame   
    
class NCtkLabel(NCtkWidget, ttk.Label):
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
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Label.__init__)
        self.config(anchor=W, justify=LEFT, relief=SUNKEN, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.setcontent(content)
        
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        #self.update_idletasks()         # sets correct sizes
        return self.winfo_width() - 1  
        
    
class NCtkListbox(NCtkWidget, tk.Listbox):
    """Listbox widget which can display a list of strings.

        Valid resource names: background, bd, bg, borderwidth, cursor,
        exportselection, fg, font, foreground, height, highlightbackground,
        highlightcolor, highlightthickness, relief, selectbackground,
        selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
        width, xscrollcommand, yscrollcommand, listvariable."""
    # and activestyle ???
    def __init__(self, parent, x, y, w, h, pad=0, command=None, items=None) :
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Listbox.__init__)
        self.config(justify=LEFT, relief=SUNKEN, activestyle="none", exportselection=False)
        self._get_parent_config()
        self._vscroll = tk.Scrollbar(self, orient=VERTICAL)
        self.config(yscrollcommand=self._vscroll.set)
        self._vscroll.config(command=self.yview)
        if command:
            self.bind("<<ListboxSelect>>", command)
        if items:
            for i in items:
                self.insert(END, i)
            
    def insert(self, index, *elements):
        #self.update()
        tk.Listbox.insert(self, index, *elements)
        self._auto_yscroll()
        self.see(index)
            
    def delete(self, first, last=None):
        tk.Listbox.delete(self, first, last=None)
        self._auto_yscroll()
                
    getselected = tk.Listbox.curselection
        #return (() if self.curselection() == "" else self.curselection())
            


### UNUSED ??? ###
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
        
class NCtkMenu(NCtkMisc, tk.Menu):
    """Menu widget which allows displaying menu bars, pull-down menus and pop-up menus.
        
        Valid resource names: activebackground, activeborderwidth,
        activeforeground, background, bd, bg, borderwidth, cursor,
        disabledforeground, fg, font, foreground, postcommand, relief,
        selectcolor, takefocus, tearoff, tearoffcommand, title, type."""
    def __init__(self, parent):
        tk.Menu.__init__(self, parent, tearoff=0)
        self.value = None
        
    # These override the Menu methods to insert the "value" option
    def getconfig(self, key):
        """Returns the value for the _key_ resource"""
        if key == "value":
            return self.value
        if key in self._trans_opt:
            key = self._trans_opt[key]
        return self.cget(key)    

    def add(self, itemType, cnf={}, **kw):
        if "command" in cnf.keys():
            cback = cnf["command"]
            if "value" in cnf.keys():
                value = cnf.pop("value")
                self.commandwrap = _setitCommand(self, cback, value)
            else:
                self.commandwrap = _setitCommand(self, cback)
            cnf.update({"command":self.commandwrap})        
        
        
        
        #if "command" in cnf.keys():
            #if "arg" in cnf.keys():
                #cmd = _setitMenu(cnf["arg"], cnf["command"])
                #cnf.pop("arg")
            #else:
                #cmd = _setitMenu(cnf["label"], cnf["command"])
            #cnf.update({"command":cmd})
        self.tk.call((self._w, 'add', itemType) +
                 self._options(cnf, kw))   
        
    def insert(self, index, itemType, cnf={}, **kw):
        if "value" in cnf.keys():
            self.value = cnf["value"]
            cnf.pop("value")        
        if "command" in cnf.keys():
            cmd = _setitMenu(cnf["label"], cnf["command"])
            cnf.update({"command":cmd})        
        self.tk.call((self._w, 'insert', index, itemType) +
                 self._options(cnf, kw))
        
    def entrycget(self, index, option):
        """Return the resource value of a menu item for OPTION at INDEX."""
        if option == "value":
            return self.value
        if option in NCtkMisc._trans_opt:
            option = NCtkMisc._trans_opt["option"]
        return self.tk.call(self._w, 'entrycget', index, '-' + option)
    entrygetconfig = entrycget
    
    def entryconfigure(self, index, cnf=None, **kw):
        """Configure a menu item at INDEX."""
        trans_kw = {}
        if isinstance(cnf, dict):
            for k, v in cnf.items():
                if k in NCtkMisc._trans_opt:
                    trans_kw[_trans_opt[k]] = v
                else:
                    trans_kw[k] = v        
        for k, v in kw.items():
            if k in NCtkMisc._trans_opt:
                trans_kw[NCtkMisc._trans_opt[k]] = v
            else:
                trans_kw[k] = v        
        return self._configure(('entryconfigure', index), trans_kw, {})
    entryconfig = entryconfigure
    
# MenuButton and Message obsolete in tkinter


class NCtkRadiobutton(NCtkWidget, ttk.Radiobutton):
    """Radiobutton widget which shows only one of several buttons in on-state.

        Valid resource names: activebackground, activeforeground, anchor,
        background, bd, bg, bitmap, borderwidth, command, cursor,
        disabledforeground, fg, font, foreground, height,
        highlightbackground, highlightcolor, highlightthickness, image,
        indicatoron, justify, padx, pady, relief, selectcolor, selectimage,
        state, takefocus, text, textvariable, underline, value, variable,
        width, wraplength."""
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Radiobutton.__init__)
        self.config(anchor=W, justify=LEFT, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.setcontent(content)
        if command:
            self.config(command=command)    
        
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        self.update_idletasks()         # sets correct sizes
        return self.winfo_width() - 20   

    def config(self, cnf=None, **kw): # override for command
        if "command" in kw.keys():
            cback = kw.pop("command")
            self.commandwrap = _setitCommand(self, cback)
            super().config(command=self.commandwrap)
        return super().config(cnf,**kw)    
    

class NCtkScale(NCtkWidget, ttk.Scale):
    """Scale widget which can display a numerical scale.

        Valid resource names: activebackground, background, bigincrement, bd,
        bg, borderwidth, command, cursor, digits, fg, font, foreground, from,
        highlightbackground, highlightcolor, highlightthickness, label,
        length, orient, relief, repeatdelay, repeatinterval, resolution,
        showvalue, sliderlength, sliderrelief, state, takefocus,
        tickinterval, to, troughcolor, variable, width."""
    def __init__(self, parent, x, y, w, h,  pad=0, limits= None, command=None):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Scale.__init__)
         # _box_dim[2] and _box_dim[3] are true w and h
        hv = HORIZONTAL if self._box_dim[2] >= self._box_dim[3] else VERTICAL  
        self.config(orient=hv)
        if isinstance(limits, (list, tuple)):
            if isinstance(limits[0], str):
                self.config(values=limits)
            elif isinstance(limits[0], (int, float)):
                self.config(from_=limits[0], to=limits[1])
                if len(limits) == 3:
                    self.config(bigincrement=limits[2])
        self.intStr = tk.StringVar()
        self.intStr.set(str(limits[0]))
        self.intStr.trace("w", lambda *args: self.event_generate("<<CHANGEDVAR>>"))
        self.config(variable=self.intStr)
        self._get_parent_config()
        if command:
            self.config(command=command)
        
        def config(self, cnf=None, **kw): # override for command
            if "command" in kw.keys():
                cback = kw.pop("command")
                self.commandwrap = _setitCommand(self, cback)
                super().config(command=self.commandwrap)
            return super().config(cnf,**kw)
        
        def getcontent(self):
            return self.intStr.get()        


class NCtkScrollbar(ttk.Scrollbar):
    """Scrollbar widget which displays a slider at a certain position.

        Valid resource names: activebackground, activerelief,
        background, bd, bg, borderwidth, command, cursor,
        elementborderwidth, highlightbackground,
        highlightcolor, highlightthickness, jump, orient,
        relief, repeatdelay, repeatinterval, takefocus,
        troughcolor, width."""
    def __init__(self, master=None, cnf={}, **kw):
        tk:Scrollbar.__init_(self, master, cnf, kw)


class NCtkSpinbox(NCtkWidget, ttk.Spinbox):
    """spinbox widget.

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
    
    #def trace_text(self, *args):
        #self.event_generate("<<CHANGEDVAR>>")
        #val = self.cget("values")
        #if val:
            #pass
    
       
            
    def __init__(self, parent, x, y, w, h, pad=0, limits=None, command=None):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Spinbox.__init__)
        self.config(relief=SUNKEN)
        if isinstance(limits, (list, tuple)):
            if isinstance(limits[0], str):
                self.config(values=limits)
            elif isinstance(limits[0], (int, float)):
                self.config(from_=limits[0], to=limits[1])
                if len(limits) == 3:
                    self.config(increment=limits[2])      
        self.intStr = tk.StringVar()
        if limits:
            self.intStr.set(str(limits[0]))
        self.intStr.trace("w", lambda *args: self.event_generate("<<CHANGEDVAR>>"))
        self.config(textvariable=self.intStr)
        self._get_parent_config()
        if command:
            self.config(command=command)
            self.bind("<Key-Return>", command)
        autoaddflag = False

    def config(self, cnf=None, **kw): # override for command
        if "command" in kw.keys():
            cback = kw.pop("command")
            self.commandwrap = _setitCommand(self, cback)
            super().config(command=self.commandwrap)
        return super().config(cnf,**kw)
    
    def mode(self, mode, wrap=False, validate=None):
        if mode in ("NORMAL", "readonly"):
            self.config(state=mode)
            autoaddflag = False
        elif mode == "autoadd":
            self.config(state="NORMAL")
            autoaddflag = True
        self.config(wrap=wrap)
            
    # overrides NCtkWidget method!
    def setcontent(self, content):
        self.delete(0, END)
        self.insert(0, content)
    
    def getcontent(self):
        return self.intStr.get()



class NCtkText(NCtkWidget, tk.Text):
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
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Text.__init__)
        self.config(relief=SUNKEN)
        self._get_parent_config()
        self._vscroll = tk.Scrollbar(self._extFrame, orient=VERTICAL)
        self.config(_yscrollcommand=self._vscroll.set)
        self._vscroll.config(command=self.yview)        
               
    def appendtext(self, t):
        self.insert(END, t)
        self._auto_yscroll()
    
    def settext(self, t):
        self.clear()
        self.insert(END, t)
        self._auto_yscroll()
    
    def gettext(self):
        return self.get('1.0', 'end')
    
    def clear(self):
        self.delete('1.0', 'end')
        self._auto_yscroll()

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

class NCtkCombobox(NCtkWidget, ttk.Combobox):
    """Combobox which allows the user to select a value from a menu.
       It is the equivalent (renamed) of the OptionMenu class in tkinter
       

        Valid resource names: activebackground, activeborderwidth,
        activeforeground, background, bd, bg, borderwidth, cursor,
        disabledforeground, fg, font, foreground, postcommand, relief,
        selectcolor, takefocus, tearoff, tearoffcommand, title, type.
    """  
    def __init__(self, parent, x, y, w, h, pad=0, items=[], command=None,):
        """Construct an optionmenu widget with the parent MASTER, with
        the resource textvariable set to VARIABLE, the initially selected
        value VALUE, the other menu values VALUES and an additional
        keyword argument command."""
        
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.OptionMenu.__init__, values=items, value=0)
        self.config(relief=SUNKEN)
        self._get_parent_config()
        self.commandwrap = _setitCommand(self, command)
        self["menu"].delete(0)
        for value in items:
            self["menu"].add_command(label=value, command=self.commandwrap)
            
        
            
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
        
    def gettext(self):
        return self.intStr.get()




class NCtkNotebook(NCtkWidget, ttk.Notebook):
    """Ttk Notebook widget manages a collection of windows and displays
    a single one at a time. Each child window is associated with a tab,
    which the user may select to change the currently-displayed window."""
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Notebook.__init__)
        self._get_parent_config()
        
