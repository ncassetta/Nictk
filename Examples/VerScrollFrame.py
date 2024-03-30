# This file is part of Nictk - A simple tkinter wrapper.
#    Copyright (C) 2021-2024 Nicola Cassetta
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


def add_label(event):
    str_label = "Label " + str(len(vsf1._frame.winfo_children()) + 1)
    lab = Ntk.Label(vsf1, 10, PACK, 120, 40, pad=5, content=str_label)

def del_label(event):
    if len(vsf1._frame.winfo_children()) > 0:
        lab = vsf1._frame.winfo_children()[-1]
        lab.destroy()


winMain = Ntk.Main(200, 150, 400, 300, "VerScrollFrame sample")

# THIS DOESN'T WORK!!!!!

## extern frame
#hfr1 = Ntk.HorFrame(winMain, 0, 0, FILL, FILL)
## our VerScrollFrame
#vsf1 = Ntk.VerScrollFrame(hfr1, 0, 0, "70%", FILL)
#vsf1.config_children(Ntk.Label, relief="solid", bcolor = "blue", fcolor="yellow",
                     #anchor=CENTER)
## vertical frame for buttons
#vfr1 = Ntk.VerFrame(hfr1, PACK, 0, FILL, FILL)
## buttons
#butAdd = Ntk.Button(vfr1, CENTER, PACK, "80%", 60, pad=(0,10), content="Add label", command=add_label)
#butDel = Ntk.Button(vfr1, CENTER, PACK, "80%", 60, pad=(0,10), content="Delete label", command= del_label)

# THIS IS OK

vsf1 = Ntk.VerScrollFrame(winMain, 0, 0, FILL, FILL)
vsf1.config_children(Ntk.Label, relief="solid", bcolor = "blue", fcolor="yellow",
                     anchor=CENTER)

for i in range(30):
    lab = Ntk.Label(vsf1, 10, PACK, 120, 40, pad=5, content="Label " + str(i + 1))
    print("Label size:", lab.winfo_w(), "x", lab.winfo_h())
    parent = lab.parent()
    print("Parent size:", parent.winfo_reqwidth(), "x", parent.winfo_reqheight())
    


Ntk.mainloop()
