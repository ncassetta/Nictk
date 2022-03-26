# Allows import from parent folder. You can delete this if you install the package
import _setup

import Nictk as Ntk
from Nictk.constants import *


#callback for the button
def hide_show(event):
    if labHello.visible():
        labHello.hide()
        btnShow.set_content("Show label")
    else:
        labHello.show()
        btnShow.set_content("Hide label")
        

# Creates the main window (400x300 with left upper corner in (100, 100)
winMain = Ntk.Main(100, 100, 400, 300, title="First Sample")
# Creates a label in it (first argument of children widgets always is the parent,
# subsequent four its dimensions, then other widget specific)
labHello = Ntk.Label(winMain, CENTER, 60, "80%", 100, content="Hello world!")
# Changes label properties: background color, foreground color, font, centered text
labHello.config(bcolor="yellow", fcolor="dark blue", font=("Arial", 32), anchor=CENTER)
# Creates a button, assigning a callback to it
btnShow = Ntk.Button(winMain, CENTER, 200, 100, 40, content="Hide label", command=hide_show) 

#enter the control loop
Ntk.mainloop()