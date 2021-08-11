# This file is part of Ntk - A simple tkinter wrapper.
#    Copyright (C) 2021  Nicola Cassetta
#    See <https://github.com/ncassetta/Ntk>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


## \file 
#
# The main file of the library
#


import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
from .constants import *

__version__ = "1.0.0"


## @cond IGNORE
#####################################################################
###################    M I X I N   C L A S S E S
#####################################################################
## @endcond



class NtkMisc:
    """Base class for windows and widgets.
    It defines methods common for windows and interior widgets."""

    _trans_opt =  { "abcolor":"activebackground", "afcolor":"activeforeground",
                    "bcolor":"background", "dfcolor":"disabledforeground",
                    "fcolor":"foreground", "hbcolor":"highlightbackground",
                    "hfcolor":"highlightcolor", "hborder":"highlightthickness",
                    "ibcolor":"insertbackground", "rbcolor":"readonlybackground",
                    "sbcolor":"selectbackground", "sfcolor":"selectforeground",
                    "tcolor":"troughcolor"}
    
    _del_opt = ["width", "height"]

    def config(self, cnf=None, **kw):
        """Configures resources of a widget.
        The values for resources are specified as keyword arguments. To get an overview
        about the allowed keyword arguments call the method keys().
        This method redefine tkinter config() to allow some changes in resource names;
        for detail see \ref ATTRIBUTES.
        \param cnf, kw the options.
        \see \ref WidgetOptions.py example file"""
        if isinstance(cnf, dict):
            cnf.update(kw)
        elif cnf is None and kw:
            cnf = kw
        if cnf is None:
            trans_cnf = None
        else:
            if isinstance(self, (NtkButton, NtkCheckbutton, NtkCombobox, NtkListbox, NtkMenu, 
                                 NtkRadiobutton, NtkScale, NtkSpinbox)) and "command" in cnf.keys():
                cmd = cnf.pop("command")
                cback, value = ((cmd, None) if callable(cmd) else (cmd[0], cmd[1]))
                # _commandwrap is the  __call__ wrapper for the command callback
                self._commandwrap = _setitCommand(self, cback, value)
                super().config(command=self._commandwrap)            
            trans_cnf = {}
            for k, v in cnf.items():
                if k in NtkMisc._del_opt:
                    raise ValueError
                newk = NtkMisc._trans_opt[k] if k in NtkMisc._trans_opt else k
                trans_cnf[newk] = v
                # TODO: what other options must be config for the _extFrame???
        
        return self._configure('configure', None, trans_cnf)
    
    def get_config(self, key):
        """Returns the value for the _key_ resource.
        \param key a string which indicates what we want to know."""
        if key in self._trans_opt:
            key = self._trans_opt[key]
        return self.cget(key)
    
    def parent(self):
        """Returns the widget parent. See \ref WIDGET_INFO"""
        return self.master
    
    def toplevel(self):
        """Returns the widget toplevel container (a NtkWindow or NtkMain).
        See \ref WIDGET_INFO"""
        return self.nametowidget(self.winfo_toplevel())
    
    def has_option(self, opt=None):
        """Returns **True** if the widget admits the given option.
        \param opt if you leave None the method returns a list of
        all its options as strings. If you give an option (string)
        returns **True** or **False**"""
        if not opt:
            return self.keys()
        else:
            return True if opt in self.keys() else False
            
    def get_winfo(self, key):
        """Returns the widget info for the item _key_.
        \param key a string which indicates what we want to know.
        See \ref WIDGET_INFO for a list
        \see \ref winfo.py example file""" 
        function = "winfo_" + key
        return getattr(tk.Widget, function)(self)
    
    def winfo_x(self):
        """Returns the x coordinate of the topleft corner of the widget with
        respect to the parent. It redefines the tk function, because it returns
        wrong values until you call update() or update_idletasks(), while this
        gives the value calculated by the constructor.
        \note This method takes into account the pad you indicate in the constructor,
        so if you must use it for spacing widgets you may want to use the value of
        the widget bounding box with winfo_bx()"""
        return self._curr_dim[0] + self._curr_dim[4][0]
    
    def winfo_y(self):
        """Returns the y coordinate of the topleft corner of the widget with
        respect to the parent. See winfo_x() for details."""
        return self._curr_dim[1] + self._curr_dim[4][1]
    
    def winfo_width(self):
        """Returns the widget width. It redefines the tk function, and is
        aliased by winfo_w(). See winfo_x() for details."""
        return self._curr_dim[2] - self._curr_dim[4][0] - self._curr_dim[4][2]
    
    def winfo_height(self):
        """Returns the widget height. It redefines the tk function, and is
        aliased by winfo_h(). See winfo_x() for details."""
        return self._curr_dim[3] - self._curr_dim[4][1] - self._curr_dim[4][3]
    
    ## Alias for winfo_width.
    winfo_w = winfo_width
    
    ## Alias for winfo_height. 
    winfo_h = winfo_height
       
    def winfo_bx(self):
        """Returns the x coordinate of the widget bounding box topleft corner.
        \note This is not the widget x if you have set a pad for the x; however this
        is the effective x which the library uses for packing widgets horizontally."""
        return self._curr_dim[0]
    
    def winfo_by(self):
        """Returns the y coordinate of the widget bounding box topleft corner.
        See winfo_bx() for details."""        
        return self._curr_dim[1]
    
    def winfo_bw(self):
        """Returns the width of the widget bounding box.
        See winfo_bx() for details"""        
        return self._curr_dim[2]
    
    def winfo_bh(self):
        """Returns the height of the widget bounding box.
        See winfo_bx() for details."""        
        return self._curr_dim[3]
    
    def winfo_bpad(self):
        """Returns the list of the four pad amounts (E-N-W-S) of the widget
        with respect to its bounding box."""
        return self._curr_dim[4]
        


class NtkContainer:
    """Base class for widgets which can contain other widgets.
    Used only as mixin: you should not use it directly."""
    
    def __init__(self):
        """The constructor.        
        It only defines some internal variables used by its methods."""
        self._oldw, self._oldh = self.winfo_w(), self.winfo_h()
        self._cnfchildren = []
    
    def config_children(self, which, **kw):
        """Configures resources for all children.
        All widgets which will be added to the container will be configured
        with the selected values. If a child container calls config_children()
        in turn, the options will be inherited: if a resource receives a new
        value it replaces the previous one, otherwise it remains unchanged.
        \param which you can indicate <b>"all"</b> (or **ALL**) for all children,
        or the name of a widget class (**not** a string, for example NtkEntry or
        NtkButton) or a tuple of names for configuring only specific widgets.
        \param kw a list of named options for the resources to be configured
        \see \ref NtkWindow.py \ref NtkSpinbox.py, \ref NtkRCbuttons.py
        example files"""
        l = [item["which"] for item in self._cnfchildren]
        if which not in l:
            item = {"which":which, "options":kw}
            self._cnfchildren.append(item)
        else:
            self._cnfchildren[l.index(which)]["options"].update(kw)
        
    def _resize_children(self, event=None):
        """Internal function. Resizes all children when the container is resized."""
        #print ("_resize_children() called on", self.__str__())
        if isinstance(self, BaseWindow) and self.winfo_ismapped():
            self._curr_dim = (super().winfo_x(), super().winfo_y(), super().winfo_width(),
                             super().winfo_height(), (0, 0, 0, 0))
        if self._oldw != self.winfo_w() or self._oldh != self.winfo_h() or event is None:
            self._oldw, self._oldh = self.winfo_w(), self.winfo_h()
            for w in self.winfo_children():
                if hasattr(w, "_update_dimensions"):
                    w._update_dimensions()
                    if hasattr(w, "_resize_children"):
                        w._resize_children(event)                    
    


# Added by me to override tkinter Widget methods

