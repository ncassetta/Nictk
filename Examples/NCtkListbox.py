import _setup           # allows import from parent folder
from NCtk import *


# items to be added to the listbox (italian numbers)
lines = ("Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto",
         "Nove", "Dieci", "Undici", "Dodici", "Tredici", "Quattordici")
# selection modes
modes = ("single", "browse", "multiple", "extended")
# explanations of selection modes
explmodes = ("single mode : you can select only one item at once, clicking on it in the listbox",
             "browse mode : you can select only an item at once, clicking on it or dragging with the mouse",
             "multiple mode : you can select multiple items, clicking on them; clicking on a selected item " +
             "unselects it",
             "extended mode : you can select multiple items, clicking, dragging the mouse and using the" +
             "<CTRL> or <SHIFT> keys")


def addtolbox(event):
    """Adds an item to the left listbox."""
    nitems = lstTest.size()
    if nitems < len(lines):
        lstTest.insert(nitems, lines[nitems])
        
def delfromlbox(event):
    """ Deletes an item from the left listbox."""
    if lstTest.size() > 0:
        lstTest.delete(END)
        testchanged(None)
        
        
def testchanged(event):
    """Callback called when you select one or more item in the left listbox."""
    sel = lstTest.getselected()
    #print("testchanged with index", sel)
    if len(sel) == 0:
        s = "none"
    else:
        s = ""
        for i in sel:
            s += "{}, ".format(i)
        s = s[:-2]
    labSel.setcontent("Selected index: " + s if len(sel) <= 1 else "Selected indexes: " + s) 

def selchanged(event):
    """Callback called when the user modifies the selection mode."""
    #lstTest.select_clear(0, END)
    testchanged(None)
    sel = lstMode.getselected()
    #print("selchanged() called with index", sel)
    if len(sel):
        labExplain.setcontent(explmodes[sel[0]])
        lstTest.config(selectmode=modes[sel[0]])
    

winMain = NCtkMain(200, 150, 600, 450, "NCtkListbox widget sample")
hfr1 = NCtkHorFrame(winMain, 0, 0, "fill", "fill")
rfr1 = NCtkRowFrame(hfr1, 0, 0, "50%", "fill")
vfr2 = NCtkVerFrame(hfr1, "pack", 0, "fill", "fill")
rfr1.add_row(40)
labTest = NCtkLabel(rfr1, 0, 0, "fill", "fill", pad=(10, 10, 10, 5), content="Try to select items")
labTest.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1, anchor=CENTER)
rfr1.add_row(-80)
lstTest = NCtkListbox(rfr1, 0, 0, "fill", "fill", pad=(10, 5, 10, 40), command=testchanged)
lstTest.config(bcolor="blue", fcolor="yellow", sfcolor="maroon", sbcolor="light blue", 
               relief=RIDGE, font=("TkDefaultFont", 14))
rfr1.add_row(40)
labSel = NCtkLabel(rfr1, 0, 0, "fill", "fill", pad=(10, 5))
labSel.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1)
testchanged(None)
rfr1.add_row("fill")
butAdd = NCtkButton(rfr1, "15%", 0, "35%", "fill", pad=(5,5, 5, 10), content="Add item",
                    command=addtolbox) 
butDel = NCtkButton(rfr1, "pack", "pack", "35%", "fill", pad=(5, 5, 5, 10), content="Del item",
                    command =delfromlbox)
labMode = NCtkLabel(vfr2, 0, 0, "fill", 40, pad=(10, 10, 10, 5), content="Listbox Mode")
labMode.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1, anchor=CENTER)
lstMode = NCtkListbox(vfr2, 0, "pack", "fill", 120, pad=(10, 5), command=selchanged, items=modes)
lstMode.config(bcolor="cyan", fcolor="brown", font=("TkDefaultFont", 14), relief=RIDGE)
labExplain=NCtkLabel(vfr2, 0, "pack", "fill", "fill", pad=(10, 10), content=explmodes[0])
labExplain.config(anchor=NW)
lstMode.select(0)
#print (labExplain.getwinfo("fpixels", 20))

#winMain._draw_children()

mainloop()
