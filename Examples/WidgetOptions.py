import _setup           # allows import from parent folder
import Ntk
from tkinter import font
from random import randrange

COLORS = ("white", "green", "blue", "yellow", "pink", "grey", "black",
          "cyan", "red", "orange", "gold", "magenta", "purple")
RELIEFS = ("sunken", "flat", "raised", "groove", "ridge", "solid")
ANCHORS = ("n", "e", "nw", "se", "s", "sw", "w", "ne", "center")
JUSTIFIES = ("left", "center", "right")
CURSORS = ("arrow", "circle", "clock", "cross", "dotbox", "exchange",
           "fleur", "heart", "man", "mouse", "pirate", "plus",
           "shuttle", "sizing", "spider", "spraycan", "target",
           "tcross", "trek", "watch")


# callbacks (you may prefer to use lambdas)
def change_bgcolor(event):
    labSample.config(bcolor=spbBgcolor.get_content())

    
def change_fgcolor(event):
    labSample.config(fcolor=spbFgcolor.get_content())


def change_relief(event):
    labSample.config(relief=spbRelief.get_content())


def change_border(event):
    labSample.config(borderwidth=int(spbBorder.get_content()))


def change_anchor(event):
    labSample.config(anchor=spbAnchor.get_content())

    
def change_justify(event):
    labSample.config(justify=spbJustify.get_content())


def change_font(event):
    fsize = randrange(12, 25)
    labSample.config(font=(spbFont.get_content(), fsize))
    
def change_cursor(event):
    labSample.config(cursor=spbCursor.get_content())
    

# create the main window
winMain = Ntk.NtkMain(200, 180, 640, 480, "Widget attributes")
# fill it with a rowframe
rfr1 = Ntk.NtkRowFrame(winMain, 0, 0, "fill", "fill")
# main label with the sample phrase
rfr1.add_row(120)
labSample = Ntk.NtkLabel(rfr1, 0, 0, "fill", "fill", pad=10,
                         content="This is a sample, because\nit demonstrates widget options")
# you must have an already created window to get fonts
FONTS = font.families()[:min(15, len(font.families()))]
# config other children widgets
rfr1.config_children(Ntk.NtkLabel, bcolor="#E0F0C0", relief="solid", border=1)
rfr1.config_children(Ntk.NtkSpinbox, rbcolor="#A0C0D0", relief="ridge", state="readonly")

# other widgets
rfr1.add_row(50)
rfr1.add_row(34)
labBgcolor = Ntk.NtkLabel(rfr1, 0, 0, "20%", "fill", pad=(10,2,2,2), content="bcolor")
spbBgcolor = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=COLORS,
                            command=change_bgcolor)
labFgcolor = Ntk.NtkLabel(rfr1, "pack", 0, "20%", "fill", pad=(10,2,2,2), content="fcolor")
spbFgcolor = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=COLORS,
                            command=change_fgcolor)

rfr1.add_row(34)
labRelief = Ntk.NtkLabel(rfr1, 0, 0, "20%", "fill", pad=(10,2,2,2), content="relief")
spbRelief = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=RELIEFS,
                           command=change_relief)
labBorder = Ntk.NtkLabel(rfr1, "pack", 0, "20%", "fill", pad=(10,2,2,2), content="border")
spbBorder = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=(0, 6, 1),
                           command=change_border)

rfr1.add_row(34)
labAnchor = Ntk.NtkLabel(rfr1, 0, 0, "20%", "fill", pad=(10,2,2,2), content="anchor")
spbAnchor = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=ANCHORS,
                           command=change_anchor)
labJustify = Ntk.NtkLabel(rfr1, "pack", 0, "20%", "fill", pad=(10,2,2,2), content="justify")
spbJustify = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=JUSTIFIES,
                            command=change_justify)

rfr1.add_row(34)
labFont = Ntk.NtkLabel(rfr1, 0, 0, "20%", "fill", pad=(10,2,2,2), content="font")
spbFont = Ntk.NtkSpinbox(rfr1, "pack", 0, "30%", "fill", pad=(2,2,10,2), limits=FONTS,
                         command=change_font)
labCursor = Ntk.NtkLabel(rfr1, "pack", 0, "20%", "fill", pad=(10,2,2,2), content="cursor")
spbCursor = Ntk.NtkSpinbox(rfr1, "pack", "pack", "30%", "fill", pad=(2,2,10,2), limits=CURSORS,
                           command=change_cursor)

# call the callbacks to set initial values
change_anchor(None)
change_bgcolor(None)
spbBorder.set_content("2")
change_cursor(None)
spbFgcolor.invoke("buttonup")
change_font(None)
change_justify(None)
change_relief(None)

Ntk.mainloop()