class NtkWidget(NtkMisc):
    """Base class which defines methods common for all Ntk internal widgets
    (not windows nor menus). It overrides the tkinter class."""
    def __init__(self, parent, x, y, w, h, pad, ctor, **kw):
        """The constructor."""
        self._orig_dim = (x, y, w, h, pad)      # tk.Widget.__init__ does nothing
        if isinstance(self, NtkCombobox):
            ctor(parent, kw["variable"], kw["values"], kw["command"]) 
        else:
            ctor(self, master=parent, **kw)
        self._calc_dimensions()                 # sets _curr_dim
        self._place_widget()
        if isinstance(parent, (NtkRowFrame, NtkColFrame)): 
            parent.get_active().children.append(self)       
        
    def hide(self):
        """Hides the widget. The widget will not be displayed, but its
        data remain managed; use show() to newly display it."""
        self.place_forget()
    
    def show(self):
        """Shows a previously hidden widget."""        
        self._place_widget()
            
    def visible(self):
        """Returns True if the widget is visible."""
        return self.winfo_ismapped()
    
    def activate(self):
        """Sets the state of the widget to NORMAL.       
        The widget can interact with mouse and keyboard. If the widget
        is a container all its children are set to NORMAL."""
        try:
            self.config(state=NORMAL)
        except (ValueError, tk.TclError):
            pass        
        if isinstance(self, NtkContainer):
            for w in self.winfo_children():
                w.activate()
                
    def deactivate(self):
        """Sets the state of the widget to DISABLED.
        The widget is grayed and cannot interact with mouse and keyboard.
        If the widget is a container all its children are set to DISABLED."""        
        try:
            self.config(state=DISABLED)
        except (ValueError, tk.TclError):
            pass        
        if isinstance(self, NtkContainer):
            for w in self.winfo_children():
                w.deactivate()        
        
    def init_content(self, content):
        """Sets the content type for the widget. The set_content() and
        get_content() methods will behave according to the type chosen
        \param content can be a string, a StringVar or an image (BitmapImage,
        PhotoImage"""
        if isinstance(self, tk.LabelFrame) and isinstance(content, str):
            self.config(text=content)
            self._cont_type = NtkWidget.TEXT
        else:
            if isinstance(content, str):
                self.config(text=content, textvariable="")
                self.textVar = None
                self._cont_type = NtkWidget.TEXT
            elif isinstance(content, tk.StringVar):
                self.config(textvariable=content)
                if content is not self.textVar:
                    self.textVar = content
                self._cont_type = NtkWidget.STRVAR        
            elif isinstance(content, tk.Variable):
                self.config(textvariable=content)
                if content is not self.textVar:
                    self.textVar = content
                self._cont_type = NtkWidget.NUMVAR
            elif isinstance(content, tk.PhotoImage) or isinstance(content, tk.BitmapImage):
                self.config(text="", textvariable="", image=content)
                self.textVar = None
                self._cont_type = NtkWidget.IMAGE
            else:
                self._cont_type = None

    def get_content(self):
        """Returns the content of the widget as a string."""
        if self._cont_type == NtkWidget.STRVAR:
            return self.textVar.get()
        elif self._cont_type == NtkWidget.NUMVAR:
            return str(self.textVar.get())        
        elif  self._cont_type == NtkWidget.TEXT:
            return self.cget("text")
        elif self._cont_type == NtkWidget.IMAGE:
            return self.cget("image")
        else:
            return ""    
    
    def set_content(self, content):
        """Set the content of the widget as a string."""
        if self._cont_type in (NtkWidget.STRVAR, NtkWidget.NUMVAR):
            self.textVar.set(content)
        elif self._cont_type ==NtkWidget.TEXT:
            self.config(text=content)
        elif self._cont_type == NtkWidget.IMAGE:
            self.config(image=content)
    
    def resize(self, x=None, y=None, w=None, h=None, pad=None):
        """Changes the dimensions of the widget. Only the given values are
        updated. Be careful, because if you have packed other widgets with respect to
        this their position will change."""
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
        self.update_idletasks()
        
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
            
        # set some local variables
        if isinstance(self.parent(), NtkRowFrame):                                                 
            parent = self.parent().get_active()
            offs_x, offs_y = 0, parent.winfo_y()
            offs_border = 2 * self.parent().cget("borderwidth")
            parent_w = parent.winfo_w() - offs_border
            parent_h = parent.winfo_h() - offs_border            
        elif isinstance(self.parent(), (NtkColFrame)):                                              
            parent = parent.get_active()
            offs_x, offs_y = parent.winfo_x(), 0
            offs_border = 2 * self.parent().cget("borderwidth")
            parent_w = parent.winfo_w() - offs_border
            parent_h = parent.winfo_h() - offs_border          
        else:
            parent = self.parent()
            offs_x, offs_y = 0, 0
            offs_border = 2 * parent.cget("borderwidth")
            parent_w = parent.winfo_width() - offs_border       # not winfo_W in case root = None
            parent_h = parent.winfo_height() - offs_border      # idem        
        
        # find the last widget from whom calculate coords
        brothers = [w for w in parent.winfo_children() if not isinstance(w, tk.Menu)]
        if self in brothers:                    # we are resizing an already placed widget
            last_wdg = brothers[brothers.index(self) - 1] if brothers.index(self) > 0 else None
        else:                                   # we are placing a new widget
            last_wdg = brothers[-1] if len(brothers) else None
        last_x, last_y = 0, 0
        if isinstance(parent, (NtkHorFrame, _framerow))and last_wdg:
            last_x = last_wdg.winfo_bx() + last_wdg.winfo_bw()
        elif isinstance(parent, (NtkVerFrame, _framecol, NtkMain, NtkWindow)) and last_wdg:
            last_y = last_wdg.winfo_by() + last_wdg.winfo_bh() 
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
                        tempw = round(parent_w * int(tempw[:-1]) / 100)
                    else:
                        raise TypeError
                x = round((parent_w - tempw) / 2)
            elif x.endswith("%"):
                x = round(parent_w * int(x[:-1]) / 100)
        elif x < 0:
            x = parent_w + x
            if x < 0:
                x = 0
        if isinstance(y, str):                  # calculate y
            if y == "pack":
                y = last_y
            elif y == "center":
                temph = h
                if isinstance(temph, str):
                    if temph == "fill":
                        raise ValueError
                    elif temph.endswith("%"):
                        temph = round(parent_h * int(temph[:-1]) / 100)
                    else:
                        raise TypeError
                y = round((parent_h - temph) / 2)            
            elif y.endswith("%"):
                y = round(parent_h * int(y[:-1]) / 100)
        elif y < 0:
            y = parent_h + y
            if y < 0:
                y = 0
        if isinstance(w, str):                  # calculate w
            if w == "fill":
                w = parent_w - x
            elif w.endswith("%"):
                w = round(parent_w * int(w[:-1]) / 100)
            else:
                raise TypeError
        elif w < 0:
            w = parent_w - x + w
            if w < 0:
                w = 1
        if isinstance(h, str):                  # calculate h
            if h == "fill":
                h = parent_h - y
            elif h.endswith("%"):
                h = round(parent_h * int(h[:-1]) / 100)
            else:
                raise TypeError
        elif h < 0:
            h = parent_h - y + h
            if h < 0:
                h = 1 
            
        x += offs_x
        y += offs_y
        self._curr_dim = (x, y, w, h, pad)
        
    def _update_dimensions(self):
        """Internal function.
        Updates widget dimension when their parent is resized."""
        #print("_update_dimensions called on", self.winfo_name())
        self._calc_dimensions()
        if self.winfo_ismapped():
            self._place_widget()         
            
    def _place_widget(self):
        """Internal function.
        Places the widget, once _calc_dimensions() has translated the
        user coordinates into numerical values."""
        self.place_forget()
        x = self.winfo_x()
        y = self.winfo_y()
        w = self.winfo_w()
        h = self.winfo_h()
        self.place(x=x, y=y, width=w, height=h)       
        if isinstance(self, (NtkLabel, NtkCheckbutton, NtkRadiobutton)):
            self.config(wraplength=self._calc_wrap())
        if hasattr(self, "_vscroll"):
            self._auto_yscroll()        
            
    def _auto_yscroll(self):
        """Internal function. Adds or hides a vertical scrollbar if the
        vertical size of the widget changes."""
        if hasattr(self, "_vscroll"):
            self.update_idletasks()             # needed for updating the yview
            offs, size = self.yview()
            if size - offs < 1.0 and not self._vscroll.winfo_ismapped():                
                self._vscroll.pack(side=RIGHT, fill=BOTH)
                self._vscroll.update()              # needed for drawing the scrollbar
            elif size - offs == 1.0 and self._vscroll.winfo_ismapped():
                self._vscroll.pack_forget()
    
    def _get_parent_config(self):
        """Internal function.
        Used for retrieving config options given in config_children()"""
        #cl = "Ntk" + self.winfo_class()
        configured = []
        p = self.parent()
        while p:
            if hasattr(p, "_cnfchildren"):
                for item in p._cnfchildren:
                    wh = item["which"]
                    if ((isinstance(wh, str) and wh == "all") or
                        isinstance(self, wh)):
                        for k, v in item["options"].items():
                            if k not in configured:
                                try:
                                    self.config({k:v})
                                    configured.append(k)
                                except (ValueError, tk.TclError):
                                    #raise
                                    pass
            p = p.master        # not parent() in case root = None 
            
## \cond
    TEXT = 1
    STRVAR = 2
    NUMVAR = 3
    IMAGE = 4
# \endcond

         
# Used by various widgets for calling with command with an event parameter. 
class _setitCommand:
    """Internal class. It wraps the command in widgets which have a command option."""
    
    def __init__(self, widget, callback=None, value=None, variable=None):
        """The constructor.
        \param widget the widget which will generate the call (it will be retrieved as the
        .widget attribute of the generated event)
        \param callback the callback
        \param value an optional value, which will retrieved as the .value attribute of
        the generated event)
        \param variable an IntVar, StringVar, DoubleVar or BooleanVar which will get the
        value when the callback is called"""
        self._widget = widget
        self._callback = callback
        self._value = value
        self._variable = variable
        
    def __call__(self, *cnf):   # some widget (as Scale) send a 2nd argument, which is ignored
        """The call method."""
        if self._variable:
            self._variable.set(self._value)        
        if self._callback:
            ev = tk.Event
            ev.type = tk.EventType.VirtualEvent
            ev.widget = self._widget
            ev.x = self._widget.winfo_pointerx()
            ev.y = self._widget.winfo_pointery()            
            ev.value = self._value
            # print ("_setitCommand.__call__ with callback =", self._callback, "value =", self._value)
            self._callback(ev)



#####################################################################
###################    M A I N   W I N D O W S
#####################################################################

class BaseWindow(NtkMisc, NtkContainer):
    """Base class for both NtkMain and NtkWindow.
    It implements some common methods."""
    
    def __init__(self, x, y, w, h, title=""):
        """Common constructor for NtkMain and NtkWindow. It binds
        the "<Configure>" event to the _resize_children() callback.
        \param x, y, w, h see \ref PLACING_WIDGETS
        \param title the window title"""
        self.geometry("{}x{}+{}+{}".format(w, h, x, y))
        self._curr_dim = (x, y, w, h, (0, 0, 0, 0))
        NtkContainer.__init__(self)
        super().bind("<Configure>", self._resize_children) 
        #self.resizable(width=FALSE, height=FALSE)
        self.title(title)
        # used for onclose()
        self._commandwrap = None
        
    # we must redefine bind() and unbind(): if the user is binding to "<Configure>"
    # event we must mantain the binding to _resize_children
    
    def bind(self, sequence=None, func=None, add=None):
        """Redefines the tkinter.Misc.bind() method for this class. We need
        this for mantainng the binding to the "<Configure>" event with the
        _resize_children() callback."""
        # If sequence has more than one event, they must happen in sequence
        # for the func is triggered. So sequence="<Configure><Enter>" does not
        # affect <Configure>
        if sequence == "<Configure>":
            return super().bind(sequence, func, add=True)
        else:
            return super().bind(sequence, func, add)
               
    def unbind(self, sequence, funcid=None):
        """Redefines the tkinter.Misc.unbind() method for this class. We need
        this for mantainng the binding to the "<Configure>" event with the
        _resize_children() callback."""
        super().unbind(sequence, funcid)
        if sequence == "<Configure>" and not funcid:
            super().bind("<Configure>", self._resize_children)
            
    def onclose(self, command):
        """Defines a callback to call when the window is closed.
        \param command a function of the type func(Event). See
        \ref EVENTS for details."""
        cback, value = ((command, None) if callable(command) else (command[0], command[1]))
        self._commandwrap = _setitCommand(self, cback, value)
        self.protocol("WM_DELETE_WINDOW", self._commandwrap)
            


