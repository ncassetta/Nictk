import _setup           # allows import from parent folder
from Ntk import *


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
    

winMain = NtkMain(200, 150, 600, 450, "NtkListbox widget sample")
hfr1 = NtkHorFrame(winMain, 0, 0, FILL, FILL)
rfr1 = NtkRowFrame(hfr1, 0, 0, "50%", FILL)
vfr2 = NtkVerFrame(hfr1, PACK, 0, FILL, FILL)
rfr1.add_row(40)
labTest = NtkLabel(rfr1, 0, 0, FILL, FILL, pad=(10, 10, 10, 5), content="Try to select items")
labTest.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1, anchor=CENTER)
rfr1.add_row(-80)
lstTest = NtkListbox(rfr1, 0, 0, FILL, FILL, pad=(10, 5, 10, 40), command=testchanged)
lstTest.config(bcolor="blue", fcolor="yellow", sfcolor="maroon", sbcolor="light blue", 
               relief=RIDGE, font=("TkDefaultFont", 14))
rfr1.add_row(40)
labSel = NtkLabel(rfr1, 0, 0, FILL, FILL, pad=(10, 5))
labSel.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1)
testchanged(None)
rfr1.add_row(FILL)
butAdd = NtkButton(rfr1, "15%", 0, "35%", FILL, pad=(5,5, 5, 10), content="Add item",
                    command=addtolbox) 
butDel = NtkButton(rfr1, PACK, PACK, "35%", FILL, pad=(5, 5, 5, 10), content="Del item",
                    command =delfromlbox)
labMode = NtkLabel(vfr2, 0, 0, FILL, 40, pad=(10, 10, 10, 5), content="Listbox Mode")
labMode.config(bcolor="light green", fcolor="blue", relief=SOLID, borderwidth=1, anchor=CENTER)
lstMode = NtkListbox(vfr2, 0, PACK, FILL, 120, pad=(10, 5), command=selchanged, items=modes)
lstMode.config(bcolor="cyan", fcolor="brown", font=("TkDefaultFont", 14), relief=RIDGE)
labExplain=NtkLabel(vfr2, 0, PACK, FILL, FILL, pad=(10, 10), content=explmodes[0])
labExplain.config(anchor=NW)
lstMode.select(0)

mainloop()
