from Ntk import *

winfo_options = ["atom", "atomname", "cells", "children", "class", "colormapfull", "containing", 
                 "depth", "exists", "fpixels", "geometry", "height", "id", "interps", "ismapped",
                 "manager", "name", "parent", "pathname", "pixels", "pointerx", "pointerxy",
                 "pointery", "reqheight", "reqwidth", "rgb", "rootx", "rooty", "screen", "screencells",
                 "screendepth", "screenheight", "screenmmheight", "screenmmwidth", "screenvisual",
                 "screenwidth", "server", "toplevel", "viewable", "visual", "visualid", "visualsavailable",
                 "vrootheight", "vrootwidth", "vrootx", "vrooty", "width", "x", "y"]

winMain = NtkMain(100, 100, 800, 600, title="winfo demo")
labTest = NtkLabel(winMain, 0, 0, "fill", 50, pad=(30, 10, 30, 10), content="NtkLabel di prova")
txtTest = NtkText(winMain, 0, "pack", "fill", "fill", pad=(30, 5, 30, 10))

for opt in winfo_options:
    try:
        output = labTest.getwinfo(opt)
    except TypeError:
        output = "NEEDS PARAM    "
    desc = "winfo_{:20}{:>30}".format(opt + "()", str(output))
    txtTest.settext(txtTest.gettext() + desc)

mainloop()
