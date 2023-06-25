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

# Italian cities
CITIES = ("Bari", "Bologna", "Firenze", "Milano", "Napoli", "Palermo",
         "Roma", "Torino", "Venezia")

MODES = {"normal":"You can change the Spinbox value clicking on buttons or typing in it and pressing <RETURN>",
         "readonly":"You can only use up and down buttons",
         "autoadd":"As Normal, but every new value you type is added to the Spinbox list"}

WRAPS = ["When you arrive at the end of the list you can continue from the beginning",
         "When you arrive at the end of the list you cannot go beyond"]


def change_label(event):
    w = event.widget
    if w == spb1:
        labSample.config(fcolor="dark blue")
        labSample.set_content("Selected city: " + w.get_content())
    else:
        labSample.config(fcolor="brown")
        labSample.set_content("Selected number: " + w.get_content())
        
        
def change_mode(event):
    opt = optMode.get()
    labMode.set_content(MODES[opt])
    spb1.mode(opt)
        
def change_wrap(event):
    opt = optWrap.get()
    labWrap.set_content(WRAPS[0] if opt else WRAPS[1])
    spb1.config(wrap=opt)


winMain = Ntk.Main(200, 150, 640, 480, "Spinbox")
# main hor frame, containing left and right subframes
vfr1 = Ntk.HorFrame(winMain, 0, 0, FILL, -60)

#left frame
rfr1 = Ntk.RowFrame(vfr1, 0, 0, "50%", FILL, content="Spinbox1")
rfr1.config(bcolor="#B0D0D0", relief=RIDGE )
rfr1.config_children(ALL, bcolor="#B0D0B0")
rfr1.config_children(Ntk.Spinbox, rbcolor="#A0C0A0")

rfr1.add_row(40)
spb1 = Ntk.Spinbox(rfr1, CENTER, 0, "50%", FILL, pad=(0, 3), limits=CITIES,
                   command=change_label)

rfr1.add_row(50)
labModeTitle = Ntk.Label(rfr1, 0, 0, FILL, FILL, pad=(0, 5),
                         content="Spinbox modes")
labModeTitle.config(bcolor=rfr1.get_config("bcolor"), relief=FLAT, anchor=S,
                    font=("Arial", 16))

rfr1.add_row("30%")
vfrMode = Ntk.VerFrame(rfr1, 0, CENTER, "40%", "80%")
vfrMode.config(relief=SUNKEN)

optMode = Ntk.StringVar()
tempT = tuple(MODES.keys())
radMode1 = Ntk.Radiobutton(vfrMode, 0, PACK, FILL, "33%", content=tempT[0],
                           variable=(optMode, tempT[0]), command=change_mode)
radMode2 = Ntk.Radiobutton(vfrMode, 0, PACK, FILL, "33%", content=tempT[1],
                           variable=(optMode, tempT[1]), command=change_mode)
radMode3 = Ntk.Radiobutton(vfrMode, 0, PACK, FILL, "33%", content=tempT[2],
                           variable=(optMode, tempT[2]), command=change_mode)
labMode = Ntk.Label(rfr1, PACK, CENTER, FILL, "80%", pad=(5, 0,10, 0))
labMode.config(anchor=NW)

rfr1.add_row(50)
labWrapTitle = Ntk.Label(rfr1, 0, 0, FILL, FILL, pad=(0, 5),
                         content="Enable wrap")
labWrapTitle.config(bcolor=rfr1.get_config("bcolor"), relief=FLAT, anchor=S,
                    font=("Arial", 16))

rfr1.add_row("30%")
optWrap = Ntk.BooleanVar()
vfrWrap = Ntk.VerFrame(rfr1, 0, CENTER, "40%", "80%")
vfrWrap.config(relief=SUNKEN)
radWrap1 = Ntk.Radiobutton(vfrWrap, 0, PACK, FILL, "50%", content="True",
                           variable=(optWrap, True), command=change_wrap)
radWrap2 = Ntk.Radiobutton(vfrWrap, 0, PACK, FILL, "50%", content="False",
                           variable=(optWrap, False), command=change_wrap)
labWrap = Ntk.Label(rfr1, PACK, CENTER, FILL, "80%", pad=(5, 0,10, 0))
labWrap.config(anchor=NW)

# right frame
rfr2 = Ntk.RowFrame(vfr1, PACK, 0, FILL, FILL, content="Spinbox2")
rfr2.config(bcolor="#FFFFA0", relief=RIDGE)
rfr2.add_row(40)
spb2 = Ntk.Spinbox(rfr2, CENTER, 0, "50%", FILL, pad=(0,3),
                   limits=(1.0, 10.0, 0.5), command=change_label)

#bottom label
labSample = Ntk.Label(winMain, CENTER, PACK, 280, FILL, pad=(0, 5),
                      content="Try the spinboxes!")
labSample.config(bcolor="pink", anchor=CENTER, font=("Arial", 16))

radMode1.invoke()
radWrap2.invoke()

Ntk.mainloop()
