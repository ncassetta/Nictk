import tkinter as tk
from  tkinter import ALL, BOTH, BOTTOM, CENTER, DISABLED, E, END, FIRST, FLAT, GROOVE, HIDDEN, HORIZONTAL, LAST, \
LEFT, N, NE, NO, NS, NSEW, NW, RAISED, RIDGE, RIGHT, ROUND, S, SE, SEL, SINGLE, SOLID, SUNKEN, SW, TOP, \
VERTICAL, W, IntVar, StringVar, BooleanVar
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb

['bd', 'borderwidth', 'class', 'menu', 'relief', 'screen', 'use', 'background', 'bg', 'colormap', 'container', 'cursor', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx', 'pady', 'takefocus', 'visual', 'width']


            
# To get a widget property use w.cget("name")       name as string, always returns a string
# To set a widget property use w.config(name=val)


#####################################################################
###################    T K I N T E R   F U N C T I O N S
#####################################################################

mainloop = tk.mainloop

#####################################################################
###################    M I X I N   C L A S S E S
#####################################################################

# Methods defined on both toplevel and interior widgets
class NCtkMisc:
    """Internal class.

    Base class which defines methods common for windows and interior widgets."""
    
   #TODO: what other methods should go here?
    _trans_opt =  { "abcolor":"activebackground", "afcolor":"activeforeground",
                    "bcolor":"background", "dfcolor":"disabledforeground",
                    "fcolor":"foreground", "hbcolor":"highlightbackground",
                    "hcolor":"highlightcolor", "hborderwidth":"highlightthickness",
                    "sbcolor":"selectbackground", "sfcolor":"selectforeground",
                    "textvar":"textvariable"}    

    def config(self, cnf=None, **kw):
        if isinstance(cnf, dict):
            cnf.update(kw)
        elif cnf is None and kw:
            cnf = kw
        if cnf is None:
            trans_cnf = None
        else:
            trans_cnf = {}
            for k, v in cnf.items():
                newk = NCtkMisc._trans_opt[k] if k in NCtkMisc._trans_opt else k
                trans_cnf[newk] = v
                # TODO: what other options must be config for the _extFrame???
                #if k == "bcolor" and hasattr(self, "_extFrame"):
                #    self._extFrame.config({newk:v})
        
        return self._configure('configure', trans_cnf, None)
    
    def getconfig(self, key):
        if key in self._trans_opt:
            key = self._trans_opt[key]
        return self.cget(key)
    
    def getwinfo(self, key, *kw):
        if key == "parent" and hasattr(self, "_extFrame"):
                return self._extFrame.winfo_parent()
        function = "winfo_" + key
        return getattr(tk.Widget, function)(self, *kw)


class NCtkContainer:
    def __init__(self):
        #elf.update()
        self._oldw, self._oldh = self.winfo_width(), self.winfo_height()
        #self.bind("<Configure>", self._resize_children)       ONLY FOR WINDOWS!!!
        self._cnfchildren = []
    
    def config_children(self, which, **kw):
        l = [item["which"] for item in self._cnfchildren]
        if which not in l:
            item = {"which":which, "options":kw}
            self._cnfchildren.append(item)
        else:
            self._cnfchildren[l.index(which)]["options"].update(kw)
        
    def _resize_children(self, event=None):
        print("_resize_children() called by", self.winfo_name())
        #self.update()       # needed for updating w and h
        if self._oldw != self.winfo_width() or self._oldh != self.winfo_height():
            self._oldw, self._oldh = self.winfo_width(), self.winfo_height()
            for w in self.winfo_children():
                if hasattr(w, "_update_dimensions"):    # w is a HorFrame or VerFrame
                    w._update_dimensions()
                    if hasattr(w, "_resize_children"):
                        w._resize_children()                    
                else:                                   # w is a Frame embedding a widget
                    for w1 in w.winfo_children():
                        if hasattr(w1, "_update_dimensions"):    # otherwise error with scrollbars
                            w1._update_dimensions()                        
                            if hasattr(w, "_resize_children"):
                                w._resize_children()
    
    


# Added by me to override tkinter Widget methods

class NCtkWidget(NCtkMisc):  
    def __init__(self, x, y, w, h, pad=0):
        self._orig_dim = (x, y, w, h, pad)      # tk.Widget.__init__ does nothing 
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
        elif isinstance(content, tk.StringVar):
            self.config(text=content, textvariable=content, image="")
        elif isinstance(content, tk.PhotoImage) or isinstance(content, tk.BitmapImage):
            self.config(text="", textvariable=None, image=content)        
    
    #def gettext(self):
    #    return self.cget("variable")
    
    #def winfo_parent(self):
    #    return self_extFrame.winfo_parent() if hasattr(self, _extFrame) else self.winfo_parent() 
    
    def _calc_dimensions(self, parent, x, y, w, h, pad):   #TODO: implement "rpack"
        #oldresizeflag = NCtkMain.resizeflag
        #NCtkMain.resizeflag = False
        parent.update_idletasks()
        #NCtkMain.resizeflag = oldresizeflag
        if not pad:                             # transform pad into two uples (EO and NS)
            padx, pady = (0, 0), (0, 0)
        elif not isinstance(pad, (list, tuple)):
            padx, pady = (pad, pad), (pad, pad)
        elif len(pad) == 2:
            padx, pady = (pad[0], pad[0]), (pad[1], pad[1])
        elif len(pad) == 4:
            padx, pady = (pad[0], pad[2]), (pad[1], pad[3])
            
        offs_x, offs_y = 0, 0    
        if isinstance(parent, NCtkRowFrame):                                                 
            parent = parent.get_active()
            offs_y = parent.winfo_y()
        elif isinstance(parent, (NCtkColFrame)):                                              
            parent = parent.get_active()
            offs_x = parent.winfo_x()
        
        brothers = parent.winfo_children()      # find the last widget from whom calculate coords
        container = self._extFrame if hasattr(self, "_extFrame") else self
        if container in brothers:               # we are resizing an already placed widget
            last_wdg = brothers[brothers.index(container) - 1] if brothers.index(container) > 0 else None
        else:                                   # we are placing a new widget
            last_wdg = parent.winfo_children()[-1] if parent.winfo_children() else None
        last_x, last_y = 0, 0
        if isinstance(parent, (NCtkHorFrame, _framerow))and last_wdg:
            last_x = last_wdg.winfo_x() + last_wdg.winfo_reqwidth()
        elif isinstance(parent, (NCtkVerFrame, _framecol, NCtkMain, NCtkWindow)) and last_wdg:
            last_y = last_wdg.winfo_y() + last_wdg.winfo_reqheight() 

        
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
                x = round((parent.winfo_width() - tempw) / 2)
            elif x.endswith("%"):
                x = round(parent.winfo_width() * int(x[:-1]) / 100)
            else:
                raise TypeError
        if isinstance(y, str):                  # calculate y
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
        return x, y, w, h, padx, pady
        
    def _place_widget(self, x, y, w, h, padx, pady):
        if isinstance(self, (NCtkHorFrame, NCtkVerFrame, NCtkRowFrame, NCtkColFrame)):
            self.place_forget()
            self.config(width=w, height=h)
            self.place(x=x, y=y)
        else:
            self._extFrame.config(width=w, height=h)
            self._extFrame.place_forget()
            self._extFrame.place(x=x, y=y)
            self._extFrame.pack_propagate(False)
            self.pack(padx=padx, pady=pady, fill=BOTH, expand=True)
        #self.update()       # updates dimensions
        
    def _update_dimensions(self):
        print("_update_dimensions called on", self.winfo_name())
        x, y, w, h, pad = self._orig_dim
        parent = self._nametowidget(self.getwinfo("parent"))    # NOT self.master (could return self._extFrame)        
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        if hasattr(self, "vscroll") and self.vscroll.winfo_ismapped():
            padx = (padx[0], 0)                 # otherwise pad between widget and scrollbar
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(self, (NCtkLabel, NCtkCheckbutton, NCtkRadiobutton)):
            self.config(wraplength=self._calc_wrap())
        if hasattr(self, "vscroll"):
            #self.config(yscrollcommand=self.vscroll.set)
            #self.vscroll.config(command=self.yview)
            self._auto_yscroll()
            
            
    def _auto_yscroll(self):
        #self.update()
        if hasattr(self, "vscroll"):
            offs, size = self.yview()
            if size - offs < 1.0 and not self.vscroll.winfo_ismapped():
                x, y, w, h, pad = self._orig_dim
                parent = self._extFrame.master
                x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)                
                self.pack_forget()
                self.vscroll.pack(padx=(0, padx[1]), pady=pady, side=RIGHT, fill=BOTH)                 
                self.pack(padx=(padx[0], 0), pady=pady, side=LEFT, fill=BOTH, expand=True)
            elif size - offs == 1.0 and self.vscroll.winfo_ismapped():
                x, y, w, h, pad = self._orig_dim
                parent = self._extFrame.master
                x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
                self.pack_forget()
                self.vscroll.pack_forget()
                self.pack(padx=padx, pady=pady, side=LEFT, fill=BOTH, expand=True)
            self.update()
    
    def _get_parent_config(self):
        configured = []
        cl = "NCtk" + self.winfo_class()
        p = self.master
        while p:
            if hasattr(p, "_cnfchildren"):
                for item in p._cnfchildren:
                    wh = item["which"]
                    if isinstance(wh, str) and (wh == "all" or wh == cl):
                        self.config(item["options"])
                    elif isinstance(wh, (list, tuple)) and cl in wh:
                        self.config(item["options"])      
                        
                #tobeconf = p._cnfchildren.copy()
                #for k in configured:
                    #if k in tobeconf.keys():
                        #tobeconf.pop(k)
                #self.config(tobeconf)
                #configured += tobeconf.keys()
            p = p.master

         
