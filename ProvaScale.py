from NCtk import *



winMain = NCtkWindow(200, 150, 400, 300, "App prova")
scl1 = NCtkScale(winMain, 10, 10, 200, 40)
scl1.config(bcolor="blue")

spb1 = Spinbox(winMain, from_= 0.0, to=10.0, increment=0.1)
spb1.pack()
citta = ("Bari", "Bologna", "Firenze", "Milano", "Napoli", "Palerno", "Roma", "Torino", "Venezia")
spb2 = Spinbox(winMain, values=citta)
spb2.pack()

mainloop()