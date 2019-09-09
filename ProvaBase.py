from NCtk import *

winMain = NCtkWindow(200, 150, 400, 300, "App prova")
hfr1 = NCtkHorFrame(winMain, "20%", 10, "fill", 60)
hfr1.config(background="#C04080")
hfr2 = NCtkHorFrame(winMain, "25%", "pack", "50%", "fill")
hfr2.config(background="#40C080")
hfr3 = NCtkHorFrame(hfr1, "40%", "pack", 50, 30,)
hfr3.config(background="#2060C0")
hfr4 = NCtkHorFrame(hfr1, "pack", "pack", 50, 30,)
hfr4.config(background="#A000C0")
print(winMain.winfo_children(), "\n", hfr1.winfo_children())

mainloop()