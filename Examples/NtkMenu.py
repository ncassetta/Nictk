import _setup           # allows import from parent folder
from Ntk import *


# callbacks (you may prefer to use lambdas)
def hitmenu(event):
    labText.setcontent("You have chosen '" + event.value + "' from the menu in the menubar")
    
def hitmenubutton(event):
    labText.setcontent("Edit is " + editon.get())
    
def hitcolors(event):
    labText.config(bcolor=event.value)

def hitpopup(event):
    labText.setcontent("You have chosen '" + event.value + "' from the popup menu")

def hitcombo(event):
    labText.setcontent("You have chosen '" + event.value + "' from the combobox")
    


winMain = NtkMain(200, 180, 640, 480, "Menu example")
winMain.config_children(NtkLabel, relief=SOLID, borderwidth=1)
# menu bar (auto added to the parent winMain)
menuBar = NtkMenu(winMain)
# first menu (auto added to the parent menuBar)
menuFile = NtkMenu(menuBar, "File")
menuFile.add_command(label="Open", command=(hitmenu, "Open"))
menuFile.add_command(label="Save", command=(hitmenu, "Save"))
menuFile.add_command(label="Save as ...", command=(hitmenu, "Save as ..."))
menuFile.add_separator()
menuFile.add_command(label="Quit", command=lambda event: winMain.destroy())
# second menu (auto added to the parent menuBar)
menuEdit = NtkMenu(menuBar, "Edit")
menuEdit.add_checkbutton(label="Edit on", command=hitmenubutton)
# sets the variable for the checkbutton (you can use as index the number (from 0)
# or the label
editon = tk.StringVar()
menuEdit.entrysetvariable("Edit on", variable=editon, offvalue="off", onvalue="on")
# third menu
menuColors = NtkMenu(menuBar, "Colors")
menuColors.add_command(label="Change to green", command=(hitcolors, "light green"))
menuColors.add_command(label="Change to pink", command=(hitcolors, "pink"))
menuColors.add_command(label="Change to blue", command=(hitcolors, "light blue"))
# menu entries option config. You can use as index the number (from 0) or the label
menuColors.entryconfig(0, bcolor="light green")
menuColors.entryconfig(1, bcolor="pink")
menuColors.entryconfig(2, bcolor="light blue")

# popup menu (not added to the parent because popup is True)
menuPopup = NtkMenu(winMain, popup=True)
menuPopup.add_command(label="Cut", command=(hitpopup, "Cut"))
menuPopup.add_command(label="Copy", command=(hitpopup, "Copy"))
menuPopup.add_command(label="Paste", command=(hitpopup, "Paste"))

# creates the upper label and binds double click on it to popup opening
labPopup=NtkLabel(winMain, 0, "10%", "fill", 100, pad=(15, 10), content="Double click to open a popup", )
labPopup.bind("<Double-Button-1>", lambda event: menuPopup.post(event.x_root, event.y_root))
labPopup.config(bcolor="orange", anchor=CENTER, font=("Arial", 12, "bold"))

#creates the middle Combobox
cmbmenu = ["Option " + str(i + 1) for i in range(100)]
cmbSample = NtkCombobox(winMain, CENTER, PACK, "80%", 50, pad=(0, 5), values=cmbmenu, command=hitcombo)
cmbSample.config(fcolor="dark blue", afcolor="blue", font=("Arial", 12, "bold"))

#creates the lower label
labText = NtkLabel(winMain, PACK, PACK, FILL, FILL, pad=(15, 10))
labText.config(bcolor="light green", fcolor="dark green", font=("Arial", 16), anchor=CENTER)


mainloop()