# Used by various widgets for calling with command with an event parameter. 
class _setitCommand:
    """Internal class. It wraps the command in widgets which have a command option."""
    def __init__(self, widget, callback=None):
        self.__widget = widget
        self.__callback = callback
        
    def __call__(self, *args):
        if self.__callback:
            ev = tk.Event
            ev.type = "VirtualEvent"
            ev.widget = self.__widget
            ev.x = self.__widget.winfo_pointerx()
            ev.y = self.__widget.winfo_pointery()            
            self.__callback(ev, *args)



#####################################################################
###################    M A I N   W I N D O W
#####################################################################

class NCtkMain(NCtkMisc, NCtkContainer, tk.Tk):
    def __init__(self, x, y, w, h, title=""):
        tk.Tk.__init__(self)
        self.geometry("{}x{}+{}+{}".format(w, h, x, y))
        NCtkContainer.__init__(self)
        self.bind("<Configure>", self._resize_children) 
        #self.resizable(width=FALSE, height=FALSE)
        self.title(title)
            
    def config_all(self, widget=None, **kw):
        prefix = "*" + widget[4:] + "." if widget else "*"
        for k, v in kw.items():
            self.option_add(prefix + k, v)
    
    def getwinfo(self, key, *kw):
        function = "winfo_" + key
        return getattr(tk.Widget, function)(self, *kw)
    
    resizeflag = True
                    
