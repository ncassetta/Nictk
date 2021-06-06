import _setup           # allows import from parent folder
from NCtk import *


def changecolor(event):
    R, G, B = int(sclRed.getcontent()), int(sclGreen.getcontent()), int(sclBlue.getcontent())
    deccolor = "({:3d}, {:3d}, {:3d})".format(R, G, B)
    hexcolor = "#{:02X}{:02X}{:02X}".format(R, G, B)
    labColor.config(bcolor=hexcolor)
    labfg = "white" if (R + G + B) / 3 < 90 else "black"
    labColor.config(fcolor=labfg)
    labColor.setcontent("Color:\n" + deccolor)


winMain = NCtkMain(200, 150, 400, 300, "Scale widget sample")
winMain.config_children("all", relief="solid", borderwidth=1)
vfr1 = NCtkVerFrame(winMain, 0, 0, "50%", "fill")
labRed = NCtkLabel(vfr1, 0, 0, "fill", 45, pad=(10, 15, 20, 5), content="Red")  
sclRed = NCtkScale(vfr1, 0, "pack", "fill", 50, pad=(10, 0, 20, 5),limits=(0,255,1), command=changecolor)
sclRed.config(bcolor="red", tcolor="#FF8080")
labGreen = NCtkLabel(vfr1, 0, "pack", "fill", 45, pad=(10, 15, 20, 5), content="Green")  
sclGreen = NCtkScale(vfr1, 0, "pack", "fill", 50, pad=(10, 0, 20, 5),limits=(0,255,1), command=changecolor)
sclGreen.config(bcolor="green", tcolor="#80FF80")
labBlue = NCtkLabel(vfr1, 0, "pack", "fill", 45, pad=(10, 15, 20, 5), content="Blue")  
sclBlue = NCtkScale(vfr1, 0, "pack", "fill", 50, pad=(10, 0, 20, 5),limits=(0,255,1), command=changecolor)
sclBlue.config(bcolor="blue", tcolor="#8080FF")
labColor = NCtkLabel(winMain, "50%", 0, "fill", "fill", pad=15)
labColor.config(anchor=CENTER, justify=CENTER)
changecolor(None)


mainloop()