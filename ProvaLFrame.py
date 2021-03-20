from NCtk import *


lines = ("Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto",
         "Nove", "Dieci", "Undici", "Dodici", "Tredici", "Quattordici")




winMain = NCtkMain(200, 150, 400, 300, "App prova")
frmTest = LabelFrame(winMain, width=200, height=100)
frmTest.pack()
frmTest.config(labelanchor=N, relief=RIDGE, text="Prova")
#lstTest.config(bcolor="blue", fcolor="yellow", font=("TkDefaultFont", 12))
#labMode = NCtkLabel(winMain, 200, 10, 150, 20, "Listbox Mode")
#labMode.config(bcolor="light green", fcolor="brown", relief=FLAT, anchor=CENTER)
#lstMode = NCtkListbox(winMain, 200, 40, 150, 100, command=selchanged, items=modes)
#lstMode.config(font=("TkDefaultFont", 12), relief=FLAT)
#butAdd = NCtkButton(winMain, 10, 240, 80, 50, "Add item", addtolbox) 
#butDel = NCtkButton(winMain, 100, 240, 80, 50, "Del item", delfromlbox)
#labExplain=NCtkLabel(winMain, 200, 150, 150, 140, explmodes[0])
#labExplain.config(anchor=NW)
#print (labExplain.getwinfo("fpixels", 20))

mainloop()