class NtkMain(BaseWindow, tk.Tk):
    """The main window of the app.
    This is the main window (derived from the tkinter Tk class), and has an associated
    Tcl interpreter, so you cannot execute functions which Tcl calls before constructing
    this. The NtkMain get destroyed only when your program ends.
    
    **Common options** (see \ref ATTRIBUTES)
    
        borderwidth, relief, bcolor, cursor, hbcolor, hfcolor', takefocus
        
    **Less common options**

        class, menu, screen, use, colormap, container, highlightthickness,
        padx, pady, visual
        
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/tk.html">anzeljg reference</a>)
    for the class **tkinter.Tk**"""
    
    def __init__(self, x, y, w, h, title=""):
        """The constructor.
        \param x, y, w, h see \ref PLACING_WIDGETS
        \param title the window title"""           
        tk.Tk.__init__(self)
        BaseWindow.__init__(self, x, y, w, h, title)


                    
class NtkWindow(BaseWindow, tk.Toplevel):
    """A common window (derived from the tkinter Toplevel class) which
    is directly managed by the windows manager.
    You can hide or show it mantaining all the internal widgets states,
    or destroy and re-create it if you want all widgets to be reinitialized.
    You can choose three possible modes for it: **normal**, 
    **modal** or **persistent** (see NtkWindow.__init__())
    
    **Common options** (see \ref ATTRIBUTES)
    
        borderwidth, relief, bcolor, cursor, hbcolor, hfcolor, takefocus
        
    **Less common options** 
        
        class, menu, screen, use, colormap, container, highlightthickness, 
        padx, pady, visual
        
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/toplevel.html">anzeljg reference</a>)
    for the class **tkinter.Toplevel**
    \see \ref NtkWindow.py example file"""
    
    def __init__(self, parent, x, y, w, h, title="", modal=NORMAL):
        """The constructor.
        \param parent you can indicate None or your winMain
        \param x, y, w, h see \ref PLACING_WIDGETS
        \param title the window title
        \param modal one of these three:
        - **"normal"** this is a normal window
        - **"modal"** the window will grab the focus until it is closed, preventing
        to switch to other windows: can be used for dialogs 
        - **"persistent"** the window can lose the focus but will remain
        on top until it is closed."""        
        tk.Toplevel.__init__(self, master=parent)
        BaseWindow.__init__(self, x, y, w, h, title)
        self._modal = modal
        self.show()
            
    def show(self):
        """Shows the window, making it visible."""
        if self._modal == "modal":
            # is it needed? If you set transient cannot reset it
            #self.transient(self.parent())
            self.focus_force() # added
            self.grab_set()      
        elif self._modal == "persistent":
            self.attributes('-topmost', 'true')
        else:
            self.manage(self)
            self.attributes('-topmost', 'false')
        self.deiconify()
            
    def hide(self):
        """Hides the window. It will not be displayed, but its
        data remain managed and the internal widgets state do not chenge;
        use show() to newly display it. If the window was already hidden
        it does nothing."""        
        self.grab_release()
        self.withdraw()
        
    def set_modal(self, modal):
        """Changes the mode of the window, making it normal,
        modal or persistent. This will have effect on the next
        call of show().
        \param modal see __init__()"""
        self._modal = modal
    


#####################################################################
#######################     F R A M E S
#####################################################################

class NtkHorFrame(NtkWidget, NtkContainer, tk.LabelFrame):
    """A container in which you can stack children widgets horizontally.
    This is done by using PACK as the x parameter in their constructor. The
    frame is initialized with the same color of its parent and no border,
    being so invisible. However you can set a border and also a label to be
    shown on it.
    \warning setting a border reduces the space inside the frame
    \see \ref NtkListbox.py, \ref NtkSpinbox.py example files"""
    
    def __init__(self, parent, x, y, w, h, pad=0, content=""):
        """The constructor.
        \param parent the frame parent
        \param x, y, w, h see \ref PLACING_WIDGETS
        \param pad this is ignored, you cannot have a padding on frames
        \param content a string you can put as label"""        
        NtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        if not isinstance(parent, NtkNotebook):
            self.config(background=parent.cget("background"), relief=FLAT)
        NtkContainer.__init__(self)
        self.init_content(content)
 
 
class NtkVerFrame(NtkWidget, NtkContainer, tk.LabelFrame):
    """A container in which you can stack children widgets vertically.
    This is done by using PACK as the y parameter in their constructor. The
    frame is initialized with the same color of its parent and no border,
    being so invisible. However you can set a border and also a label to be
    shown on it.
    \warning setting a border reduces the space inside the frame
    
    See \ref NtkListbox.py, \ref NtkRCbuttons.py, \ref NtkScale.py example files"""
    
    def __init__(self, parent, x, y, w, h, pad=0, content=""):
        """The constructor.
        \param parent the frame parent
        \param x, y, w, h see \ref PLACING_WIDGETS
        \param pad this is ignored, you cannot have a padding on frames
        \param content a string you can put as label"""                        
        NtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        if not isinstance(parent, NtkNotebook):
            self.config(background=parent.cget("background"), relief=FLAT)
        NtkContainer.__init__(self)
        self.init_content(content)
        
        
class _framerow():
    """ Internal class. It represents a row of a NtkRowFrame container, and you
    can pack widgets horizontally inside it."""
    def __init__(self, parent, h):
        """The constructor. It sets some internal variables and calculates the
        row dimensions. When a _framerow is constructed it becomes the active
        row in the parent: widgets created are added to this row
        (see Ntk.NtkRowFrame).
        \param parent the Ntk.NtkRowFrame to which the row belongs
        \param h the height of the row (its width coincides with that of the
        parent; see \ref PLACING_WIDGETS for the various options you have"""
        ## The parent NtkRowFrame
        self.master = parent
        ## The ordinal number of the row (starting from 0)
        self.num = len(parent._rows)
        ## The children widgets
        self.children = []
        self._orig_h = h
        self._tot_h = 0
        self._calc_dimensions()
    
    def parent(self):
        """Returns the parent NtkRowFrame."""
        return self.master
    
    def winfo_children(self):
        """Returns the list of the row children."""
        return self.children

    def winfo_x(self):
        """Returns the x coordinate of the row topleft with respect to parent.
        Actually it is always 0."""
        return 0

    ## The row has no padding, so winfo_bx is the same as winfo_x.
    winfo_bx = winfo_x

    def winfo_y(self):
        """Returns the y coordinate of the row topleft with respect to parent."""
        return self._curr_dim[1]

    ## The row has no padding, so winfo_by is the same as winfo_y.
    winfo_by = winfo_y
    
    def winfo_w(self):
        """Returns the width of the row. Actually it is the same of the parent."""
        return self._curr_dim[2]

    ## The row has no padding, so winfo_bw is the same as winfo_w.
    winfo_bw = winfo_w    

    def winfo_h(self):
        """Returns the height of the row."""
        return self._curr_dim[3]
    
    ## The row has no padding, so winfo_bh is the same as winfo_h.
    winfo_bh = winfo_h
    
    #def winfo_name(self):
        #return "_framerow"
        
    def _calc_dimensions(self):
        """Internal function.
        Translates the coordinates given by the user into numerical values."""        
        n, h = self.num, self._orig_h
        parent = self.parent()
        #parent.update_idletasks()
        if n == len(parent._rows):                  # we are placing a new row
            y = 0 if not len(parent._rows) else parent._rows[-1]._tot_h
        else:                                       # already placed row
            y = 0 if n == 0 else parent._rows[n - 1]._tot_h
        if isinstance(h, str):
            if h.endswith("%"):
                h = round(parent.winfo_h() * int(h[:-1]) / 100)
            elif h == "fill":
                if n == len(parent._rows):
                    h = parent.winfo_h() if not len(parent._rows) else \
                        parent.winfo_h() - parent._rows[-1]._tot_h
                else:
                    h = parent.winfo_h() if n == 0 else \
                        parent.winfo_h() - parent._rows[n - 1]._tot_h
        elif isinstance(h, int):
            if h < 0:
                h = parent.winfo_h() - y + h
                if h < 0:
                    h = 1
        else:
            raise TypeError
        self._curr_dim = (0, y, parent.winfo_w(), h)
        self._tot_h = y + h
        #print(self) 
        
    def _resize_children(self, event):
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
    # TODO: not yet implemented.
    pass



