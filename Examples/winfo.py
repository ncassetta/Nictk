from NCtk import *

winfo_options = ["atom", "atomname", "cells", "children", "class", "colormapfull", "containing", 
                 "depth", "exists", "fpixels", "geometry", "height", "id", "interps", "ismapped",
                 "manager", "name", "parent", "pathname", "pixels", "pointerx", "pointerxy",
                 "pointery", "reqheight", "reqwidth", "rgb", "rootx", "rooty", "screen", "screencells",
                 "screendepth", "screenheight", "screenmmheight", "screenmmwidth", "screenvisual",
                 "screenwidth", "server", "toplevel", "viewable", "visual", "visualid", "visualsavailable",
                 "vrootheight", "vrootwidth", "vrootx", "vrooty", "width", "x", "y"]

winMain = NCtkMain(100, 100, 800, 600, title="winfo demo")
labTest = NCtkLabel(winMain, 0, 0, "fill", 50, pad=(30, 10, 30, 10), content="NCtkLabel di prova")
txtTest = NCtkText(winMain, 0, "pack", "fill", "fill", pad=(30, 5, 30, 10))

for opt in winfo_options:
    try:
        output = labTest.getwinfo(opt)
    except TypeError:
        output = "NEEDS PARAM    "
    desc = "winfo_{:20}{:>30}".format(opt + "()", str(output))
    txtTest.settext(txtTest.gettext() + desc)

mainloop()
