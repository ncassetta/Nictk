import _setup           # allows import from parent folder
from NCtk import *

CITTA = ("Bari", "Bologna", "Firenze", "Milano", "Napoli", "Palermo",
         "Roma", "Torino", "Venezia")


def changeLabel(event):
    sel = event.widget.gettext()
    lab1.setcontent("Selected: " + sel)


winMain = NCtkMain(200, 150, 400, 300, "Combobox sample")
#winMain.config(bcolor="yellow")
cmb = NCtkCombobox(winMain, 0, 0, FILL, 60, pad=10, items=CITTA, command=changeLabel)
lab1 = NCtkLabel(winMain, 0, "pack", "fill", 80, pad=10)
lab1.config(bcolor="#D0B0F0", font = ("Arial", 16), relief=RIDGE)
#chk1 = NCtkCheckbutton(frm1, 0, 0, "30%", "fill", pad=(10, 5),
                       #content="This is a button with pink background", command=changeLabText) 
#chk1.config(bcolor="pink", abcolor="pink")
#chk1.setvariable(but1, "Value: off", "Value: on")
#chk1.select()


mainloop()