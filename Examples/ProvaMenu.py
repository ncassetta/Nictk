import _setup           # allows import from parent folder
from NCtk import *

def hitmenu(item):
    labText.settext("You have chosen '" + item + "' from the menu in the menubar")
    
def hitcolors(item):
    labText.config(bcolor=item)
    
def exit(item):
    winMain.destroy()

def hitpopup(item):
    labText.settext("You have chosen '" + item + "' from the popup menu")

def hitcombo(item):
    labText.settext("You have chosen '" + item + "' from the combobox")

def popup(event):
    menuPopup.post(event.x_root, event.y_root)
    


winMain = NCtkMain(200, 180, 640, 480, "Menu example")
#winMain.config(bcolor="pink")
menuBar = NCtkMenu(winMain)
menuFile = NCtkMenu(menuBar)
menuFile.add_command(label="Open", command=hitmenu)
menuFile.add_command(label="Save", command=hitmenu)
menuFile.add_command(label="Save as ...", command=hitmenu)
menuFile.add_separator()
menuFile.add_command(label="Quit", command=exit)
menuBar.add_cascade(label="File", menu=menuFile)
menuEdit = NCtkMenu(menuBar)
menuEdit.add_checkbutton(label="Edit on", command=hitmenu)
menuBar.add_cascade(label="Edit", menu=menuEdit)
opt = menuFile.entrygetconfig("Open", "state")
menuColors = NCtkMenu(menuBar)
menuColors.add_command(label="Change to green", command=hitcolors, arg="light green")
menuColors.add_command(label="Change to red", command=hitcolors, arg="pink")
menuColors.add_command(label="Change to blue", command=hitcolors, arg="light blue")
menuColors.entryconfig(0, bcolor="light green")
menuColors.entryconfig(1, bcolor="pink")
menuColors.entryconfig(2, bcolor="light blue")
menuBar.add_cascade(label="Colors", menu=menuColors)
winMain.config(menu=menuBar)

menuPopup = NCtkMenu(winMain)
menuPopup.add_command(label="Cut", command=hitpopup)
menuPopup.add_command(label="Copy", command=hitpopup)
menuPopup.add_command(label="Paste", command=hitpopup)

labPopup=NCtkLabel(winMain, 0, "10%", "fill", 100, pad=(10, 10 , 20, 5), content="Double click to open a popup", )
labPopup.bind("<Double-Button-1>", popup)
labPopup.config(bcolor="pink", anchor=CENTER, relief=FLAT, font=("Arial", 12, "bold"))

cmbmenu = ["Option " + str(i + 1) for i in range(100)]
cmbSample = NCtkCombobox(winMain, "pack", "pack", "40%", 40, command=hitcombo, items=cmbmenu)
#cmbSample.update()
opt = cmbSample.entrygetconfig("Option 23", "foreground")

cmbSample.delete(5, 10)
cmbSample.insert(5, "New Option")
cmbSample.entryconfig(8, font="Arial", bcolor="white")
opt = cmbSample.entrycget("Option 23", "state")

labText = NCtkLabel(winMain, "pack", "pack", "fill", "fill", "", (10, 10, 20, 10))
labText.config(bcolor="light green", fcolor="dark green", font=("Arial", 16),
               anchor=CENTER)


mainloop()