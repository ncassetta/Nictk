from NCtk import *

winMain = NCtkWindow(200, 150, 400, 300, "App prova")
hfr1 = NCtkHorFrame(winMain, "20%", 10, "fill", 60)
hfr1.config(bcolor="#C04080")
hfr2 = NCtkHorFrame(winMain, "25%", "pack", "50%", "fill")
hfr2.config(bcolor="#40C080")
hfr3 = NCtkHorFrame(hfr1, "40%", "pack", 50, 30,)
hfr3.config(bcolor="#2060C0")
hfr4 = NCtkHorFrame(hfr1, "pack", "pack", 50, 30,)
hfr4.config(bcolor="#A000C0")
print(winMain.winfo_children(), "\n", hfr1.winfo_children())

mainloop()