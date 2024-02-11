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

winfo_options = ["atom", "atomname", "cells", "children", "class", "colormapfull", "containing", 
                 "depth", "exists", "fpixels", "geometry", "height", "id", "interps", "ismapped",
                 "manager", "name", "parent", "pathname", "pixels", "pointerx", "pointerxy",
                 "pointery", "reqheight", "reqwidth", "rgb", "rootx", "rooty", "screen", "screencells",
                 "screendepth", "screenheight", "screenmmheight", "screenmmwidth", "screenvisual",
                 "screenwidth", "server", "toplevel", "viewable", "visual", "visualid", "visualsavailable",
                 "vrootheight", "vrootwidth", "vrootx", "vrooty", "width", "x", "y"]

winMain = Ntk.Main(100, 100, 800, 600, title="winfo demo")
labTest = Ntk.Label(winMain, 0, 0, "fill", 50, pad=(30, 10, 30, 10), content="labTest")
txtTest = Ntk.Text(winMain, 0, "pack", "fill", "fill", pad=(30, 5, 30, 10))

for opt in winfo_options:
    try:
        output = labTest.get_winfo(opt)
    except TypeError:
        output = "NEEDS PARAM    "
    desc = "{:40}{:>30}".format('labTest.get_winfo("' + opt + '")', str(output))
    txtTest.append_text(desc + "\n")

Ntk.mainloop()
