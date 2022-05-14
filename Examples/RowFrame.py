# This file is part of Nictk - A simple tkinter wrapper.
#    Copyright (C) 2021  Nicola Cassetta
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

# TODO: advice that you programmatically don't use constants


winMain = Ntk.Main(200, 150, 400, 300, "NtkRowFrame sample")
rfr1 = Ntk.RowFrame(winMain, 0, 0, "fill", "fill")
rfr1.config_children(Ntk.Label, relief="solid", bcolor = "blue", fcolor="yellow",
                     anchor="center")
# In this example we have added all rows, and then selected them with set_active.
# Is more common to add a row at a time (which sets it as active) and then add
# widgets to it

# fixed vertical size
rfr1.add_row(30)
# percent vertical size
rfr1.add_row("30%")
# percent vertical size
rfr1.add_row("30%")
# fixed from bottom vertical size
rfr1.add_row(-10)

# "pack" == PACK and "fill" == FILL
rfr1.set_active(0)
lab1 = Ntk.Label(rfr1, "pack", "20%", "30%", "fill", pad=(10, 0), content="A label in row 0")
lab2 = Ntk.Label(rfr1, "pack", "20%", "50%", "fill", pad=(10, 0), content="This is a fixed height row")

rfr1.set_active(1)
lab3 = Ntk.Label(rfr1, "pack", "20%", "30%", "60%", pad=(10, 0), content="A label in row 1")
lab4 = Ntk.Label(rfr1, "pack", "20%", "50%", "60%", pad=(10, 0), content="This is a 30% height row")

rfr1.set_active(2)
lab5 = Ntk.Label(rfr1, "pack", "20%", "30%", "60%", pad=(10, 0), content="A label in row 2")
lab6 = Ntk.Label(rfr1, "pack", "20%", "50%", "60%", pad=(10, 0), content="Try to resize the window")

rfr1.set_active(3)
lab7 = Ntk.Label(rfr1, "pack", 10, "30%", -10, pad=(10, 0), content="A label in row 3")
lab8 = Ntk.Label(rfr1, "pack", 10, "50%", -10, pad=(10, 0), content="This is a fixed from bottom height row")

Ntk.mainloop()
