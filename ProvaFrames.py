from NCtk import *

winMain = NCtkMain(200, 150, 400, 300, "Frame Sample")
hfr1 = NCtkHorFrame(winMain, "20%", 10, "fill", 60)
hfr1.config(bcolor="#C04080", text="HorFrame 1", relief=RIDGE)
opt1 = hfr1.getconfig("relief")
hfr2 = NCtkHorFrame(winMain, "25%", "pack", "50%", "fill")
hfr2.config(bcolor="#40C080")
hfr3 = NCtkHorFrame(hfr1, "40%", "pack", 50, 30,)
hfr3.config(bcolor="#2060C0")
hfr4 = NCtkHorFrame(hfr1, "pack", "pack", 50, 30,)
hfr4.config(bcolor="#A000C0")
print(winMain.getwinfo("children"), "\n", hfr1.getwinfo("children"))

mainloop()