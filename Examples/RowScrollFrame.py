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


def add_row(event):
    rsf1.add_row(40)
    Ntk.Label(rsf1, PACK, PACK, "40%", FILL, pad=5, content="Row " + str(rsf1._rows[-1].num))
    Ntk.Label(rsf1, PACK, PACK, "40%", FILL, pad=5, content="Label 2") 

def del_row(event):
    # see the VerScroll.Frame.get_intframe() note.
    if rsf1.num_rows() > 0:
        rsf1.del_row(rsf1.num_rows() - 1)


# main window
winMain = Ntk.Main(200, 150, 400, 300, "VerScrollFrame sample")

# extern frame
hfr1 = Ntk.HorFrame(winMain, 0, 0, FILL, FILL)
# our VerScrollFrame
rsf1 = Ntk.RowScrollFrame(hfr1, 0, 0, "70%", FILL)
rsf1.config(relief=SOLID)
rsf1.config_children(Ntk.Label, relief="solid", bcolor = "blue", fcolor="yellow",
                     anchor=CENTER)
# vertical frame for buttons
vfr1 = Ntk.VerFrame(hfr1, PACK, 0, FILL, FILL)
# buttons
butAdd = Ntk.Button(vfr1, CENTER, PACK, "80%", 60, pad=(0,10), content="Add row", command=add_row)
butDel = Ntk.Button(vfr1, CENTER, PACK, "80%", 60, pad=(0,10), content="Delete row", command= del_row)


Ntk.mainloop()
