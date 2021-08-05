import _setup           # allows import from parent folder
import Ntk


winMain = Ntk.NtkMain(200, 150, 400, 300, "NtkRowFrame sample")
rfr1 = Ntk.NtkRowFrame(winMain, 0, 0, "fill", "fill")
rfr1.config_children(Ntk.NtkLabel, relief=Ntk.SOLID, bcolor = "blue", fcolor="yellow",
                     anchor=Ntk.CENTER)
# In this example we have added all rows, and then selected them with set_active.
# Is more common to add a row at a time (which sets it as active) and then add
# widgets to it

# fixed vertical size
rfr1.add_row(30)
# percent vertical size
rfr1.add_row("30%")
# percent vertical size
rfr1.add_row("30%")
# fixed from bottom vertical size
rfr1.add_row(-10)

# "pack" == Ntk.PACK and "fill" == Ntk.FILL
rfr1.set_active(0)
lab1 = Ntk.NtkLabel(rfr1, "pack", "20%", "30%", "fill", pad=(10, 0), content="A label in row 0")
lab2 = Ntk.NtkLabel(rfr1, "pack", "20%", "50%", "fill", pad=(10, 0), content="This is a fixed height row")

rfr1.set_active(1)
lab3 = Ntk.NtkLabel(rfr1, "pack", "20%", "30%", "60%", pad=(10, 0), content="A label in row 1")
lab4 = Ntk.NtkLabel(rfr1, "pack", "20%", "50%", "60%", pad=(10, 0), content="This is a 30% height row")

rfr1.set_active(2)
lab5 = Ntk.NtkLabel(rfr1, "pack", "20%", "30%", "60%", pad=(10, 0), content="A label in row 2")
lab6 = Ntk.NtkLabel(rfr1, "pack", "20%", "50%", "60%", pad=(10, 0), content="Try to resize the window")

rfr1.set_active(3)
lab7 = Ntk.NtkLabel(rfr1, "pack", 10, "30%", -10, pad=(10, 0), content="A label in row 3")
lab8 = Ntk.NtkLabel(rfr1, "pack", 10, "50%", -10, pad=(10, 0), content="This is a fixed from bottom height row")

Ntk.mainloop()
