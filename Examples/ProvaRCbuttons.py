import _setup           # allows import from parent folder
from NCtk import *

def changeLabText(ev):
    if ev.widget == chk1:
        s = "Pink button variable value:     " + chk1Var.get()
    elif ev.widget == chk2:
        s = "Orange button variable value:   " + str(chk2Var.get())
    else:
        s = "Option " + str(optVar.get()) + " selected"
    labSample.setcontent(s)


winMain = NCtkMain(200, 150, 600, 400, "Radio and Check Buttons")
winMain.config(bcolor="#FFFFA0")
winMain.config_children("all", relief=GROOVE)
rfr1 = NCtkRowFrame(winMain, 0, 0, FILL, FILL)
rfr1.add_row(60)
labSample = NCtkLabel(rfr1, 0, 0, FILL, FILL, pad=10)
rfr1.add_row(80)

chk1 = NCtkCheckbutton(rfr1, 0, 0, "40%", FILL, pad=(10, 5, 5, 5),
                       content="This button controls a StrVar, which can get values: 'Value: on' and 'Value: off",
                       command=changeLabText) 
chk1.config(bcolor="pink", abcolor="pink")
chk1Var = StringVar()
chk1.setvariable(chk1Var, "Value: off", "Value: on")
chk1.select()
labChk1 = NCtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 5, 10, 5))
labChk1.config(textvariable=chk1Var)
rfr1.add_row(80)
chk2 = NCtkCheckbutton(rfr1, 0, 0, "40%", FILL, pad=(10, 5, 5, 5),
                       content="This button controls an IntVar, which gan get values: 0 and 1", command=changeLabText)
chk2Var = IntVar()
chk2.config(bcolor="orange", abcolor="orange")
chk2.setvariable(chk2Var, 0, 1)
chk2.deselect()
labChk2 = NCtkLabel(rfr1, PACK ,0 , FILL, FILL, pad=(5, 5, 10, 5))
labChk2.config(textvariable=chk2Var)
optVar = IntVar()
rfr1.add_row(-10)
frm3 = NCtkVerFrame(rfr1, 10, 10, -10, FILL)
frm3.config_children("all", relief=FLAT)
frm3.config(relief=GROOVE)
rad1 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%", command=changeLabText)
rad1.config(variable=optVar, value=1, text = "Option 1")
rad2 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%", command=changeLabText)
rad2.config(variable=optVar, value= 2, text="Option 2")
rad3 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%", command=changeLabText)
rad3.config(variable=optVar, value= 3, text="Option 3")
rad2.invoke()


mainloop()