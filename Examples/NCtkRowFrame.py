import _setup           # allows import from parent folder
from NCtk import *


winMain = NCtkMain(200, 150, 400, 300, "App prova")
rfr1 = NCtkRowFrame(winMain, 0, 0, "fill", "fill")
rfr1.config_children("NCtkLabel", relief="solid", bcolor = "blue", fcolor="yellow")
rfr1.add_row(30)
rfr1.add_row("30%")
rfr1.add_row("30%")
rfr1.add_row("30%")
rfr1.set_active(0)
lab1 = NCtkLabel(rfr1, "pack", "20%", "30%", "fill", pad=(10, 0), content="A label in row 0")
lab2 = NCtkLabel(rfr1, "pack", "20%", "50%", "fill", pad=(10, 0), content="This is a fixed height row")
rfr1.set_active(1)
lab3 = NCtkLabel(rfr1, "pack", "20%", "30%", "60%", pad=(10, 0), content="A label in row 1")
lab4 = NCtkLabel(rfr1, "pack", "20%", "50%", "60%", pad=(10, 0), content="This is a 30% height row")
rfr1.set_active(2)
lab5 = NCtkLabel(rfr1, "pack", "20%", "30%", "60%", pad=(10, 0), content="A label in row 2")
lab6 = NCtkLabel(rfr1, "pack", "20%", "50%", "60%", pad=(10, 0), content="This is a 30% height row")

mainloop()