class NtkRowFrame(NtkWidget, NtkContainer, tk.LabelFrame):
    """A container in which you can stack rows vertically.
    Each row behaves like a NtkHorFrame, allowing to stack children
    widgets horizontally (using PACK as the x parameter in their constructor).
    You can add rows to the frame, obtaining thus a disposition similar
    to a matrix. When you add widgets you must indicate the NtkRowFrame
    object (**not** the row) as their parent. The widgets will be added to
    the active row, which is the last constructed or the one set with the
    set_active() method.
    The frame is initialized with the same color of its parent and no border,
    being so invisible. However you can set a border and also a label to be
    shown on it.
    \warning setting a border reduces the space inside the frame
    \see \ref NtkRowFrame.py, \ref NtkCombobox.py \ref NtkWindow.py
    example files"""    
    
    def __init__(self, parent, x, y, w, h, pad=0, content=""):
        """The constructor. The frame has initially no rows, and you must
        add them with the add_row() method.
        \param parent the frame parent
        \param x, y, w, h see \ref PLACING_WIDGETS
        \param pad this is ignored, you cannot have a padding on frames
        \param content a string you can put as label"""
        NtkWidget.__init__(self, parent, x, y, w, h, 0,
                            tk.LabelFrame.__init__)         # pad argument is ignored
        if not isinstance(parent, NtkNotebook):
            self.config(background=parent.cget("background"), relief=FLAT)
        NtkContainer.__init__(self)
        self.init_content(content)
        self._rows = []
        self._active = None
        
    def add_row(self, h):
        """Adds a row to the frame.
        Rows are stacked vertically from top to bottom. This also sets
        the new row as the active one: newly created widgets (which have
        the NtkRowFrame as their parent) will belong to this row.
        \param h the height of the row (the width coincides with the frame one);
        see \ref PLACING_WIDGETS for the various options you have"""
        self._rows.append(_framerow(self, h))
        self._active = self._rows[-1].num
        
    def set_active(self, n):
        """Sets the n-th row as active. Newly created widgets (which have
        the NtkRowFrame as their parent) will belong to this row. When
        you use add_row() the newly created row is automatically set as
        active.
        \param n the row number (starting from 0)"""
        if 0 <= n < len(self._rows):
            self._active = n
            
    def get_active(self):
        """Returns the number of the active row in the frame."""
        if self._active is None:
            raise ValueError
        return self._rows[self._active]
            
    def _resize_children(self, event=None):
        """Internal function. Resizes all children when the container is resized."""
        for row in self._rows:
            row._calc_dimensions()        
            row._resize_children(event)
                    
 

class NtkColFrame(NtkWidget, NtkContainer, tk.LabelFrame):
    # TODO: not yet implemented.
    pass
    #def __init__(self, parent, x, y, w, h, pad=0):
        #NtkWidget.__init__(self, parent, x, y, w, h, 0,
                            #tk.LabelFrame.__init__)         # pad argument is ignored
        #self.config(background=parent.cget("background"), relief=FLAT)
        #NtkContainer.__init__(self)
        #self._cols = []
        #self._active = None
        
    #def add_col(self, h):
        #self._cols.append(_framerow(self, h))
        #self._active = self._cols[-1]
        
    #def set_active(self, n):
        #if 0 <= n < len(self._cols):
            #self._active = n
      
            

#####################################################################
############       tkinter WIDGETS SUPERCLASSES
#####################################################################     



class NtkButton(NtkWidget, tk.Button):
    """Button widget. You can set its content to a text, an image or
    a bitmap, and can associate a callback to its pressure in the
    constructor or with the command option in Ntk.Misc.config().
    
    **Common options** (see \ref ATTRIBUTES)
    
          abcolor, afcolor, anchor, bcolor, borderwidth, command, cursor, dfcolor, font,
          fcolor, hbcolor, hborder, hfcolor, justify, relief, state, takefocus, text,
          textvariable, wraplength
    
    **Less common options** 
    
          bitmap, compound, default, overrelief, image, padx, pady, repeatdelay,
          repeatinterval, underline
          
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/button.html">anzeljg reference</a>
    for the class **tkinter.Button**"""
    
    #Button widget.
    #STANDARD OPTIONS

        #activebackground, activeforeground, anchor,
        #background, bitmap, borderwidth, cursor,
        #disabledforeground, font, foreground
        #highlightbackground, highlightcolor,
        #highlightthickness, image, justify,
        #padx, pady, relief, repeatdelay,
        #repeatinterval, takefocus, text,
        #textvariable, underline, wraplength

    #WIDGET-SPECIFIC OPTIONS

        #command, compound, default, height,
        #overrelief, state, width   
    def __init__(self, parent, x, y, w, h, pad=0, content="", command=None):
        """The constructor. You can specify here the initial content of the button
        and a callback to associate to its pressure.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param content the button label; here you can specify
         + a string
         + a StringVar (which automatically updates the label when changed)
         + a BitmapImage or PhotoImage objects
        \param command see \ref EVENTS"""         
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Button.__init__)
        self.config(anchor=CENTER, justify=LEFT)
        self._get_parent_config()
        self.textVar = None
        self.init_content(content)
        self._commandwrap = None
        if command:
            self.config(command=command)
            
     

class NtkCanvas(tk.Canvas):
    """Canvas widget to display graphical elements like lines or text. This widget
    is unchanged from tkinter (except for the constructor).

    **Common options** (see \ref ATTRIBUTES)

         bcolor, borderwidth, cursor, hbcolor, hborder, hcolor, ibcolor, relief, sbcolor,
         sfcolor, state, takefocus

    **Less common options** 

         closeenough, confine, insertborderwidth, insertofftime, insertontime,
         insertwidth, offset, scrollregion, selectborderwidth, state,
         xscrollcommand, xscrollincrement, yscrollcommand, yscrollincrement.

    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas.html">anzeljg reference</a>
    for the class **tkinter.Canvas**."""

    #Valid resource names: background, bd, bg, borderwidth, closeenough,
    #confine, cursor, height, highlightbackground, highlightcolor,
    #highlightthickness, insertbackground, insertborderwidth,
    #insertofftime, insertontime, insertwidth, offset, relief,
    #scrollregion, selectbackground, selectborderwidth, selectforeground,
    #state, takefocus, width, xscrollcommand, xscrollincrement,
    #yscrollcommand, yscrollincrement.
    #def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):

    def __init__(self, parent, x, y, w, h, pad=0):
        """The constructor. You can specify here the initial content of the canvas.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS"""           
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Canvas.__init__)
        #self.config(anchor=W, justify=LEFT, wraplength=self._calc_wrap())
        self._get_parent_config()
        


