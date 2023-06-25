# This file is part of Nictk - A simple tkinter wrapper.
#    Copyright (C) 2023 Nicola Cassetta
#    See <https://github.com/ncassetta/Nictk>
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


# Allows import from parent folder. You can delete this if you install the package
import _setup

import Nictk as Ntk
from Nictk.constants import *

BCOLOR = "#A0C0E0"      # light blue
COLORS = ("light salmon", "light green", "light yellow", "light cyan")


class MyMain(Ntk.Main):
    def __init__(self, x, y, w, h):
        Ntk.Main.__init__(self, x, y, w, h)
        # these are used in self.change_title
        self.oldw, self.oldh = w, h
        self.afterid = None
        
        ## binds a callback to the windows size change
        #self.bind("<Configure>", self.change_title)
        
        ## creates two upper labels
        self.hfr1 = Ntk.HorFrame(self, PACK, PACK, FILL, "20%")
        self.labbind = Ntk.Label(self.hfr1, PACK, PACK, "50%", FILL, pad=(5, 15))
        self.labbind.config(bcolor=BCOLOR, font=("Arial", 12), text="Enabled")
        self.chkbind1 = Ntk.Checkbutton(self.hfr1, PACK, PACK, "25%", FILL, pad=(5, 15),
                                        content="Bind mouse click", command=self.label_bind)
        self.chkbind2 = Ntk.Checkbutton(self.hfr1, PACK, PACK, "25%", FILL, pad=(5, 15),
                                        content="Deactivate", command=self.label_status)
        self.color_index = -1
        

        # sets window title to "My Window"
        self.default_title()
        
        self.checkwindow = Ntk.Checkbutton(self, PACK, PACK, "50%", "20%", pad=(5, 15),
                                        content="Bind resize to window", command=self.window_bind)
        

    def label_bind(self, event):
        lab = self.labbind
        if "<Button-1>" in lab.bind():
            lab.unbind("<Button-1>")
            lab.set_content(lab.get_content().replace("Bound to mouse click - ", ""))
            lab.config(bcolor=BCOLOR)
        else:
            lab.bind("<Button-1>", self.label_on_click)
            lab.set_content("Bound to mouse click - " + lab.get_content()) 
    
    def label_status(self, event):
        lab = self.labbind
        if lab.enabled():
            lab.deactivate()
            lab.set_content(lab.get_content().replace("Enabled", "Disabled"))
        else:
            lab.activate()
            lab.set_content(lab.get_content().replace("Disabled", "Enabled"))
                           
    def label_on_click(self, event):
        self.color_index = (self.color_index + 1) % len(COLORS)
        self.labbind.config(bcolor=COLORS[self.color_index])
        
    def window_bind(self, event):
        but = event.widget
        if but.get_value():
            self.bind("<Configure>", self.change_title)
        else:
            self.unbind("<Configure>")
        
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
                    
                
winMain = MyMain(100, 100, 640, 320)
Ntk.mainloop()