import _setup           # allows import from parent folder
from Ntk import *


COL1 = "#A0C0E0"        # light blue
COL2 = "#B0D0F0"        # lighter blue
COL3 = "#F0B0D0"        # pink
COL4 = "#E0E0A0"        # light yellow


class MyMain(NtkMain):
    def __init__(self, x, y, w, h):
        NtkMain.__init__(self, x, y, w, h)
        # these are used in self.change_title
        self.oldw, self.oldh = w, h
        self.afterid = None
        
        # binds a callback to the windows size change
        self.bind("<Configure>", self.change_title)
        
        # creates two upper labels
        self.lab1 = NtkLabel(self, 0, 0, FILL, "40%", pad=(20, 10))
        self.lab1.config(bcolor=COL1, font=("Arial", 12), takefocus=True)
        self.lab2 = NtkLabel(self, 0, PACK, FILL, "40%", pad=(20, 10))
        self.lab2.config(bcolor=COL1, font=("Arial", 12), takefocus=True)
        # third (helper) label
        self.labHelp = NtkLabel(self, 0, PACK, FILL, FILL, pad=(20, 10))
        self.labHelp.setcontent(self.helpstr)
        # text will scroll, so no line wrapping
        self.labHelp.config(wraplen=0)

        # binds for all labels various events to the same handler
        # generally this is not recommended (see the docstring of
        # change_label)
        self.bind_class("Label", "<Enter>", self.change_label)
        self.bind_class("Label", "<Leave>", self.change_label)
        self.bind_class("Label", "<FocusIn>", self.change_label)
        self.bind_class("Label", "<FocusOut>", self.change_label)
        self.bind_class("Label", "<Button>", self.change_label)

        # sets window title to "My Window"
        self.default_title()
        # calls text_scroll after 1/5 sec
        self.after(200, self.scroll_string)
        # string which will scroll in the helper label
        

    helpstr = ("                          " +
        "Click on the labels above and move the focus with the TAB key    ---   " +
        "Try to drag windows edges")         
        

    def change_title(self, event):
        """This callback changes the window title when it is resized. If
        self.afterid is not None a change_title() timer is pending: it
        cancels it, and recharges the timer to 1/10 sec."""
        # if a timer for default_title is pending deletes it because we are still
        # dragging
        if self.afterid:
            self.after_cancel(self.afterid)
            self.afterid = None
        # gets the actual window dims and compares with old to guess if we are
        # stretching or shrinking
        neww = self.winfo_w()
        newh = self.winfo_h()
        #print("neww={} oldw={} newh={} oldh={}".format(neww, self.oldw, newh, self.oldh))
        if neww > self.oldw or newh > self.oldh:
            if self.title() != "Ouch! I'm stretching!":
                self.title("Ouch! I'm stretching!")
        elif neww < self.oldw or newh < self.oldh:
            if self.title() != "Augh! I'm shrinking!":
                self.title("Augh! I'm shrinking!")
        self.oldw, self.oldh = neww, newh
        # recharges default_title timer
        self.afterid = self.after(100, self.default_title)
        
        
    def default_title(self):
        """Resets the title of the main window to "Main Window".
        It is called 1/10 sec after you finish to resize the window."""
        #print("default_title() called")
        self.title("My Window")
        self.afterid = None
        

    def change_label(self, event):
        """Changes the labels text according to the happened event.
        Note that you can know what event happened comparing the attribute
        type with the Enum EventType. However is generally better to have
        separate handlers for separate events, this is done for demonstration"""
        t, w = event.type, event.widget
        # we don't want lab3 involved in events
        if w == self.labHelp:
            return
        if t == EventType.Enter:
            w.config(bcolor=COL2)
            w.setcontent("The mouse is over me")
            # enlarges the widget
            w.resize(pad=(17, 7))
        elif t == EventType.Leave:
            w.config(bcolor=COL1)
            w.setcontent("The mouse has left me")
            # sets original dims
            w.resize(pad=(20, 10))
        elif t == EventType.FocusIn:
            w.config(bcolor=COL3)
            w.setcontent("I've got the focus")
        elif t == EventType.FocusOut:
            w.config(bcolor=COL1)
            w.setcontent("I've lost the focus")
        elif t == EventType.Button:
            w.config(bcolor=COL4)
            w.setcontent("You clicked on me!")
            

    def scroll_string(self):
        "Scrolls  the helper string 1 char every 1/5 sec"""
        self.helpstr = self.helpstr[1:] + self.helpstr[0]
        self.labHelp.setcontent(self.helpstr)
        # recharges the timer
        self.after(200, self.scroll_string)
       
            
                
winMain = MyMain(100, 100, 400, 300)

mainloop()