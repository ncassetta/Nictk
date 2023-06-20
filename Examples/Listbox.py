# This file is part of Nictk - A simple tkinter wrapper.
#    Copyright (C) 2021-2023 Nicola Cassetta
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


# TODO: delete should delete all items selected, not only the last one


# items to be added to the listbox (italian numbers)
numbers = ("Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto",
           "Nove", "Dieci", "Undici", "Dodici", "Tredici", "Quattordici")
# selection modes
modes = ("single", "browse", "multiple", "extended")
# explanations of selection modes
explmodes = ("single mode : you can select only one item at once, clicking on it in the listbox",
             "browse mode : you can select only an item at once, clicking on it or dragging with the mouse",
             "multiple mode : you can select multiple items, clicking on them; clicking on a selected item " +
             "unselects it",
             "extended mode : you can select multiple items, clicking, dragging the mouse and using the" +
             "<CTRL> or <SHIFT> keys")


def add_item(event):
    """Adds an item to the left listbox and controls
    the state of ButAdd and ButDel."""
    nitems = lstTest.size()
    if nitems < len(numbers):
        lstTest.add(numbers[nitems])
    nitems = lstTest.size()
    if nitems > 0:        
        butDel.activate()
    if nitems == len(numbers):
        butAdd.deactivate()
        
def del_item(event):
    """ Deletes an item from the left listbox and controls
    the state of ButAdd and ButDel."""
    nitems = lstTest.size()
    if nitems > 0:
        lstTest.delete(nitems - 1)
        # adjusts the selection report
        lbox_changed(None)
    nitems = lstTest.size()
    if nitems < len(numbers):
        butAdd.activate()
    if lstTest.size() == 0:
        butDel.deactivate()
        
        
        
def lbox_changed(event):
    """Callback called when you select one or more item in the left listbox."""
    sel = lstTest.get_selected()
    #print("testchanged with index", sel)
    if len(sel) == 0:
        s = "none"
    else:
        s = ""
        for i in sel:
            s += "{}, ".format(i)
        s = s[:-2]
    labSel.set_content("Selected index: " + s if len(sel) <= 1 else "Selected indexes: " + s) 

def mode_changed(event):
    """Callback called when the user modifies the selection mode."""
    #lstTest.select_clear(0, END)
    lbox_changed(None)
    sel = lstMode.get_selected()
    #print("selchanged() called with index", sel)
    if len(sel):
        labExplain.set_content(explmodes[sel[0]])
        lstTest.config(selectmode=modes[sel[0]])
    

winMain = Ntk.Main(200, 150, 600, 450, "NtkListbox widget sample")

# we use frames for positioning widgets
hfr1 = Ntk.HorFrame(winMain, 0, 0, FILL, FILL)
rfr1 = Ntk.RowFrame(hfr1, 0, 0, "50%", FILL)
vfr2 = Ntk.VerFrame(hfr1, PACK, 0, FILL, FILL)

rfr1.add_row(40)
labTest = Ntk.Label(rfr1, 0, 0, FILL, FILL, pad=(10, 10, 10, 5),
                       content="Try to select items")
labTest.config(bcolor="light green", fcolor="blue", relief=SOLID,
               borderwidth=1, anchor=CENTER)

rfr1.add_row(-80)
lstTest = Ntk.Listbox(rfr1, 0, 0, FILL, FILL, pad=(10, 5, 10, 40),
                         command=lbox_changed)
lstTest.config(bcolor="blue", fcolor="yellow", sfcolor="maroon", sbcolor="light blue", 
               relief=RIDGE, font=("TkDefaultFont", 14))

rfr1.add_row(40)
labSel = Ntk.Label(rfr1, 0, 0, FILL, FILL, pad=(10, 5))
labSel.config(bcolor="light green", fcolor="blue", relief=SOLID,
              borderwidth=1)

# calls the callback to adjust labSel content
lbox_changed(None)

rfr1.add_row(FILL)
butAdd = Ntk.Button(rfr1, "15%", 0, "35%", FILL, pad=(5,5, 5, 10),
                       content="Add item", command=add_item) 
butDel = Ntk.Button(rfr1, PACK, PACK, "35%", FILL, pad=(5, 5, 5, 10),
                       content="Del item", command =del_item)
butDel.deactivate()

labMode = Ntk.Label(vfr2, 0, 0, FILL, 40, pad=(10, 10, 10, 5),
                       content="Listbox Mode")
labMode.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1,
               anchor=CENTER)
lstMode = Ntk.Listbox(vfr2, 0, PACK, FILL, 120, pad=(10, 5),
                         command=mode_changed, items=modes)
lstMode.config(bcolor="cyan", fcolor="brown", font=("TkDefaultFont", 14), relief=RIDGE)
labExplain=Ntk.Label(vfr2, 0, PACK, FILL, FILL, pad=(10, 10),
                        content=explmodes[0])
labExplain.config(anchor=NW)
lstMode.select(0)

Ntk.mainloop()
