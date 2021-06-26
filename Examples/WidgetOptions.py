import _setup           # allows import from parent folder
from Ntk import *
from tkinter import font
from random import randrange

COLORS = ("white", "green", "blue", "yellow", "pink", "grey", "black",
          "cyan", "red", "orange", "gold", "magenta", "purple")
RELIEFS = (SUNKEN, FLAT, RAISED, GROOVE, RIDGE, SOLID)
ANCHORS = (N, E, NW, SE, S, SW, W, NE, CENTER)
JUSTIFIES = (LEFT, CENTER, RIGHT)
CURSORS = ("arrow", "circle", "clock", "cross", "dotbox", "exchange",
           "fleur", "heart", "man", "mouse", "pirate", "plus",
           "shuttle", "sizing", "spider", "spraycan", "target",
           "tcross", "trek", "watch")


def changeBgcolor(event):
    labSample.config(bcolor=spbBgcolor.getcontent())
    
def changeFgcolor(event):
    labSample.config(fcolor=spbFgcolor.getcontent())

def changeRelief(event):
    labSample.config(relief=spbRelief.getcontent())

def changeBorder(event):
    labSample.config(borderwidth=int(spbBorder.getcontent()))

def changeAnchor(event):
    labSample.config(anchor=spbAnchor.getcontent())
    
def changeJustify(event):
    labSample.config(justify=spbJustify.getcontent())

def changeFont(event):
    fsize = randrange(12, 25)
    labSample.config(font=(spbFont.getcontent(), fsize))
    
def changeCursor(event):
    labSample.config(cursor=spbCursor.getcontent())
    

# create the main window
winMain = NtkMain(200, 180, 640, 480, "Widget attributes")

# fill it with a rowframe
rfr1 = NtkRowFrame(winMain, 0, 0, "fill", "fill")

# main label with the sample phrase
rfr1.add_row(120)
labSample = NtkLabel(rfr1, 0, 0, "fill", "fill", pad=10,
                      content="This is a sample, because\nit demonstrates widget options")

# you must have an already created window to get fonts
FONTS = font.families()[:min(15, len(font.families()))]

# config other children widgets
rfr1.config_children(NtkLabel, bcolor="#E0F0C0", relief=SOLID, border=1)
rfr1.config_children(NtkSpinbox, readonlybackground="#A0C0D0", relief=RIDGE, state="readonly")

# other widgets
rfr1.add_row(16)
rfr1.add_row(34)
labBgcolor = NtkLabel(rfr1, 0, 0, "20%", FILL, pad=(10,2,2,2), content="bcolor")
spbBgcolor = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=COLORS, command=changeBgcolor)
labFgcolor = NtkLabel(rfr1, PACK, 0, "20%", FILL, pad=(10,2,2,2), content="fcolor")
spbFgcolor = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=COLORS, command=changeFgcolor)
rfr1.add_row(34)
labRelief = NtkLabel(rfr1, 0, 0, "20%", FILL, pad=(10,2,2,2), content="relief")
spbRelief = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=RELIEFS, command=changeRelief)
labBorder = NtkLabel(rfr1, PACK, 0, "20%", FILL, pad=(10,2,2,2), content="border")
spbBorder = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=(0, 6, 1), command=changeBorder)
rfr1.add_row(34)
labAnchor = NtkLabel(rfr1, 0, 0, "20%", FILL, pad=(10,2,2,2), content="anchor")
spbAnchor = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=ANCHORS, command=changeAnchor)
labJustify = NtkLabel(rfr1, PACK, 0, "20%", FILL, pad=(10,2,2,2), content="justify")
spbJustify = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=JUSTIFIES, command=changeJustify)
rfr1.add_row(34)
labFont = NtkLabel(rfr1, 0, 0, "20%", FILL, pad=(10,2,2,2), content="font")
spbFont = NtkSpinbox(rfr1, PACK, 0, "30%", FILL, pad=(2,2,10,2), limits=FONTS, command=changeFont)
labCursor = NtkLabel(rfr1, PACK, 0, "20%", FILL, pad=(10,2,2,2), content="cursor")
spbCursor = NtkSpinbox(rfr1, PACK, PACK, "30%", FILL, pad=(2,2,10,2), limits=CURSORS, command=changeCursor)

changeAnchor(None)
changeBgcolor(None)
spbBorder.setcontent(2)
changeCursor(None)
spbFgcolor.invoke("buttonup")
changeFont(None)
changeJustify(None)
changeRelief(None)

mainloop()