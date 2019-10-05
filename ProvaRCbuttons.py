from NCtk import *


winMain = NCtkWindow(200, 150, 640, 480, "Radio and Check Buttons")
winMain.config(background="yellow")
labSample = NCtkLabel(winMain, 10, 10, "fill", 60, "This is a sample")
but = (StringVar)
but.set("off")
chk1 = NCtkCheckbutton(winMain, 10, 100, 100, 30)
chk1.config(background="pink", text="This is a button", variable=but, offvalue="off", onvalue="on")
labBut = NCtkLabel(winMain, 159, 100, 100, 30)
labBut.config(textvariable=but)
a = 0
rad1 = NCtkRadiobutton(winMain, 10, 300, 100, 30)
rad1.config(variable=a, value=1)
rad2 = NCtkRadiobutton(winMain, 10, 340, 100, 30)
rad2.config(variable=a, value= 2)

mainloop()