class NtkCheckbutton(NtkWidget, tk.Checkbutton):
    """ Checkbutton widget which is either in on or off state.
    You can associate a variable to its states and a callback to
    be called when the state of the button changes.
    
    **Common options** (see \ref ATTRIBUTES)
    
          abcolor, afcolor, anchor, bcolor, borderwidth, command, cursor,
          dfcolor, font, fcolor, hbcolor, hborder, hfcolor, justify, relief,
          scolor, state, takefocus, text, textvariable, variable, wraplength   
    
    **Less common options**
    
          bitmap, image, indicatoron, offvalue, onvalue, padx, pady,
          selectimage, underline
          
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/checkbutton.html">anzeljg reference</a>
    for the class **tkinter.Checkbutton**.
    \see \ref NtkRCbuttons.py example file"""
    
    #Valid resource names: activebackground, activeforeground, anchor,
    #background, bd, bg, bitmap, borderwidth, command, cursor,
    #disabledforeground, fg, font, foreground, height,
    #highlightbackground, highlightcolor, highlightthickness, image,
    #indicatoron, justify, offvalue, onvalue, padx, pady, relief,
    #selectcolor, selectimage, state, takefocus, text, textvariable,
    #underline, variable, width, wraplength."""    
    #def __init__(self, parent, x, y, w, h, content=None, padx=0, pady=0):
    
    def __init__(self, parent, x, y, w, h, pad=0, content="", variable=None, command=None):
        """The constructor. You can specify here the label of the button, a Variable object
        which will be updated at state change and a callback to associate to status change.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param content the button label; here you can specify
         + a string
         + a StringVar (which automatically updates the button label when changed)
         + a **tkinter.BitmapImage** or **tkinter.PhotoImage** objects
        \param variable the Variable object whose value is associated with the button
        states; here you can specify:
         + None: an IntVar is automatically created and values 0 and 1 associated; you can
         get the button status with the get_value() method
         + a Variable object which will get the values 1 (or "1" if StringVar) for
         on and 0 ("0") for off
         + a triple (_variable_, _onvalue_, _offvalue_) specifying the variable, its value
         for on and its value for off
        \param command see \ref EVENTS"""           
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Checkbutton.__init__)
        self.config(anchor=W, justify=LEFT, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.textVar=None
        self.init_content(content)
        if variable:
            if isinstance(variable, (tuple, list)) and len(variable) == 3 and \
               isinstance(variable[0], tk.Variable):
                self.config(variable=variable[0], onvalue=variable[1], offvalue=variable[2])
                self.valueVar = variable
            elif isinstance(variable, tk.Variable):
                self.config(variable=variable)
                if isinstance(variable, StringVar):
                    self.config(onvalue="1", offvalue="0")
                else:
                    self.config(onvalue=1, offvalue=0)
                self.valueVar = variable
        else:
            self.valueVar = IntVar()
            self.config(variable=self.valueVar, onvalue=1, offvalue=0)
        self._commandwrap = None
        if command:
            self.config(command=command)
            
    #def deselect(self):
        #"""Put the button in off-state."""
        #self.tk.call(self._w, 'deselect')

    #def flash(self):
        #"""Flash the button."""
        #self.tk.call(self._w, 'flash')

    #def invoke(self):
        #"""Toggle the button and invoke a command if given as resource."""
        #return self.tk.call(self._w, 'invoke')

    #def select(self):
        #"""Put the button in on-state."""
        #self.tk.call(self._w, 'select')
            
    def set_variable(self, variable=None, offvalue=None, onvalue=None):
        """Sets the associated tkinter.Variable object and its values when
        the button is in off and on state. Only the given values are changed.
        You should do this in the constructor so you need this only if you want
        to change them later."""
        if variable:
            self.config(index, variable=variable)
            self.valueVar = variable
        if offvalue:
            self.entry_config(index, offvalue=offvalue)
        if onvalue:
            self.entry_config(index, onvalue=onvalue)  
        
    def get_value(self):
        """Returns the actual value associated to the button state.
        \note for this class the get_content() method returns the button
        label, NOT the button status value"""
        return self.valueVar.get()
    
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        """Internal function. It calculates the text wraplength when the widget
        is resized."""         
        return 0 if self.cget("wraplen") == 0 else self.winfo_w() - 20
    
    
# No more used by NtkCombobox. 
#class _setitCombobox:
    #"""Internal class. It wraps the command in the widget OptionMenu."""
    #def __init__(self, var, value, callback=None):
        #self.__value = value
        #self.__var = var
        #self.__callback = callback
    #def __call__(self, *args):
        #self.__var.set(self.__value)
        #if self.__callback:
            #self.__callback(self.__value, *args)
            ##self.__callback(*args)

class NtkCombobox(NtkWidget, tk.OptionMenu):
    """Combobox which allows the user to select a value from a menu.
    It is the equivalent (renamed) of the OptionMenu class in tkinter
       
    **Common options** (see \ref ATTRIBUTES)
    
        abcolor, afcolor, bcolor, borderwidth, cursor, dfcolor, font,
        fcolor, relief, scolor, state, takefocus.
        
    **Less common options**
    
        activeborderwidth, postcommand, tearoff, tearoffcommand, title, type.
        
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/optionmenu.html">anzeljg reference</a>
    for the class **tkinter.OptionMenu**
    \see \ref NtkCombobox.py \ref NtkMenu example files"""
    
    def __init__(self, parent, x, y, w, h, pad=0, items=[], variable=None, command=None):
        """The constructor. You can specify here the label of the button, a Variable object
        which will be updated when the state change and a callback to associate to state change.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param items a list of strings for the menu options
        \param variable a StringVar which is automatically updated at every menu choice;
        if you leave None a StringVar is automatically created. A <<ChangedVar>>
        event is generated when its value changes
        \param command see \ref EVENTS""" 
        
        # NOTE: the Menuoption constructor is different from all others, so I must
        # adopt this strange structure copying and modifying the original tkinter
        # constructor hera as _init1_()
        
        # MUST be here, so it initializes master if None
        tk.Widget.__init__(self, parent, "menubutton")
        self.textVar = tk.StringVar() if not variable else variable 
        self.textVar.trace("w", lambda *args: self.event_generate("<<ChangedVar>>"))
        NtkWidget.__init__(self, parent, x, y, w, h, pad, self._init1_, variable=self.textVar,
                            values=items, command=command)
        self._get_parent_config()
        self._commandwrap = _setitCommand(self, command)
    
    def _init1_(self, master, variable, values, command, **kw):
        """Helper function for the constructor."""
        kw = {"borderwidth": 2, "textvariable": variable,
              "indicatoron": 1, "relief": RAISED, "anchor": "c",
              "highlightthickness": 2}
        self.config(kw)
        self.widgetName = 'tk_optionMenu'
        menu = self.__menu = NtkMenu(self)
        self.menuname = menu._w
        self._cont_type = NtkWidget.STRVAR
        # we need to remember the callback if we want to add new entries later
        self.callback = None
        if command:
            self.callback, value = ((command, None) if callable(command) else (command[0], command[1]))
            # value is ignored
        for v in values:
            menu.add_command(label=v, command=_setitCommand(self, self.callback, v, variable))
        self["menu"] = menu             # I don't know why
        variable.set(values[0] if len(values) else "")
        
    def get_menu(self):
        """Returns the internal NtkMenu object. You can then
        apply to it the NtkMenu methods."""
        return self.__menu
    
    def get_item(self, index):
        """Returns the label of a menu item.
        \param index an int (starting from 0); if the index is
        greater than the menu length the last element is returned; if 
        the menu is empty an empty string is returned."""
        return self.__menu.entrycget(index, "label") if self.__menu.size() > 0 else ""
    
    def get_items(self):
        """Returns a tuple of strings with all menu labels."""
        lst = []
        for i in range(self.__menu.len()):
            lst.append(self.__menu.entrycget(i, "label"))
        return tuple(lst)
    
    def set_content(self, index, invoke=True):
        """Selects a menu item.
        \param index here you can specify:
         + an int (starting from 0): the corresponding item will become the selected
         one; if the index is greater than the menu length the last element is selected
         + an empty string: this deselects all items
         + one of the menu items strings: this will become the selected item; if the
        string is not in the menu the selection remains unchanged 
        \param invoke if True the associated callback will be executed"""
        if isinstance(index, int):
            text = self.__menu.entrycget(index, "label")
            self.textVar.set(text)
            if invoke:
                self.invoke(text)
        else:
            if len(index):
                ind = self.index(index)
                if ind != None:
                    self.textVar.set(index)
                    if invoke:
                        self.invoke(index)
            else:
                self.textVar.set("")
            
        
    # TODO activate_entry and deactivate_entry ?        
    #def activate(self, index):
        #"""Activate entry at INDEX."""
        #self.tk.call(self._w, 'activate', index)
        
    def add(self, *items):
        """Appends one or more items to the list of options.
        \param *items one or more strings (the item labels) to be
        appended"""
        for item in items:
            self.__menu.add_command(label=item,
                command=_setitCommand(self, self.callback, item, self.textVar))
        
    def insert(self, index, *items):
        """Inserts one or more items to the list of options at a given
        position.
        \param index the insert position; it can be an int (beginning from 0)
        or a string already in the options list (items will be inserted BEFORE it)
        \param *items one or more strings (the item labels) to be
        inserted"""
        if isinstance(index, str):
            index = self.__menu.index(index)
        for i in range(len(items)):
            item = items[i]
            self.__menu.insert_command(index + i, label=item,
                command=_setitCommand(self, self.callback, item, self.textVar))
    
    def delete(self, index1, index2=None):
        """Deletes menu items between index1 and index2 (included).
        \param index1, index2 the first and last items to be deleted;
        if you leave _index2_ = None only _index1_ will be deleted. These
        can be integers or strings already in the options list
        \note be careful: if you specify two strings ALL items between
        them will be deleted"""
        self.__menu.delete(index1, index2)
    
    def get_config_item(self, index, option):
        """Returns the resource value of a menu item. It is aliased by
        entry_get_config().
        \param index you can specify an int (the menu item index) or
        a string (the label of the item)
        \param option the option we want to know (as a string)"""
        if option in NtkMisc._trans_opt:
            option = NtkMisc._trans_opt["option"]        
        return self.__menu.tk.call(self["menu"]._w, 'entrycget', index, '-' + option)
    
    def config_item(self, index, cnf=None, **kw):
        """Configures a menu item. It is aliased by entry_config().
        \param index you can specify an int (the menu item index) or
        a string (the label of the item)
        \param cnf, **kw the options"""
        trans_kw = {}
        if isinstance(cnf, dict):
            for k, v in cnf.items():
                if k in NtkMisc._trans_opt:
                    trans_kw[NtkMisc._trans_opt[k]] = v
                else:
                    trans_kw[k] = v        
        for k, v in kw.items():
            if k in NtkMisc._trans_opt:
                trans_kw[NtkMisc._trans_opt[k]] = v
            else:
                trans_kw[k] = v        
        return self.__menu._configure(('entryconfigure', index), {}, **trans_kw)
    
    def index(self, index):
        """Returns the index of a menu item. If the item is
        not in the  mnenu returns None.
        \param index a string (the label of the menu item)"""
        i = self.__menu.tk.call(self.__menu._w, 'index', index)
        if i == 'none': return None
        return self.__menu.tk.getint(i)
    
    def invoke(self, index):
        """Invokes the given menu item and executes
        the associated command.
        \param index you can specify an int (the menu item index) or
        a string (the label of the item)."""
        return self.__menu.tk.call(self.__menu._w, 'invoke', index)



class NtkEntry(NtkWidget, tk.Entry):
    """Entry widget which allows displaying simple text.

    **Common options** (see \ref ATTRIBUTES)
    
         bcolor, borderwidth, cursor, font, fcolor, hbcolor, hborder,
         hfcolor, ibcolor, justify, relief, sbcolor, sfcolor, state,
         takefocus, textvariable

    **Less common options** 
   
         exportselection, insertborderwidth, insertofftime, insertontime,
         insertwidth, invalidcommand, selectborderwidth, show, validate,
         validatecommand, xscrollcommand.

    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry.html">anzeljg reference</a>
    for the class **tkinter.Entry**
    \see \ref NtkEntry.py example file"""
        
    #Valid resource names: background, bd, bg, borderwidth, cursor,
    #exportselection, fg, font, foreground, highlightbackground,
    #highlightcolor, highlightthickness, insertbackground,
    #insertborderwidth, insertofftime, insertontime, insertwidth,
    #invalidcommand, invcmd, justify, relief, selectbackground,
    #selectborderwidth, selectforeground, show, state, takefocus,
    #textvariable, validate, validatecommand, vcmd, width,
    #xscrollcommand."""
        
    def __init__(self, parent, x, y, w, h, pad=0, content="", command=None):
        """The constructor. You can specify here the initial content of the entry
        and a callback to associate with the Return. Moreover, every time you modify
        the entry string a <<ChangedVar>> event is generated, which you can bind
        to a callback.
        \param self the object instance
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param content the initial text of the entry. Here you can specify
         + a string: an internal StringVar is created
         + a StringVar: this become the associated StringVar
        \param command see \ref EVENTS"""           
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Entry.__init__)
        self._get_parent_config()
        self.textVar = tk.StringVar(value=content) if isinstance(content, str) else content
        self.init_content(self.textVar)
        self.textVar.trace("w", lambda *args: self.event_generate("<<ChangedVar>>"))
        self._commandwrap = None
        if command:
            self.config(command=command)
            
    def config(self, cnf=None, **kw):
        """Configures resources of a widget.
        We need to redefine this for this class. See
        Ntk.NtkWidget.config()."""
        
        if isinstance(cnf, dict):
            cnf.update(kw)
        elif cnf is None and kw:
            cnf = kw        
        if "command" in cnf.keys():
            cmd = cnf.pop("command")
            cback, value = ((cmd, None) if callable(cmd) else (cmd[0], cmd[1]))
            # _commandwrap is the  __call__ wrapper for the command callback
            self._commandwrap = _setitCommand(self, cback, value)
            self.bind("<Return>", self._commandwrap)            
        super().config(cnf)
    
    def get_config(self, key):
        """Returns the value for the _key_ resource.
        We need to redefine this for this class. See
        Ntk.NtkWidget.get_config()."""
        if key == "command":
            return _commandwrap
        return self.cget(key)    

