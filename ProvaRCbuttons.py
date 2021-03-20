from NCtk import *

def changeLabText(ev):
    if ev.widget == chk1:
        s = "Pink button " + but1.get()
    elif ev.widget == chk2:
        s = "Orange button value: " + str(but2.get())
    else:
        s = "Option " + str(opt.get()) + " selected"
    labSample.setcontent(s)


winMain = NCtkMain(200, 150, 640, 480, "Radio and Check Buttons")
winMain.config(bcolor="yellow")
labSample = NCtkLabel(winMain, 0, 0, "fill", 60, pad=10)
but1 = StringVar()
frm1 = NCtkHorFrame(winMain, 0, "pack", "fill", 80)
chk1 = NCtkCheckbutton(frm1, 0, 0, "30%", "fill", pad=(10, 5),
                       content="This is a button with pink background", command=changeLabText) 
chk1.config(bcolor="pink", abcolor="pink")
chk1.setvariable(but1, "Value: off", "Value: on")
chk1.select()
labBut1 = NCtkLabel(frm1, "pack", 0, 100, "fill", pad=(0, 5))
labBut1.config(textvariable=but1)
but2 = IntVar()
frm2 = NCtkHorFrame(winMain, 0, "pack", "fill", 80)
chk2 = NCtkCheckbutton(frm2, 0, 0, "30%", "fill", pad=(10, 5),
                       content="This is another button wich controls the label text", command=changeLabText, )
chk2.config(bcolor="orange", abcolor="orange")
chk2.setvariable(but2, 0, 1)
chk2.deselect()
labBut2 = NCtkLabel(frm2, "pack",0 , 100, "fill", pad=(0,5))
labBut2.config(textvariable=but2)
opt = IntVar()
frm3 = NCtkVerFrame(winMain, 0, 300, 500, "fill")
rad1 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%", pad=(10, 0), command=changeLabText)
rad1.config(variable=opt, value=1, text = "Option 1")
rad2 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%", pad=(10, 0), command=changeLabText)
rad2.config(variable=opt, value= 2, text="Option 2")
rad3 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%", pad=(10, 0), command=changeLabText)
rad3.config(variable=opt, value= 3, text="Option 3")
rad2.select()


mainloop()