import _setup           # allows import from parent folder
from NCtk import *

COL1 = "#A0C0E0"
COL2 = "#B0D0F0"
COL3 = "#F0B0D0"
    
STR0 = "My Window"
STR1 = "Ouch! I'm stretching!"
STR2 = "Augh! I'm shrinking!"
STR3 = "The mouse is over me"
STR4 = "The mouse has left me"
STR5 = "I've got the focus"
STR6 = "I've lost the focus"

class MyMain(NCtkMain):
    def __init__(self, x, y, w, h, title=""):
        NCtkMain.__init__(self, x, y, w, h, title)
        self.afterid = None
        self.update()
        self.oldw, self.oldh = self.getwinfo("width"), self.getwinfo("height")
        self.bind("<Configure>", self.change_title)
        self.lab1 = NCtkLabel(self, 0, 0, "fill", "40%", pad=(20, 10))
        self.lab1.config(bcolor=COL1, takefocus=True)
        self.lab2 = NCtkLabel(self, 0, PACK, FILL, "40%", pad=(20, 10))
        self.lab2.config(bcolor=COL1, takefocus=True)
        self.lab3 = NCtkLabel(self, 0, PACK, FILL, FILL, pad=(20, 10))
        self.lab3.setcontent("Click on the labels above and move the focus with the TAB key")

        # event.type is an int number coding the event. So all suggest
        # to always have separate handlers for separate events
        self.bind_class("Label", "<Enter>", self.change_label)
        self.bind_class("Label", "<Leave>", self.change_label)
        self.bind_class("Label", "<FocusIn>", self.change_label)
        self.bind_class("Label", "<FocusOut>", self.change_label)

        self.afterid = self.after(100, self.default_title)
    
        
    def change_title(self, event):
        if self.afterid:
            self.after_cancel(self.afterid)
            print("after() delayed")
            self.afterid = None
        neww = self.getwinfo("width")
        newh = self.getwinfo("height")
        #print("neww={} oldw={} newh={} oldh={}".format(neww, self.oldw, newh, self.oldh))
        if neww > self.oldw or newh > self.oldh:
            if self.title() != STR1:
                self.title(STR1)
        elif neww < self.oldw or newh < self.oldh:
            if self.title() != STR2:
                self.title(STR2)
        self.oldw, self.oldh = neww, newh
        self.afterid = self.after(100, self.default_title)
        #print(self.afterid)
        
        
    def default_title(self):
        print("default_title() called")
        self.title(STR0)
        self.afterid = None
        
    def change_label(self, event):
        t, w = event.type, event.widget
        if w == self.lab3:
            return
        if t == tk.EventType.Enter:
            w.config(bcolor=COL2)
            w.setcontent(STR3)
        elif t == tk.EventType.Leave:
            w.config(bcolor=COL1)
            w.setcontent(STR4)
        elif t == tk.EventType.FocusIn:
            w.config(bcolor=COL3)
            w.setcontent(STR5)
        elif t == tk.EventType.FocusOut:
            w.config(bcolor=COL1)
            w.setcontent(STR6)
            
                
winMain = MyMain(100, 100, 400, 300)

mainloop()