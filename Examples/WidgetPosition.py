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


import _setup           # allows import from parent folder
import Ntk
from Ntk.constants import *

# Strings for the various labels

STR_LAB1 = """Label 1 has absolute position:
x=0, y=0, w=400, h=50, pad=(10,5)"""
STR_LAB2 = """Label 2 is packed under Label 1 and has relative width:
x=0, y=PACK, w="75%", h=50, pad=(10, 5)"""
STR_LAB3="""Label 3 has absolute (from right) width and relative height:
x=0, y=PACK, w=-200, h="10%", pad=(10, 5)"""
STR_HOR1 = "Hor Frame 1 is packed under Label 3. It fills parent width: x=0, y=PACK, w =FILL, h=180"
STR_LAB4 = """Label 4 is a child of the frame:
x="10%", y=CENTER, w="40%", h=50, pad=(5,0)"""
STR_LAB5 ="""Label 5 is packeded right Label 4 in the frame:
x=PACK, y=CENTER, w="40%", h=50, pad=(5,0)"""
STR_LAB6 ="""Label 6 is packed under the frame, x and w are from right:
x=-400, h=PACK, w=-50, h=60, pad=(0,10)"""


# create the main window
winMain = Ntk.NtkMain(50, 50, 800, 600, "Ntk widget positioning example")
# set the font for all children
winMain.config_children(Ntk.NtkLabel, relief=RIDGE, font=("Arial", 10))

# create the children
lab1 = Ntk.NtkLabel(winMain, 0, 0, 600, 50, pad=(10, 5), content=STR_LAB1)
lab1.config(bcolor="#A0B0C0")

lab2 = Ntk.NtkLabel(winMain, 0, PACK, "75%", 50, pad=(10, 5), content=STR_LAB2)
lab2.config(bcolor="#F0F080")

lab3 = Ntk.NtkLabel(winMain, 0, PACK, -200, "10%", pad=(10, 5), content=STR_LAB3)
lab3.config(bcolor="#C090E0")

hfr1 = Ntk.NtkHorFrame(winMain, 0, PACK, FILL, 180, content=STR_HOR1)
hfr1.config(bcolor="#C0C070")

lab4 = Ntk.NtkLabel(hfr1, "10%", CENTER, "40%", 80, pad=(5,0), content=STR_LAB4)
lab4.config(bcolor="#E07080")

lab5 = Ntk.NtkLabel(hfr1, PACK, CENTER, "40%", 80, pad=(5, 0), content=STR_LAB5)
lab5.config(bcolor="#20F0C0")

lab6 = Ntk.NtkLabel(winMain, -600, PACK, -100, 60, pad=(0, 10), content=STR_LAB6)
lab6.config(bcolor="#70F060")

lab7 = Ntk.NtkLabel(winMain, 0, -70, FILL, 60, pad=10, content=
                    "Try to resize the window horizontally or vertically")
lab7.config(bcolor="#6090F0", anchor=CENTER)

Ntk.mainloop()