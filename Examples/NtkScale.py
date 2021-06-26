import _setup           # allows import from parent folder
from Ntk import *


def changecolor(event):
    """This is called when you move one fo the scales. It changes
    the color of the right label background according to their
    values."""
    R, G, B = int(sclRed.getcontent()), int(sclGreen.getcontent()), int(sclBlue.getcontent())
    deccolor = "({:3d}, {:3d}, {:3d})".format(R, G, B)
    # gets the string for config "#RRGGBB"
    hexcolor = "#{:02X}{:02X}{:02X}".format(R, G, B)
    labColor.config(bcolor=hexcolor)
    # sets the text color white if background is dark or black if it is light
    labfg = "white" if (R + G + B) / 3 < 90 else "black"
    labColor.config(fcolor=labfg)
    labColor.setcontent("Color:\n" + deccolor)


winMain = NtkMain(200, 150, 400, 300, "Scale widget sample")
winMain.config_children(ALL, relief="solid", borderwidth=1)

# vertical frame for aligning the three scales and their labels in the left side
vfr1 = NtkVerFrame(winMain, 0, 0, "50%", FILL)

# red label and scale
labRed = NtkLabel(vfr1, 0, 0, FILL, 45, pad=(10, 15, 20, 5), content="Red")  
sclRed = NtkScale(vfr1, 0, PACK, FILL, 50, pad=(10, 0, 20, 5),limits=(0,255,1), command=changecolor)
# bcolor: background and non selected cursor color
# tcolor (through color): color of the cursor guide
# abcolor: (activebackground color): color of the selected cursor
sclRed.config(bcolor="red", tcolor="#FF8080", abcolor="#FFA0A0")

# green label and scale
labGreen = NtkLabel(vfr1, 0, PACK, FILL, 45, pad=(10, 15, 20, 5), content="Green")  
sclGreen = NtkScale(vfr1, 0, PACK, FILL, 50, pad=(10, 0, 20, 5),limits=(0,255,1), command=changecolor)
sclGreen.config(bcolor="green", tcolor="#80FF80", abcolor="#A0FFA0")

# blue label and scale
labBlue = NtkLabel(vfr1, 0, PACK, FILL, 45, pad=(10, 15, 20, 5), content="Blue")  
sclBlue = NtkScale(vfr1, 0, PACK, FILL, 50, pad=(10, 0, 20, 5),limits=(0,255,1), command=changecolor)
sclBlue.config(bcolor="blue", tcolor="#8080FF", abcolor="#A0A0FF")

# color label in the right side
labColor = NtkLabel(winMain, "50%", 0, FILL, FILL, pad=15)
labColor.config(anchor=CENTER, justify=CENTER)

# call the callback for setting initial color to black
changecolor(None)

mainloop()