# class Frame substituted by NtkHorFrame, NtkVerFrame   
    
class NtkLabel(NtkWidget, tk.Label):
    """Label widget which can display text and bitmaps.

    **Common options** (see \ref ATTRIBUTES)

         abcolor, afcolor, anchor, bcolor, borderwidth, cursor, dfcolor,
         font, fcolor, hbcolor, hborder, hfcolor, justify, relief,
         takefocus, state, text, textvariable, wraplength

    **Less common options** 

         bitmap, image, padx, pady, underline
   
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/label.html">anzeljg reference</a>
    for the class **tkinter.Label**."""

       #STANDARD OPTIONS

            #activebackground, activeforeground, anchor,
            #background, bitmap, borderwidth, cursor,
            #disabledforeground, font, foreground,
            #highlightbackground, highlightcolor,
            #highlightthickness, image, justify,
            #padx, pady, relief, takefocus, text,
            #textvariable, underline, wraplength

       #WIDGET-SPECIFIC OPTIONS

            #height, state, width

    def __init__(self, parent, x, y, w, h, pad=0, content=""):
        """The constructor. You can specify here the initial content of the label.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param content the label content; here you can specify
         + a string
         + a tkinter.Variable object (which automatically updates the label when
         changed)
         + a BitmapImage or PhotoImage objects"""
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Label.__init__)
        self.config(anchor=W, justify=LEFT, relief=SUNKEN, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.textVar = None
        self.init_content(content)
        
    def _calc_wrap(self):               # Used to calculate text wraplength when resized
        """Internal function. It calculates the text wraplength when the widget
        is resized.""" 
        return 0 if self.cget("wraplen") == 0 else self.winfo_w() - 1  
        
    
class NtkListbox(NtkWidget, tk.Listbox):
    """Listbox widget which can display a list of strings. It allows you to choose one
    or more of them and to associate a callback to the choice event. Moreover it adds
    and removes automatically a vertical scrollbar if the list becomes larger than the
    widget height.

    **Common options** (see \ref ATTRIBUTES)

         bcolor, borderwidth, cursor, font, fcolor, hbcolor, hborder, hfcolor, 
         relief, sbcolor, sfcolor, state, takefocus

    **Less common options** 

         exportselection, selectborderwidth, selectmode,
         setgrid, xscrollcommand, yscrollcommand, listvariable

    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/listbox.html">anzeljg reference</a>
    for the class **tkinter.Listbox**
    \note This widget doesn't have an associated **tkinter.Variable** object,
    because it has multiple selection modes, and some of them can return lists
    of strings (see selection_mode() and get_selection_mode()). If you want to
    know what is selected use the get_selected() method (which always returns
    a tuple, eventually empty).
    \see \ref NtkListbox.py example file """

        #Valid resource names: background, bd, bg, borderwidth, cursor,
        #exportselection, fg, font, foreground, height, highlightbackground,
        #highlightcolor, highlightthickness, relief, selectbackground,
        #selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
        #width, xscrollcommand, yscrollcommand, listvariable."""

    def __init__(self, parent, x, y, w, h, pad=0, items=[], command=None):
        """The constructor. You can specify here the initial item list of the
        listbox and a callback to associate to the choice of an item.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param items you can specify here the list of items as strings
        \param command see \ref EVENTS"""           
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Listbox.__init__)
        self.config(justify=LEFT, activestyle="none", exportselection=False)
        self._get_parent_config()
        self._vscroll = tk.Scrollbar(self, orient=VERTICAL)
        self.config(yscrollcommand=self._vscroll.set)
        self._vscroll.config(command=self.yview)
        # get_content returns an empty string
        self.init_content(None)
        for i in items:
            self.add(i)        
        # this doesn't need _commandwrap
        if command:
            self.config(command=command)
        
    def config(self, cnf=None, **kw):
        """Configures resources of the widget.
        We need to redefine this for this class. See
        Ntk.NtkWidget.config()."""
        
        if isinstance(cnf, dict):
            cnf.update(kw)
        elif cnf is None and kw:
            cnf = kw        
        if "command" in cnf.keys():
            cmd = cnf.pop("command")
            cback, value = ((cmd, None) if callable(cmd) else (cmd[0], cmd[1]))
            # _commandwrap is the  __call__ wrapper for the command callback
            self._commandwrap = _setitCommand(self, cback, value)
            self.bind("<<ListboxSelect>>", self._commandwrap)
        if "selectmode" in cnf.keys():
            self.set_select_mode(cnf.pop("selectmode"))
        super().config(cnf)
    
    def get_config(self, key):
        """Returns the value for the _key_ resource.
        We need to redefine this for this class. See
        Ntk.NtkWidget.get_config()."""
        if key == "command":
            return _commandwrap
        return self.cget(key)    
    
    def get_item(self, index):
        """Returns the text of a menu item as a string.
        \param index an int (starting from 0); if the index is
        greater than the  length the last element is returned; if 
        the menu is empty an empty string is returned."""
        if index >= self.size():
            index = "end"
        return self.get(index)
     
    def get_items(self):
        """Returns a tuple of strings with all list items."""
        return self.get(0, END)       
                
    def add(self, *items):
        """Appends one or more items to the item list.
        It is equivalent to insert(self, END, *items)
        \param *items one or more strings"""
        #self.update()
        tk.Listbox.insert(self, END, *items)
        self._auto_yscroll()
        self.see(END)      
      
    def insert(self, index, *items):
        """Inserts one or more items at the given index.
        \param index the insert position; it can be
         + an int (beginning from 0, if the int is greater than the list size
         it becomes the end of the list)
         + a string already in the options list (items will be inserted BEFORE it)
         + one of the constants "active", "anchor", "end"
        \param *items one or more strings (the item labels) to be
        inserted"""    
        index = self.index(index)
        tk.Listbox.insert(self, index, *items)
        self._auto_yscroll()
        self.see(index)
            
    def delete(self, index1, index2=None):
        """Deletes the items between index1 and index2 (included).
        \param index1, index2 the first and last items to be deleted;
        if you leave _index2_ = None only _index1_ will be deleted.
        see insert()
        \note be careful: if you specify two strings ALL items between
        them will be deleted"""        
        index1 = self.index(index1)
        if index2 != None:
            index2 = self.index(index2)
        tk.Listbox.delete(self, index1, index2)
        self._auto_yscroll()
        
    def index(self, ind):
        """Returns the index of a menu item. If the item is
        not in the  mnenu returns None.
        \param ind a string (the label of the menu item), or one of the
        constants "active", "anchor", "end" """
        if isinstance(ind, str) and ind not in ("active", "anchor", "end"):
            return self.get(0, END).index(ind)
        elif isinstance(ind, int) and ind >= self.size():
            ind = "end"
        i = self.tk.call(self._w, 'index', ind)
        if i == 'none': return None
        return self.tk.getint(i)    
                
    def select(self, item):
        """Selects one or more items.
        \param item can be
         + an int (the index of the selected element starting from 0)
         + a string already in the list
         + one of the constants "active", "anchor", "end"
         + a tuple of previous ones. In this case the items
        are selected only if the select mode is "multiple" or
        "extended" """
        if isinstance(item, (int, str)):
            item = self.index(item)
            self.select_set(item)
            self.event_generate("<<ListboxSelect>>")
        elif (isinstance(item, (tuple, list)) and
             self.get_config("selectmode") in ("multiple", "extended")):
            self.selection_clear(0)
            for i in item:
                ind = self.index(i)
                self.select_set(ind)
                self.event_generate("<<ListboxSelect>>")
          
    ## Returns a tuple of int (the indexes of selected element). Returns an
    # empty tuple if no element is selected."""
    get_selected = tk.Listbox.curselection
    #return (() if self.curselection() == "" else self.curselection())
            
    def set_select_mode(self, mode):
        """Sets the listbox select mode.
        \param mode here you can specify
         + "single": the user can select only one item at once, clicking
         on it in the listbox"
         + "browse": the user can select only one item at once, clicking
         on it or dragging with the mouse
         + "multiple": the user can select multiple items, clicking on them;
         clicking on a selected item unselects it"
         + "extended": the user can select multiple items, clicking, dragging
         the mouse and using the <CTRL> or <SHIFT> keys"""
        self.selection_clear(0, END)
        super().config(selectmode=mode)
        
    def get_select_mode(self):
        """Gets the listbox select mode. See set_select_mode()."""
        return self.cget("selectmode")
    
    def see(self, index):
        """Scroll such that _index_ is visible.
        \param index see insert()"""
        index = self.index(index)
        self.tk.call(self._w, 'see', index)

    def selection_anchor(self, index):
        """Set the fixed end of the selection.
        \param index see insert()"""
        index = self.index(index)
        self.tk.call(self._w, 'selection', 'anchor', index)

    def selection_clear(self, index1, index2=None):
        """Clear the selection from _index1_ to _index2_.
        See delete()"""
        index1 = self.index(index1)
        if index2 != None:
            index2 = self.index(index2)
        self.tk.call(self._w,
                 'selection', 'clear', index1, index2) 


### UNUSED ??? ###
# Used by NtkMenu
#class _setitMenu:
    #"""Internal class. It wraps the command in the widget Menu."""
    #def __init__(self, value, callback=None):
        #self.__value = value
        #self.__callback = callback
    #def __call__(self, *args):
        #if self.__callback:
            #self.__callback(self.__value, *args)
            ##self.__callback(*args)     
        
