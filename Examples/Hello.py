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


#callback for the button
def hide_show(event):
    if labHello.visible():
        labHello.hide()
        btnShow.set_content("Show label")
    else:
        labHello.show()
        btnShow.set_content("Hide label")
        

# Creates the main window (400x300 with left upper corner in (100, 100)
winMain = Ntk.Main(100, 100, 400, 300, title="First Sample")
# Creates a label in it (first argument of children widgets always is the parent,
# subsequent four its dimensions, then other widget specific)
labHello = Ntk.Label(winMain, CENTER, 60, "80%", 100, content="Hello world!")
# Changes label properties: background color, foreground color, font, centered text
labHello.config(bcolor="yellow", fcolor="dark blue", font=("Arial", 32), anchor=CENTER)
# Creates a button, assigning a callback to it
btnShow = Ntk.Button(winMain, CENTER, 200, 100, 40, content="Hide label", command=hide_show) 

#enter the control loop
Ntk.mainloop()