class NCtkWindow(NCtkMisc, NCtkContainer, tk.Toplevel):
    def __init__(self, parent, x, y, w, h, title="", modal=False):
        tk.Toplevel.__init__(self, master=parent)
        xp = parent.winfo_x()
        yp = parent.winfo_y()
        self.geometry(str(w) + "x" + str(h) + "+" + str(x+xp) + "+" + str(y+yp))
        NCtkContainer.__init__(self)
        self.bind("<Configure>", self._resize_children) 
        self.title(title)
        if modal:
            focus_set()
            grab_set()
            transient(parent)   


#####################################################################
#######################     F R A M E S
#####################################################################

class NCtkHorFrame(NCtkWidget, NCtkContainer, tk.LabelFrame):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad=0)    # pad argument is ignored
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, 0)
        tk.LabelFrame.__init__(self, parent, width=w, height=h, relief=FLAT)
        self.place(x=x, y=y)
        self.config(background=parent.cget("background"))
        NCtkContainer.__init__(self)
 
 
class NCtkVerFrame(NCtkWidget, NCtkContainer, tk.LabelFrame):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad=0)    # pad argument is ignored
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, 0)
        tk.LabelFrame.__init__(self, parent, width=w, height=h, relief=FLAT)
        self.place(x=x, y=y)
        self.config(background=parent.cget("background"))
        NCtkContainer.__init__(self)
        
        
