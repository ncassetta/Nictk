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


def clear_text(event):
    pass

def save_text(event):
    pass



winMain = Ntk.Main(200, 150, 400, 300, "Text sample")

txt1 = Ntk.Text(winMain, 0, 0, FILL, "80%", pad=10)
hfr1 = Ntk.HorFrame(winMain, 0, PACK, FILL, FILL)
# buttons
butAdd = Ntk.Button(hfr1, CENTER, PACK, 80, 60, pad=(0,10), content="Save", command=clear_text)
butDel = Ntk.Button(hfr1, CENTER, PACK, 80, 60, pad=(0,10), content="Clear", command=save_text)

## THIS IS OK

#vsf1 = Ntk.VerScrollFrame(winMain, 0, 0, "80%", FILL)
#vsf1.config_children(Ntk.Label, relief="solid", bcolor = "blue", fcolor="yellow",
                     #anchor=CENTER)

    


Ntk.mainloop()
