import _setup           # allows import from parent folder
from Ntk import *


#callback for the button
def hide_show(event):
    if labHello.visible():
        labHello.hide()
        btnShow.setcontent("Show label")
    else:
        labHello.show()
        btnShow.setcontent("Hide label")
        

# Creates the main window (400x300 with left upper in (100, 100)
winMain = NtkMain(100, 100, 400, 300, title="First Sample")
# Creates a label in it (first argument of children widgets always is the parent,
# subsequent four its dimensions, then other widget specific)
labHello = NtkLabel(winMain, CENTER, 60, "80%", 100, content="Hello world!")
# Changes label properties: background color, foreground color, font, centered text
labHello.config(bcolor="yellow", fcolor="dark blue", font=("Arial", 32), anchor=CENTER)
# Creates a button, assigning a callback to it
btnShow = NtkButton(winMain, CENTER, 200, 100, 40, content="Hide label", command=hide_show) 

#enter the control loop
mainloop()