class _framerow:
    def __init__(self, parent, h):
        self.master = parent
        self.num = len(parent._rows)
        self.children = []
        self._calc_dimensions(parent, h)

    def __str__(self):
        return str({"master":self.master,"num":self.num, "y":self.y,
                    "origh":self.orig_h, "h":self.h, "toth":self.tot_h })
        
    def winfo_children(self):
        return self.children

    def winfo_x(self):
        return 0

    def winfo_y(self):
        return self.y

    def winfo_height(self):
        return self.h

    def winfo_width(self):
        return self.master.winfo_width()
    
    def winfo_reqwidth(self):
        return self.master.winfo_reqwidth()
    
    def winfo_reqheight(self):
        return self.h
    
    def winfo_name(self):
        return "_framerow"
        
    def _calc_dimensions(self, parent, h):   #TODO: implement "rpack"
        parent.update_idletasks()
        n = self.num
        if n == len(parent._rows):                  # we qre placing a new row
            self.y = 0 if not len(parent._rows) else parent._rows[-1].tot_h
        else:                                       # always placed row
            self.y = 0 if n == 0 else parent._rows[n - 1].tot_h
        self.orig_h = h
        if isinstance(h, str):
            if h.endswith("%"):
                self.h = round(parent.winfo_height() * int(h[:-1]) / 100)
            elif h == "fill":
                if n == len(parent._rows):
                    self.h = parent.winfo_height() if not len(parent._rows) else \
                             parent.winfo_height() - parent._rows[-1].tot_h
                else:
                    self.h = parent.winfo_height() if n == 0 else \
                             parent.winfo_height() - parent._rows[n - 1].tot_h
        elif isinstance(h, int):
            if h < 0:
                self.h = parent.winfo_height() - self.y + h
                if self.h < 0:
                    raise ValueError
            else:
                self.h = h
        else:
            raise TypeError
        self.tot_h =self.y + self.h
        print(self)
        
    def _resize_children(self):
        for w in self.winfo_children():
            if hasattr(w, "_update_dimensions"):
                w._update_dimensions()
                if hasattr(w, "_resize_children"):
                    w._resize_children()       
            else:
                for w1 in w.winfo_children():
                    if hasattr(w1, "_update_dimensions"):
                        w1._update_dimensions()
                        if hasattr(w1, "_resize_children"):
                            w1._resize_children()                          


class _framecol:
    pass


class NCtkRowFrame(NCtkWidget, NCtkContainer, tk.Frame):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad=0)    # pad argument is ignored
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, 0)
        tk.Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        self.config(background=parent.cget("background"))
        NCtkContainer.__init__(self)
        self._rows = []
        self._active = None
        
    def add_row(self, h):
        self._rows.append(_framerow(self, h))
        self._active = self._rows[-1].num
        
    def set_active(self, n):
        if 0 <= n < len(self._rows):
            self._active = n
            
    def get_active(self):
        if self._active is None:
            raise ValueError
        return self._rows[self._active]
    
    def resize_row(self, n, h):
        row = self._rows[n]
        self._rows[n]._calc_dimensions(self, h)
        self._rows[n]._resize_children()
        for i in range(n + 1, len(self._rows)):
            self._rows[i]._calc_dimensions(self, self._rows[i].orig_h)
            self._rows[i]._resize_children()
            
    def _resize_children(self):
        oldactive =self._active
        for row in self._rows:
            self._active = row.num
            self.resize_row(row.num, row.orig_h)
            row._resize_children()
        self._active = oldactive
            
    #def _update_dimensions(self):
        #self._calc_dimensions(self.master, self.orig_h)
        #for w in self.children:
            #if hasattr(w, "_update_dimensions"):
                #wdg._update_dimensions()
            #else:
                #for w1 in wdg.children:
                    #if hasattr(w1, _update_dimensions):
                        #w1._update_dimensions()            
    

