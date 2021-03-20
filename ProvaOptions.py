from NCtk import *
from tkinter import font
from random import randrange

COLORS = ("white", "green", "blue", "yellow", "pink", "grey", "black",
          "cyan", "red", "orange", "gold", "magenta", "purple")
RELIEFS = (SUNKEN, FLAT, RAISED, GROOVE, RIDGE)
ANCHORS = (N, E, NW, SE, S, SW, W, NE, CENTER)
JUSTIFIES = (LEFT, CENTER, RIGHT)
CURSORS = ("arrow", "circle", "clock", "cross", "dotbox", "exchange",
           "fleur", "heart", "man", "mouse", "pirate", "plus",
           "shuttle", "sizing", "spider", "spraycan", "target",
           "tcross", "trek", "watch")


def changeBgcolor(event):
    butBgcolor.index = (butBgcolor.index + 1) % len(COLORS)
    col = COLORS[butBgcolor.index]
    labSample.config(bcolor=col)
    labBgcolor.config(text="Background color: " + col)
    
def changeFgcolor(event):
    butFgcolor.index = (butFgcolor.index + 1) % len(COLORS)
    col = COLORS[butFgcolor.index]
    labSample.config(fcolor=col)
    labFgcolor.config(text="Foreground color: " + col)

def changeRelief(event):
    butRelief.index = (butRelief.index + 1) % 5
    r = RELIEFS[butRelief.index]
    labSample.config(relief=r)
    labRelief.config(text="Relief: " + r)

def changeBorder(event):
    butBorder.index = (butBorder.index + 1) % 6
    b = butBorder.index + 1
    labSample.config(borderwidth=b)
    labBorder.config(text="Border width: " + str(b))

def changeAnchor(event):
    butAnchor.index = (butAnchor.index + 1) % len(ANCHORS)
    j = ANCHORS[butAnchor.index]
    labSample.config(anchor=j)
    labAnchor.config(text="Anchor: " + j)
    
def changeJustify(event):
    butJustify.index = (butJustify.index + 1) % 3
    j = JUSTIFIES[butJustify.index]
    labSample.config(justify=j)
    labJustify.config(text="Justify: " + j)

def changeFont(event):
    butFont.index = (butFont.index + 1) % len(FONTS)
    f = FONTS[butFont.index]
    fsize = randrange(8, 18)
    labSample.config(font=(f, fsize))
    labFont.config(text="Font: " + f + " " + str(fsize))
    
def changeCursor(event):
    butCursor.index = (butCursor.index + 1) % len(CURSORS)
    c = CURSORS[butCursor.index]
    labSample.config(cursor=c)
    labCursor.config(text="Cursor: " + c)

winMain = NCtkMain(200, 180, 640, 480, "Widget attributes")
labSample = NCtkLabel(winMain, 0, 0, "fill", 80, pad=10, content="This is a sample, because\nit demonstrates widget options")
# you must have an already created window to get fonts
FONTS = font.families()[:min(15, len(font.families()))]
winMain.config_all("NCtkLabel", background="white", relief=RIDGE)

hfr1 = NCtkHorFrame(winMain, "pack", "pack", "fill", 30)
butBgcolor = NCtkButton(hfr1, "pack", "pack", "15%", "fill", (2, 3, 2, 1),
                        content="BackgColor", command=changeBgcolor)
butBgcolor.index = 0
labBgcolor = NCtkLabel(hfr1, "pack", "pack", "35%", "fill", 2)
butFgcolor = NCtkButton(hfr1, "pack", "pack", "15%", "fill", 2, "ForegColor", changeFgcolor)
butFgcolor.index = 0
labFgcolor = NCtkLabel(hfr1, "pack", "pack", "35%", "fill", 2)

hfr2 = NCtkHorFrame(winMain, "pack", "pack", "fill", 30)
butRelief = NCtkButton(hfr2, "pack", "pack", "15%", "fill", 2, "Relief", changeRelief)
butRelief.index = 0
labRelief = NCtkLabel(hfr2, "pack", "pack", "35%", "fill", 2)
butBorder = NCtkButton(hfr2, "pack", "pack", "15%", "fill", 2, "Border", changeBorder)
butBorder.index = 0
labBorder = NCtkLabel(hfr2, "pack", "pack", "35%", "fill", 2,)

hfr3 = NCtkHorFrame(winMain, "pack", "pack", "fill", 30)
butAnchor = NCtkButton(hfr3, "pack", "pack", "15%", "fill", 2, "Anchor", changeAnchor)
butAnchor.index = 0
labAnchor = NCtkLabel(hfr3, "pack", "pack", "35%", "fill", 2)
butJustify = NCtkButton(hfr3, "pack", "pack", "15%", "fill", 2, "Justify", changeJustify)
butJustify.index = 0
labJustify = NCtkLabel(hfr3, "pack", "pack", "35%", "fill", 2)

hfr4 = NCtkHorFrame(winMain, "pack", "pack", "fill", 30)
butFont = NCtkButton(hfr4, "pack", "pack", "15%", "fill", 2, "Font", changeFont)
butFont.index = 0
labFont = NCtkLabel(hfr4, "pack", "pack", "35%", "fill", 2)
butCursor = NCtkButton(hfr4, "pack", "pack", "15%", "fill", 2, "Cursor", changeCursor)
butCursor.index = 0
labCursor = NCtkLabel(hfr4, "pack", "pack", "35%", "fill", 2)

mainloop()