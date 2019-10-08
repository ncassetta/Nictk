from NCtk import *

def hitmenu(item):
    labText.settext("You have chosen '" + item + "' from the menu in the menubar")

def hitpopup(item):
    labText.settext("You have chosen '" + item + "' from the popup menu")

def hitcombo(item):
    labText.settext("You have chosen '" + item + "' from the combobox")

def popup(event):
    menuPopup.post(event.x_root, event.y_root)
    


winMain = NCtkWindow(200, 180, 640, 480, "Menu example")
#winMain.config(bcolor="pink")
menuBar = NCtkMenu(winMain)
menuFile = NCtkMenu(menuBar)
menuFile.add_command(label="Open", command=hitmenu)
menuFile.add_command(label="Save", command=hitmenu)
menuFile.add_command(label="Save as ...", command=hitmenu)
menuFile.add_separator()
menuFile.add_command(label="Quit", command=hitmenu)
menuFile.entryconfig(34, fcolor="red")
menuBar.add_cascade(label="File", menu=menuFile)
winMain.config(menu=menuBar)
menuEdit = NCtkMenu(menuBar)
menuEdit.add_checkbutton(label="Edit on", command=hitmenu)
menuBar.add_cascade(label="Edit", command=menuEdit)
opt = menuFile.entrygetconfig("Open", "state")

menuPopup = NCtkMenu(winMain)
menuPopup.add_command(label="Cut", command=hitpopup)
menuPopup.add_command(label="Copy", command=hitpopup)
menuPopup.add_command(label="Paste", command=hitpopup)

labPopup=NCtkLabel(winMain, 0, "10%", "fill", 100, "Double click to open a popup", (10, 10 , 20, 5))
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