class NCtkColFrame(NCtkWidget, NCtkContainer, tk.Frame):
    def __init__(self, parent, x, y, w, h, pad=0):
        NCtkWidget.__init__(self, x, y, w, h, pad=0)    # pad argument is ignored
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, 0)
        tk.Frame.__init__(self, parent, width=w, height=h)
        self.place(x=x, y=y)
        self.config(background=parent.cget("background"))
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

# We must enclose all widgets in an external Frame to obtain their width and
# height in pixels, because otherwise the silly Tk would assume them in
# characters        

class NCtkButton(NCtkWidget, tk.Button):
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
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        tk.Button.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)): 
            parent.get_active().children.append(self._extFrame)
        self.config(anchor=CENTER, justify=LEFT)
        self._get_parent_config()
        self.setcontent(content)
        self.commandwrap = None
        if command:
            self.config(command=command)
            
    def config(self, cnf=None, **kw): # override for command
        if "command" in kw.keys():
            cback = kw.pop("command")
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


class NCtkCheckbutton(NCtkWidget, tk.Checkbutton):     ## TODO: manage command
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))        
        tk.Checkbutton.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
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
            self.commandwrap = _setitCommand(self, cback)
            super().config(command=self.commandwrap)
        return super(NCtkCheckbutton, self).config(cnf,**kw)
    
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        self.update_idletasks()         # sets correct sizes
        return self.winfo_width() - 20    
            

class NCtkEntry(NCtkWidget, tk.Entry):
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        tk.Entry.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        self.config(relief=SUNKEN)
        self._get_parent_config()
        self.intStr = tk.StringVar(name="var_"+self._name)
        if content:
            self.intStr.set(str(content))
        self.intStr.trace("w", self.trace_callback)
        self.config(textvariable=self.intStr)
        if command:
            self.bind("<Return>", command)
        
    # overrides NCtkWidget methods!
    def setcontent(self, content):
        self.intStr.set(str(content))
        
    def getcontent(self):
        return self.intStr.get()        


# class Frame substituted by NCtkHorFrame, NCtkVerFrame   
    
class NCtkLabel(NCtkWidget, tk.Label):
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        tk.Label.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        self.config(anchor=W, justify=LEFT, relief=SUNKEN, wraplength=self._calc_wrap())
        self._get_parent_config()
        self.setcontent(content)
        
    def _calc_wrap(self):               # Used to calculate text wraplength when resized 
        self.update_idletasks()         # sets correct sizes
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        #self._extFrame.config(bg="red")
        tk.Listbox.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        self.config(justify=LEFT, relief=SUNKEN, activestyle="none", exportselection=False)
        self._get_parent_config()
        self.vscroll = tk.Scrollbar(self._extFrame, orient=VERTICAL)
        self.config(yscrollcommand=self.vscroll.set)
        self.vscroll.config(command=self.yview)
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
        
class NCtkMenu(tk.Menu):
    """Menu widget which allows displaying menu bars, pull-down menus and pop-up menus.
        
        Valid resource names: activebackground, activeborderwidth,
        activeforeground, background, bd, bg, borderwidth, cursor,
        disabledforeground, fg, font, foreground, postcommand, relief,
        selectcolor, takefocus, tearoff, tearoffcommand, title, type."""
    def __init__(self, parent):
        tk.Menu.__init__(self, parent, tearoff=0)
        
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


class NCtkRadiobutton(NCtkWidget, tk.Radiobutton):
    """Radiobutton widget which shows only one of several buttons in on-state.

        Valid resource names: activebackground, activeforeground, anchor,
        background, bd, bg, bitmap, borderwidth, command, cursor,
        disabledforeground, fg, font, foreground, height,
        highlightbackground, highlightcolor, highlightthickness, image,
        indicatoron, justify, padx, pady, relief, selectcolor, selectimage,
        state, takefocus, text, textvariable, underline, value, variable,
        width, wraplength."""
    def __init__(self, parent, x, y, w, h, pad=0, content=None, command=None):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        tk.Radiobutton.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
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
    

