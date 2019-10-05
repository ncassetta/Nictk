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
    labExplain.settext(explmodes[lstMode.getselected()[0]])
    

winMain = NCtkWindow(200, 150, 400, 300, "App prova")
lstTest = NCtkListbox(winMain, 10, 10, 170, 200)
lstTest.config(bcolor="blue", fcolor="yellow", font=("TkDefaultFont", 12))
labMode = NCtkLabel(winMain, 200, 10, 150, 20, "Listbox Mode")
labMode.config(bcolor="light green", fcolor="brown", relief=FLAT, anchor=CENTER)
lstMode = NCtkListbox(winMain, 200, 40, 150, 100, command=selchanged, items=modes)
lstMode.config(font=("TkDefaultFont", 12), relief=FLAT)
butAdd = NCtkButton(winMain, 10, 240, 80, 50, "Add item", addtolbox) 
butDel = NCtkButton(winMain, 100, 240, 80, 50, "Del item", delfromlbox)
labExplain=NCtkLabel(winMain, 200, 150, 150, 140, explmodes[0])
labExplain.config(anchor=NW)
print (labExplain.getwinfo("fpixels", 20))

mainloop()