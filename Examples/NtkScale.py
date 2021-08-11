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


def changecolor(event):
    """This is called when you move one fo the scales. It changes
    the color of the right label background according to their
    values."""
    R, G, B = int(sclRed.get_value()), int(sclGreen.get_value()), int(sclBlue.get_value())
    # string in decimal values "(R, G, B)" to be shown in the label
    deccolor = "({:3d}, {:3d}, {:3d})".format(R, G, B)
    # string in hex values for config "#RRGGBB"
    hexcolor = "#{:02X}{:02X}{:02X}".format(R, G, B)
    # changes the background color 
    labColor.config(bcolor=hexcolor)
    # sets the text color white if background is dark or black if it is light
    labfg = "white" if (R + G + B) / 3 < 90 else "black"
    labColor.config(fcolor=labfg)
    labColor.set_content("Color:\n" + deccolor)


winMain = Ntk.NtkMain(200, 150, 400, 300, "Scale widget sample")
winMain.config_children(ALL, relief="solid", borderwidth=1, anchor=CENTER)

# vertical frame for aligning the three scales and their labels in the left side
vfr1 = Ntk.NtkVerFrame(winMain, 0, 0, "50%", FILL)

# red label and scale
labRed = Ntk.NtkLabel(vfr1, 0, 0, FILL, 45, pad=(10, 15, 20, 5), content="Red")  
sclRed = Ntk.NtkScale(vfr1, 0, PACK, FILL, 50, pad=(10, 0, 20, 5),
                      limits=(0,255,1), command=changecolor)
# bcolor: background and non selected cursor color
# tcolor (through color): color of the cursor guide
# abcolor: (activebackground color): color of the selected cursor
sclRed.config(bcolor="red", tcolor="#FF8080", abcolor="#FFA0A0")

# green label and scale
labGreen = Ntk.NtkLabel(vfr1, 0, PACK, FILL, 45, pad=(10, 15, 20, 5),
                        content="Green")  
sclGreen = Ntk.NtkScale(vfr1, 0, PACK, FILL, 50, pad=(10, 0, 20, 5),
                    limits=(0,255,1), command=changecolor)
sclGreen.config(bcolor="green", tcolor="#80FF80", abcolor="#A0FFA0")

# blue label and scale
labBlue = Ntk.NtkLabel(vfr1, 0, PACK, FILL, 45, pad=(10, 15, 20, 5),
                       content="Blue")  
sclBlue = Ntk.NtkScale(vfr1, 0, PACK, FILL, 50, pad=(10, 0, 20, 5),
                       limits=(0,255,1), command=changecolor)
sclBlue.config(bcolor="blue", tcolor="#8080FF", abcolor="#A0A0FF")

# color label in the right side
labColor = Ntk.NtkLabel(winMain, "50%", 0, FILL, FILL, pad=15)
labColor.config(anchor=CENTER, justify=CENTER)

# call the callback for setting initial color to black
changecolor(None)

Ntk.mainloop()