class NCtkScale(NCtkWidget, tk.Scale):
    """Scale widget which can display a numerical scale.

        Valid resource names: activebackground, background, bigincrement, bd,
        bg, borderwidth, command, cursor, digits, fg, font, foreground, from,
        highlightbackground, highlightcolor, highlightthickness, label,
        length, orient, relief, repeatdelay, repeatinterval, resolution,
        showvalue, sliderlength, sliderrelief, state, takefocus,
        tickinterval, to, troughcolor, variable, width."""
    def __init__(self, parent, x, y, w, h,  pad=0, limits= None, command=None):
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        hv = HORIZONTAL if w >= h else VERTICAL
        tk.Scale.__init__(self, self._extFrame, orient=hv)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        if isinstance(limits, (list, tuple)):
            if isinstance(limits[0], str):
                self.config(values=limits)
            elif isinstance(limits[0], (int, float)):
                self.config(from_=limits[0], to=limits[1])
                if len(limits) == 3:
                    self.config(bigincrement=limits[2])
        self.intStr = tk.StringVar()
        self.intStr.set(str(limits[0]))
        self.intStr.trace("w", lambda: self.event_generate("<<CHANGEDVAR>>"))
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


class NCtkScrollbar(tk.Scrollbar):
    """Scrollbar widget which displays a slider at a certain position.

        Valid resource names: activebackground, activerelief,
        background, bd, bg, borderwidth, command, cursor,
        elementborderwidth, highlightbackground,
        highlightcolor, highlightthickness, jump, orient,
        relief, repeatdelay, repeatinterval, takefocus,
        troughcolor, width."""
    def __init__(self, master=None, cnf={}, **kw):
        tk:Scrollbar.__init_(self, master, cnf, kw)


class NCtkSpinbox(NCtkWidget, tk.Spinbox):
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        tk.Spinbox.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        self.config(relief=SUNKEN)
        if isinstance(limits, (list, tuple)):
            if isinstance(limits[0], str):
                self.config(values=limits)
            elif isinstance(limits[0], (int, float)):
                self.config(from_=limits[0], to=limits[1])
                if len(limits) == 3:
                    self.config(increment=limits[2])
        
        self.intStr = tk.StringVar()        
        self.intStr.set(str(limits[0]))
        self.intStr.trace("w", lambda: self.event_generate("<<CHANGEDVAR>>"))
        self.config(textvariable=self.intStr)
        self._get_parent_config()
        if command:
            self.config(command=command)

    def config(self, cnf=None, **kw): # override for command
        if "command" in kw.keys():
            cback = kw.pop("command")
            self.commandwrap = _setitCommand(self, cback)
            super().config(command=self.commandwrap)
        return super().config(cnf,**kw)  
            
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        tk.Text.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        self.config(relief=SUNKEN)
        self._get_parent_config()
        self.vscroll = tk.Scrollbar(self._extFrame, orient=VERTICAL)
        self.config(yscrollcommand=self.vscroll.set)
        self.vscroll.config(command=self.yview)        
               
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

class NCtkCombobox(NCtkWidget, tk.OptionMenu):
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
        
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        self.intStr = tk.StringVar()
        tk.OptionMenu.__init__(self, self._extFrame, self.intStr, items, None)
        self._place_widget(x, y, w, x, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
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
        NCtkWidget.__init__(self, x, y, w, h, pad)
        x, y, w, h, padx, pady = self._calc_dimensions(parent, x, y, w, h, pad)
        self._extFrame = tk.Frame(parent, width=w, height=h)
        self._extFrame.config(background=parent.cget("background"))
        ttk.Notebook.__init__(self, self._extFrame)
        self._place_widget(x, y, w, h, padx, pady)
        if isinstance(parent, (NCtkRowFrame, NCtkColFrame)):
            parent.get_active().children.append(self._extFrame)
        self._get_parent_config()
        
