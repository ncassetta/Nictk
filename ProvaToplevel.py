from NCtk import *

def show(item):
   global winSec
   if not winSec:
       winSec = NCtkToplevel(winMain, 220, 220, 300, 200, "Toplevel")
       lblSec = NCtkLabel(winSec, 0, 0, "fill", "50%", content="Label", pad=(10, 10))
       lblSec.config(relief="sunken", bcolor="#C04080")
       butWindow.setcontent("Hide window")
   else:
      winSec.destroy()
      winSec = None
      butWindow.setcontent("Show window")
      
def modal(item):
   pass

def persistent(item):
   pass

winMain = NCtkWindow(200, 150, 400, 300, "App prova") 
flagModal = IntVar(value=0)            # these go AFTER winMain declaration
flagPersistent = IntVar(value=0)
butWindow = NCtkButton(winMain, 20, 20, 80, 30, content="Show window", command=show)
chkModal = NCtkCheckbutton(winMain, 20, "pack", 80, 30, content="Modal")
chkModal.config(variable=flagModal)
chkPers = NCtkCheckbutton(winMain, 20, "pack", 80, 30, content="Persistent")
chkPers.config(variable=flagPersistent)

winSec = None


mainloop()