import _setup           # allows import from parent folder
from Ntk import *

def changeLabText(ev):
    if ev.widget == chk1:
        s = "Pink button variable value:     " + chk1Var.get()
    elif ev.widget == chk2:
        s = "Orange button variable value:   " + str(chk2Var.get())
    else:
        s = "Option " + str(optVar.get()) + " selected"
    labSample.setcontent(s)


winMain = NtkMain(200, 150, 600, 400, "Radio and Check Buttons")
winMain.config(bcolor="#FFFFA0")
winMain.config_children(ALL, relief=GROOVE)
rfr1 = NtkRowFrame(winMain, 0, 0, FILL, FILL)
rfr1.add_row(60)
labSample = NtkLabel(rfr1, 0, 0, FILL, FILL, pad=10)
rfr1.add_row(80)

chk1 = NtkCheckbutton(rfr1, 0, 0, "40%", FILL, pad=(10, 5, 5, 5),
                       content="This button controls a StrVar, which can get values: 'Value: on' and 'Value: off",
                       command=changeLabText) 
chk1.config(bcolor="pink", abcolor="pink")
chk1Var = StringVar()
chk1.setvariable(chk1Var, "Value: off", "Value: on")
chk1.select()
labChk1 = NtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 5, 10, 5))
labChk1.config(textvariable=chk1Var)
rfr1.add_row(80)
chk2 = NtkCheckbutton(rfr1, 0, 0, "40%", FILL, pad=(10, 5, 5, 5),
                       content="This button controls an IntVar, which gan get values: 0 and 1", command=changeLabText)
chk2Var = IntVar()
chk2.config(bcolor="orange", abcolor="orange")
chk2.setvariable(chk2Var, 0, 1)
chk2.deselect()
labChk2 = NtkLabel(rfr1, PACK ,0 , FILL, FILL, pad=(5, 5, 10, 5))
labChk2.config(textvariable=chk2Var)
optVar = IntVar()
rfr1.add_row(-10)
frm3 = NtkVerFrame(rfr1, 10, 10, -10, FILL)
frm3.config_children("all", relief=FLAT)
frm3.config(relief=GROOVE)
rad1 = NtkRadiobutton(frm3, 0, PACK, FILL, "33%", command=changeLabText)
rad1.config(variable=optVar, value=1, text = "Option 1")
rad2 = NtkRadiobutton(frm3, 0, PACK, FILL, "33%", command=changeLabText)
rad2.config(variable=optVar, value= 2, text="Option 2")
rad3 = NtkRadiobutton(frm3, 0, PACK, FILL, "33%", command=changeLabText)
rad3.config(variable=optVar, value= 3, text="Option 3")
rad2.invoke()

mainloop()