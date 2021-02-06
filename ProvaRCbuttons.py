from NCtk import *

def changeLabText():
    print ("changeLabText called with but2 =", but2.get())
    if but2.get():
        labSample.setcontent("Checked")
    else:
        labSample.setcontent("Not checked")


winMain = NCtkWindow(200, 150, 640, 480, "Radio and Check Buttons")
winMain.config(background="yellow")
labSample = NCtkLabel(winMain, 0, 0, "fill", 60, pad=10)
but1 = StringVar()
frm1 = NCtkHorFrame(winMain, 0, "pack", "fill", 80)
chk1 = NCtkCheckbutton(frm1, 0, 0, "30%", "fill", content="This is a button with pink background",
                       pad=(10, 5))
chk1.config(bcolor="pink")
chk1.setvariable(but1, "Value: off", "Value: on")
chk1.select()
labBut1 = NCtkLabel(frm1, "pack", 0, 100, "fill", pad=(0, 5))
labBut1.config(textvariable=but1)
but2 = IntVar()
frm2 = NCtkHorFrame(winMain, 0, "pack", "fill", 80)
chk2 = NCtkCheckbutton(frm2, 0, 0, "30%", "fill", content="This is another button wich controls the label text",
                       command=changeLabText, pad=(10, 5))
chk2.config(bcolor="orange")
chk2.setvariable(but2, 0, 1)
chk2.deselect()
labBut2 = NCtkLabel(frm2, "pack",0 , 100, "fill", pad=(0,5))
labBut2.config(textvariable=but2)
a = 0
frm3 = NCtkVerFrame(winMain, 0, 300, 500, "fill")
rad1 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%")
rad1.config(variable=a, value=1, text = "Option 1")
rad2 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%")
rad2.config(variable=a, value= 2, text="Option 2")
rad3 = NCtkRadiobutton(frm3, 0, "pack", "fill", "33%")
rad3.config(variable=a, value= 3, text="Option 2")
rad2.select()


mainloop()