class NtkMenu(NtkMisc, tk.Menu):
    """Menu widget which allows displaying menu bars, pull-down menus and pop-up menus.
    
    **Common options** (see \ref ATTRIBUTES)
    
          abcolor, afcolor, bcolor, borderwidth, cursor, dfcolor, font, fcolor, relief,
          sfcolor, takefocus
    
    **Less common options**
    
          activeborderwidth, postcommand, tearoff, tearoffcommand, title, type
    
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/menu.html">anzeljg reference</a>
    for the class **tkinter.Menu**
    \see \ref NtkMenu.py example file"""
        
        #Valid resource names: activebackground, activeborderwidth,
        #activeforeground, background, bd, bg, borderwidth, cursor,
        #disabledforeground, fg, font, foreground, postcommand, relief,
        #selectcolor, takefocus, tearoff, tearoffcommand, title, type."""
        
    def __init__(self, parent, label=None, popup=False):
        """The constructor. It creates an empty menu, and you can add to it
        commands, checkbuttons, radiobuttons and separators.
        \param parent the menu parent; if it is an instance of NtkMenu this menu will be
        added to it as a cascade, if it is a window this is set as its menubar  (but see
        below)
        \param label the menu text
        \param popup if True this is a popup menu, and will not be added to its parent
        """          
        tk.Menu.__init__(self, parent, tearoff=0)
        if isinstance(parent, NtkMenu):
            parent.add_cascade(label=label, menu=self)
        elif isinstance(parent, (NtkMain, NtkWindow)) and not popup:
            parent.config(menu=self)
        self._len = 0

    def add(self, itemType, cnf={}, **kw):
        """Appends an item to the menu. It overrides tkinter method. You,
        however, can continue to use add_command(), add_checkbutton(),
        add_radiobutton() and add_separator() (see the
        <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/menu.html">tkinter reference</a>)."""
        if "command" in cnf.keys():
            cmd = cnf["command"]
            cback, value = ((cmd, None) if callable(cmd) else (cmd[0], cmd[1]))
            self._commandwrap = _setitCommand(self, cback, value)                  
            cnf.update({"command":self._commandwrap})        
        self.tk.call((self._w, 'add', itemType) + self._options(cnf, kw))
        self._len += 1
        
        
    def insert(self, index, itemType, cnf={}, **kw):
        """Inserts an item in the menu at the given index (starting from 0).
        It overrides tkinter method. You, however, can continue to use
        insert_command(), insert_checkbutton(), insert_radiobutton() and
        insert_separator() (see the
        <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/menu.html">tkinter reference</a>)."""
        if "command" in cnf.keys():
            cmd = cnf["command"]
            cback, value = ((cmd, None) if callable(cmd) else (cmd[0], cmd[1]))
            self._commandwrap = _setitCommand(self, cback, value)
            cnf.update({"command":self._commandwrap})        
        self.tk.call((self._w, 'insert', index, itemType) + self._options(cnf, kw))
        self._len += 1
        
    def delete(self, index1, index2=None):
        """Deletes menu items between _index1_ and _index2_ (included)."""
        if index2 is None:
            index2 = index1

        num_index1, num_index2 = self.index(index1), self.index(index2)
        if (num_index1 is None) or (num_index2 is None):
            num_index1, num_index2 = 0, -1

        for i in range(num_index1, num_index2 + 1):
            if 'command' in self.entry_config(i):
                c = str(self.entrycget(i, 'command'))
                if c:
                    self.deletecommand(c)
            self._len -= 1
        self.tk.call(self._w, 'delete', index1, index2)    
        
    def entry_get_config(self, index, option):
        # This is an alias for entrycget()
        """Returns the resource value of a menu item.
        \param index the item index as an int (starting from 0)
        \param option the option we wantto know as a string"""
        if option in NtkMisc._trans_opt:
            option = NtkMisc._trans_opt["option"]
        return self.tk.call(self._w, 'entrycget', index, '-' + option)
    
    def entry_config(self, index, cnf=None, **kw):
        # This is an alias for entryconfigure().
        """Configures a menu item at _index_."""      
        trans_kw = {}
        if isinstance(cnf, dict):
            for k, v in cnf.items():
                if k in NtkMisc._trans_opt:
                    trans_kw[_trans_opt[k]] = v
                else:
                    trans_kw[k] = v        
        for k, v in kw.items():
            if k in NtkMisc._trans_opt:
                trans_kw[NtkMisc._trans_opt[k]] = v
            else:
                trans_kw[k] = v        
        return self._configure(('entryconfigure', index), None, trans_kw)
    
    def entry_set_variable(self, index, variable=None, offvalue=None, onvalue=None):
        """Sets a variable for the menu at _index_. It is useful only for
        checkbutton items."""
        if variable:
            self.entry_config(index, variable=variable)
        if offvalue:
            self.entry_config(index, offvalue=offvalue)
        if onvalue:
            self.entry_config(index, onvalue=onvalue)
    
    def size(self):
        """Returns the number of elements in the items list."""
        return self._len
    
    #def clear(self):
        #while self.index(1) == 1:
            #self.delete(1)
            
    
# MenuButton and Message obsolete in tkinter


class NtkRadiobutton(NtkWidget, tk.Radiobutton):
    """Radiobutton widget which shows only one of several buttons in on-state.
    If you want a group of mutually exclusive radiobuttons you must associate
    to them (in the constructor or by the set_variable() method) the same
    Variable object (only StringVar and IntVar are admitted), setting a 
    different value for every button, so you can know which button is pressed
    by the variable get() method (so the radiobutton has no get_value() method).

    **Common options** (see \ref ATTRIBUTES)

         abcolor, afcolor, anchor, bcolor, borderwidth, command, cursor,
         dfcolor, font, fcolor, hbcolor, hborder, hfcolor, justify, relief,
         scolor, state, takefocus, text, textvariable, wraplength

    **Less common options** 

         bitmap, image, indicatoron, padx, pady, selectimage,
         underline, value, variable
         
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/listbox.html">anzeljg reference</a>
    for the class **tkinter.Radiobutton**
    \see \ref NtkRCbuttons.py example file""" 

        #Valid resource names: activebackground, activeforeground, anchor,
        #background, bd, bg, bitmap, borderwidth, command, cursor,
        #disabledforeground, fg, font, foreground, height,
        #highlightbackground, highlightcolor, highlightthickness, image,
        #indicatoron, justify, padx, pady, relief, selectcolor, selectimage,
        #state, takefocus, text, textvariable, underline, value, variable,
        #width, wraplength."""
        
    def __init__(self, parent, x, y, w, h, pad=0, content=None, variable=None, command=None):
        """The constructor. You can specify here the label of the button, a Variable object
        which will be updated at state change and a callback to associate to status change.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param content the button label; here you can specify
         + a string
         + a StringVar (which automatically updates the button label when changed)
         + a **tkinter.BitmapImage** or **tkinter.PhotoImage** objects
        \param variable the Variable object whose value is associated with the button
        state; you should specify a duple (_variable_, _value_): the variable (an IntVar o
        StringVar shared with other radiobuttons of the same mutually exclusive group) and its
        value when the button is on (different for every button of the group). If you don't
        give here this parameters you can set it later with the set_variable() method (otherwise
        the button won't be mutually exclusive with others).
        \param command see \ref EVENTS"""         
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Radiobutton.__init__)
        self.config(anchor=W, justify=LEFT, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.init_content(content)
        if variable:
            if isinstance(variable, (tuple, list)) and len(variable) == 2:
                self.config(variable=variable[0], value=variable[1])
            else:
                self.config(variable=variable)        
        self._commandwrap = None
        if command:
            self.config(command=command)
            
    def set_variable(self, variable=None, value=None):
        """Sets the associated tkinter.Variable object and its value when
        the button is on. Only the given values are changed.
        You should do this in the constructor so you need this only if you want
        to change them later."""        
        if variable:
            self.config(variable=variable)
        if value:
            self.config(value=value)  
        
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        """Internal function. It calculates the text wraplength when the widget
        is resized."""          
        return 0 if self.cget("wraplen") == 0 else self.winfo_w() - 20

    

class NtkScale(NtkWidget, tk.Scale):
    """Scale widget which can display a numerical scale.
    You can associate an InTVar or DoubleVar to its state and a callback to
    be called when the state of the scale changes.
    
    **Common options** (see \ref ATTRIBUTES)
    
          abcolor, bcolor,  borderwidth, command, cursor, font, fcolor, hbcolor,
          hfcolor, relief, state, takefocus, tcolor, variable
    
    **Less common options**
    
          bigincrement, digits, from, highlightthickness, label, orient,
          repeatdelay, repeatinterval, resolution, showvalue, sliderlength,
          sliderrelief, tickinterval, to 
          
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/scale.html">anzeljg reference</a>
    for th class **tkinter.scale**
    \see \ref NtkScale.py example file"""
    

        #Valid resource names: activebackground, background, bigincrement, bd,
        #bg, borderwidth, command, cursor, digits, fg, font, foreground, from,
        #highlightbackground, highlightcolor, highlightthickness, label,
        #length, orient, relief, repeatdelay, repeatinterval, resolution,
        #showvalue, sliderlength, sliderrelief, state, takefocus,
        #tickinterval, to, troughcolor, variable, width."""
        
    def __init__(self, parent, x, y, w, h, pad=0, limits=None, variable=None, command=None):
        """The constructor. You can specify here the numeric limits of the scale, a Variable
        object which will be updated at state change and a callback to associate to status
        change.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param limits you can specify a duple of numbers (min and max) or a triple
        (min, max, step)
        \param variable the Variable object whose value is associated with the button
        states; here you can specify:
         + None: a DoubleVar is automatically created
         + an IntVar or DoubleVar object
        \param command see \ref EVENTS"""        
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Scale.__init__)
        hv = HORIZONTAL if self.winfo_w() >= self.winfo_h() else VERTICAL  
        self.config(orient=hv)
        if isinstance(limits, (list, tuple)):
            self.config(from_=limits[0], to=limits[1])
            if len(limits) == 3:
                self.config(bigincrement=limits[2])
        self.valueVar = tk.DoubleVar() if not variable else variable 
        self.valueVar.set(str(limits[0]))
        self.valueVar.trace("w", lambda *args: self.event_generate("<<ChangedVar>>"))
        self.config(variable=self.valueVar)
        self._cont_type = None
        self._get_parent_config()
        self._commandwrap = None
        if command:
            self.config(command=command)
            
    def set_variable(self, variable=None, from_=None, to_=None, increment=None):
        """Sets the associated tkinter.Variable object and its values when
        the button is in off and on state. Only the given values are changed.
        You should do this in the constructor so you need this only if you want
        to change them later."""
        if variable:
            self.config(variable=variable)
            self.valueVar = variable
        if from_:
            self.config(from_=from_)
            if self.valueVar.get() < from_:
                self.valueVar.set(from_)
        if to:
            self.config(to=to)
            if self.valueVar.get() > to:
                self.valueVar.set(to)            
        if increment:
            self.config(bigincrement=increment)
        
    def get_value(self):
        """Returns the actual value associated to the scale.
        \note for this class the get_content() method returns
        an empty string"""
        return self.valueVar.get()        
            



