from NCtk import *

def popup(event):
    menuPopup.post(event.x_root, event.y_root)

winMain = NCtkWindow(200, 180, 640, 480, "Menu example")
menuBar = NCtkMenu(winMain)
menuFile = NCtkMenu(menuBar)
menuFile.add_command(label="Open")
menuFile.add_command(label="Save")
menuFile.add_command(label="Save as ...")
menuFile.add_separator()
menuFile.add_command(label="Quit")
menuBar.add_cascade(label="File", menu=menuFile)
winMain.config(menu=menuBar)
menuEdit = NCtkMenu(menuBar)
menuEdit.add_checkbutton(label="Edit on")
menuBar.add_cascade(label="Edit", menu=menuEdit)

menuPopup = NCtkMenu(winMain)
menuPopup.add_command(label="Cut")
menuPopup.add_command(label="Copy")
menuPopup.add_command(label="Paste")

labSample=NCtkLabel(winMain, 0, 200, "fill", 50, "Double click to open a popup")
labSample.bind("<Double-Button-3>", popup)


mainloop()