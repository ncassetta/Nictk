from NCtk import *


winMain = NCtkWindow(200, 150, 640, 480, "Widget attributes")
winMain.config(background="yellow")
labSample = NCtkLabel(winMain, 10, 10, "fill", 60, "This is a sample")
chk1 = NCtkCheckbutton(winMain, 10, 100, 100, 100)
chk1.config(foreground="blue", text="This is a\nbutton, which\nis a button")
mainloop()