class NtkScrollbar(tk.Scrollbar):
    """Scrollbar widget which displays a slider at a certain position.
    This is unchanged with respect to tkinter. Some widgets (NtkListbox,
    NtkText) have an auto-scrollbar feature, which adds or remove the
    vertical scrollbar if the text exceed the widget height, so you
    don't have to add this manually.
    
    **Common options** (see \ref ATTRIBUTES)
    
          abcolor, bcolor, borderwidth, command, cursor, hbcolor, hfcolor, 
          relief, takefocus, tcolor
    
    **Less common options**
    
          activerelief, elementborderwidth, highlightthickness, jump,
          orient, repeatdelay, repeatinterval
          
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/scrollbar.html">anzeljg reference</a>
    for the class **tkinter.Scrollbar**."""

        #Valid resource names: activebackground, activerelief,
        #background, bd, bg, borderwidth, command, cursor,
        #elementborderwidth, highlightbackground,
        #highlightcolor, highlightthickness, jump, orient,
        #relief, repeatdelay, repeatinterval, takefocus,
        #troughcolor, width."""
        
    def __init__(self, master=None, cnf={}, **kw):
        """The constructor.""" 
        tk.Scrollbar.__init_(self, master, cnf, kw)



class NtkSpinbox(NtkWidget, tk.Spinbox):
    """Spinbox widget, which allows to choose from a list of strings or
    type one. You can set it in a readonly state for disabling typing
    into it and enable the autoadd feature, which automatically adds
    to the item list every string you type. You can associate a StringVar
    to its value and a callback to be called when the the user changes
    his choice.
    
    **Common options** (see \ref ATTRIBUTES)
    
         abcolor, bcolor, borderwidth, command, cursor, dbcolor,
         dfcolor, font, fcolor, hbcolor, hborder, hfcolor, ibcolor,
         justify, rbcolor, relief, sbcolor, sfcolor, state, takefocus,
         textvariable
             
    **Less common options** 

         buttonbackground, buttoncursor, buttondownrelief,
         buttonuprelief, exportselection, format, from,
         insertborderwidth, insertofftime, insertontime, insertwidth,
         invalidcommand, increment, repeatdelay,  repeatinterval,
         selectborderwidth, to, validate, validatecommand values,
         xscrollcommand, wrap
         
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/listbox.html">anzeljg reference</a>
    for the class **tkinter.Spinbox**
    \see \ref NtkSpinbox.py example file""" 
    
    #def trace_text(self, *args):
        #self.event_generate("<<CHANGEDVAR>>")
        #val = self.cget("values")
        #if val:
            #pass
           
    def __init__(self, parent, x, y, w, h, pad=0, limits=None, variable= None, command=None):
        """The constructor. You can specify here the admitted values for the spinbox, a Variable
        object which will be updated when the state changes and a callback to associate to the
        choice event.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS
        \param limits the admitted values; here you can specify
         + a list of strings
         + a duple of int or float (the min and max)
         * a triple of int or float (min, max and step)
        \param variable the StringVar object whose value is associated with the
        choosen item (numbers are  converted into strings); if you leave None an
        internal StringVar is created
        \param command see \ref EVENTS"""        
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Spinbox.__init__)
        #self.config(relief=SUNKEN)
        if isinstance(limits, (list, tuple)):
            if isinstance(limits[0], str):
                self.config(values=limits)
            elif isinstance(limits[0], (int, float)):
                self.config(from_=limits[0], to=limits[1])
                if len(limits) == 3:
                    self.config(increment=limits[2])
        self.textVar = tk.StringVar() if not variable else variable
        self.init_content(self.textVar)
        if limits:
            self.textVar.set(str(limits[0]))
        self.textVar.trace("w", lambda *args: self.event_generate("<<ChangedVar>>"))
        self._get_parent_config()
        self._commandwrap = None
        self._autoaddflag = False
        if command:
            self.config(command=command)
            self.bind("<Key-Return>", self._autoadd)            
        
        
    def bind(self, sequence=None, func=None, add=None):
        """Redefines the Misc.bind() method for this class.
        We need it because the constructor binds the Key-Return
        event to the command callback."""
        # If sequence has more than one event, they must happen in sequence
        # for the func is triggered. So sequence="<Configure><Enter>" does not
        # affect <Configure>
        if sequence == "<Key-Return>":
            return super().bind(sequence, func, add=True)
        else:
            return super().bind(sequence, func, add)
               
    def unbind(self, sequence, funcid=None):
        """Redefines the Misc.unbind method for this class.
        We need it because the constructor binds the Key-Return
        event to the command callback."""
        super().unbind(sequence, funcid)
        if sequence == "<Key-Return>" and not funcid:
            super().bind("<Key-Return>", self._commandwrap)                   
    
    def mode(self, mode, wrap=None, validate=None):
        """Sets the spinbox mode to one of these three:
        - normal you can get the content by clicking the arrow keys or
          typing in the texr field
        - readonly: you can only click the arrow key
        - autoadd: (only if values are string) as normal, but inserts
          every new typed word into the list""" 
          
        if mode in ("normal", "readonly"):
            self.config(state=mode)
            _autoaddflag = False
        elif mode == "autoadd":
            self.config(state="normal")
            self._autoaddflag = True
        if wrap:
            self.config(wrap=wrap)
        if validate:
            self.config(validate=validate)
    
    def _autoadd(self, event):
        s = self.textVar.get()
        values = self.cget("values")
        if self._autoaddflag and len(values) and len(s):
            values = values.split()
            if s not in values:
                values.append(s)
                self.config(values=values)
                self.textVar.set(s)
        if self._commandwrap:
            self._commandwrap()    



class NtkText(NtkWidget, tk.Text):
    """Text widget which can display formatted text. This widget is
    almost unchanged with respect to tkinter.

    **Common options** (see \ref ATTRIBUTES)
    
         bcolor, borderwidth, cursor, font, fcolor, hbcolor, hborder,
         hfcolor, ibcolor, relief, sbcolor, sfcolor, state, takefocus,
         
    **Less common options**    

         autoseparators, exportselection, insertborderwidth, insertofftime,
         insertontime, insertwidth, maxundo, padx, pady, selectborderwidth,
         setgrid, spacing1, spacing2, spacing3, tabs, undo, wrap,
         xscrollcommand, yscrollcommand
         
    see <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/text.html">anzeljg reference</a>
    for the class **tkinter.Text**.""" 

    def __init__(self, parent, x, y, w, h, pad=0):
        """The constructor. It produces a text widget with an automatic vertical
        scrollbar.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS"""
        
        NtkWidget.__init__(self, parent, x, y, w, h, pad, tk.Text.__init__)
        self._get_parent_config()
        self._vscroll = tk.Scrollbar(self, orient=VERTICAL)
        self.config(yscrollcommand=self._vscroll.set)
        self._vscroll.config(command=self.yview)        
               
    def append_text(self, t):
        """Appends the text t to the end."""
        self.insert(END, t)
        self._auto_yscroll()
    
    def set_text(self, t):
        """Replaces the actual text with t."""
        self.clear()
        self.insert(END, t)
        self._auto_yscroll()
    
    def get_text(self):
        """Returns the entire widget content."""
        return self.get('1.0', END)
    
    def clear(self):
        """Sets the text to an empty string."""
        self.delete('1.0', END)
        self._auto_yscroll()

    def tag_config(self, tagName, cnf=None, **kw):
        """Configures a tag."""
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





class NtkNotebook(NtkWidget, ttk.Notebook):
    """Ttk Notebook widget which manages a collection of windows and displays
    a single one at a time. Each child window is associated with a tab,
    which the user may select to change the currently-displayed window.
    See <a href="https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html"anzeljg
    reference</a> for the class **ttk.Notebook**.
    \warning being this a ttk widget you cannot use the config() method on it."""
    def __init__(self, parent, x, y, w, h, pad=0):
        """The constructor.
        \param parent the widget parent
        \param x, y, w, h, pad see \ref PLACING_WIDGETS"""        
        NtkWidget.__init__(self, parent, x, y, w, h, pad, ttk.Notebook.__init__)
        self._get_parent_config()
        
        

#####################################################################
############               E   N   D
#####################################################################
        
        
if __name__ == "__main__":
    winMain = NtkMain(100, 100, 400, 250, "Ntk")
    labInfo = NtkLabel(winMain, CENTER, 20, 300, 100, content=
"""Ntk - A simple tkinter wrapper
Version {:}
Copyright Nicola Cassetta 2021""".format(__version__))
    labInfo.config(anchor=CENTER, relief=RIDGE, bcolor="white", justify=CENTER)
    butClose = NtkButton(winMain, CENTER, 180, 60, 30, content="Exit",
                         command=lambda ev: winMain.destroy())
    mainloop()




