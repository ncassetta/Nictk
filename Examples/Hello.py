from NCtk import *

#callback for the button
def hideshow(event):
    if labHello.visible():
        labHello.hide()
        btnShow.setcontent("Show label")
    else:
        labHello.show()
        btnShow.setcontent("Hide label")

# Creates the main window (400x300 with left upper in (100, 100)
winMain = NCtkMain(100, 100, 400, 300, title="First Sample")
# Creates a label in it (first argument of children widgets always is the parent,
# subsequent four its dimensions, then other widget specific)
labHello = NCtkLabel(winMain, CENTER, 40, "80%", 60, content="Hello world!")
# Changes label properties: background color, foreground color, font, centered text
labHello.config(bcolor="yellow", fcolor="blue", font=("Arial", 18), anchor=CENTER)
# Creates a button, assigning a callback to it
btnShow = NCtkButton(winMain, CENTER, 120, 80, 30, content="Hide label", command=hideshow) 

#enter the control loop
mainloop()