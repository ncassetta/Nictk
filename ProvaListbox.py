from NCtk import *


lines = ("Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto",
         "Nove", "Dieci", "Undici", "Dodici", "Tredici", "Quattordici")
modes = ("single", "browse", "multiple", "extended")
explmodes = ("single mode : you can select only one item at once",
             "browse mode : you can select only an item at once, and \
             drag with the mouse",
             "multiple mode : ",
             "extended mode : ")


def addtolbox(event):
    nitems = lstTest.size()
    if nitems < len(lines):
        lstTest.insert(nitems, lines[nitems])
        
def delfromlbox(event):
    if lstTest.size() > 0:
        lstTest.delete(ACTIVE)

def selchanged(event):
    lstMode.update()
    labExplain.setcontent(explmodes[lstMode.getselected()[0]])
    

winMain = NCtkWindow(200, 150, 400, 300, "NCtkListbox widget sample")
hfr1 = NCtkHorFrame(winMain, 0, 0, "fill", -50)
lstTest = NCtkListbox(hfr1, 0, 0, "50%", "fill", pad=(5, 5))
lstTest.config(bcolor="blue", fcolor="yellow", font=("TkDefaultFont", 12))
vfr1 = NCtkVerFrame(hfr1, "pack", 0,"50%", "fill")
labMode = NCtkLabel(vfr1, 0, 0, "fill", 30, "Listbox Mode", pad=5)
labMode.config(bcolor="light green", fcolor="brown", relief=FLAT, anchor=CENTER)
lstMode = NCtkListbox(vfr1, 0, "pack", "fill", 80, command=selchanged, items=modes)
lstMode.config(font=("TkDefaultFont", 12), relief=FLAT)
hfr1 = NCtkHorFrame(winMain, 0, "pack", "50%", 50)
butAdd = NCtkButton(hfr1, 0, "pack", 80, 40, "Add item", addtolbox, pad=(5,5)) 
butDel = NCtkButton(hfr1, "pack", "pack", 80, 40, "Del item", delfromlbox, pad=(5,5))


labExplain=NCtkLabel(vfr1, 0, "pack", "fill", "fill", explmodes[0])
labExplain.config(anchor=NW)
print (labExplain.getwinfo("fpixels", 20))

mainloop()