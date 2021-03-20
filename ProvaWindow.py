from NCtk import *

def show():
   winSec.data = (1, 2, 3, 4)
   if flagModal.get():
      winSec.transient(winMain)
      winSec.focus_force() # added
      winSec.grab_set()      
   if flagPers.get():
      winSec.attributes('-topmost', 'true')
   else:
      winSec.attributes('-topmost', 'false')
   #stModal = "Modal: " + ("True" if flagModal else "False")
   #stPers = "Persistent: " + ("True" if flagPers.get() else "False")
   #lblModal.setcontent(stModal)
   #lblPers.setcontent(stPers)
   winSec.deiconify()

def hide():
   winSec.data = ent1.gettext()
   winSec.grab_release()
   winSec.withdraw()

def bclose():
   hide(None)

def getentryvalue():
   #print(item)
   show()
   while winSec.winfo_viewable():
      winMain.update()
   print("Done!")
   print(winSec.data)
   return  # "break"


winMain = NCtkMain(200, 150, 400, 300, "Main Window") 
flagModal = IntVar(value=0)            # these go AFTER winMain declaration
flagPers = IntVar(value=0)
butShow = NCtkButton(winMain, 20, 20, 80, 30, content="Show window", command=getentryvalue)
chkModal = NCtkCheckbutton(winMain, 20, "pack", 80, 30, content="Modal")
chkModal.config(variable=flagModal)
chkPers = NCtkCheckbutton(winMain, 20, "pack", 80, 30, content="Persistent")
chkPers.config(variable=flagPers)
winSec = NCtkWindow(winMain, 220, 220, 300, 200, "Secondary Window")
lbl1 = NCtkLabel(winSec, 0, 0, "fill", "20%", pad=10, content="Type something below")
lbl1.config(relief="sunken", bcolor="#C04080")
ent1 = NCtkEntry(winSec, 0, "pack", "fill", "20%", pad=10)
ent1.config(relief="sunken", bcolor="#C04080")
butExit =NCtkButton(winSec, 220, 160, 70, 30, content="Exit", command=hide)
winSec.protocol("WM_DELETE_WINDOW", bclose)
winSec.withdraw()


mainloop()