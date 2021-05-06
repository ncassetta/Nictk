import _setup           # allows import from parent folder
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

def hide(event):
   winSec.data = ent1.getcontent()
   winSec.grab_release()
   winSec.withdraw()

def bclose():
   hide(None)

def showwindow(event):
   #print(item)
   winSec.show()
   while winSec.winfo_viewable():
      winMain.update()
   print("Done!")
   print(winSec.data)
   return  # "break"

def changewindow(event):
   winSec.setmodal(strtype.get())


winMain = NCtkMain(200, 150, 800, 600, "Main Window")
rfr1 = NCtkRowFrame(winMain, 0, 0, FILL, FILL)
rfr1.config_children("all", fcolor="dark blue", font=("DefaultFont", 12))
rfr1.config_children(("NCtkLabel", "NCtkButton"), bcolor = "#E0E0A0", )
rfr1.config_children("NCtkLabel", relief=RIDGE)
rfr1.add_row("10%")
butShow = NCtkButton(rfr1, CENTER, CENTER, "40%", "80%", content="Show the window",
                     command=showwindow)
strtype = StringVar()
rfr1.add_row("10%")
radNormal = NCtkRadiobutton(rfr1, 20, 0, 120, FILL, pad=(10, 10, 0, 10), content=" Normal ",
                           command=changewindow)
radNormal.config(variable=strtype, value="normal")
labNormal = NCtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 10, 20, 10),
                     content="The window will be a normal window")
rfr1.add_row("10%")
radModal = NCtkRadiobutton(rfr1, 20, 0, 120, FILL, pad=(10, 10, 0, 10), content=" Modal ",
                           command=changewindow)
radModal.config(variable=strtype, value="modal")
labModal = NCtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 10, 20, 10),
                     content="The window will always be visible, and mantain the focus until you close it")
rfr1.add_row("10%")
radPers = NCtkRadiobutton(rfr1, 20, 0, 120, FILL, pad=(10, 10, 0, 10), content="Persistent",
                          command=changewindow)
radPers.config(variable=strtype, value="persistent")
labPers = NCtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 10, 20, 10),
                     content="The window will always be visible, but can lose the focus")

winSec = NCtkWindow(None, 220, 220, 300, 200, "Secondary Window")
lbl1 = NCtkLabel(winSec, 0, 0, "fill", "30%", pad=10, content="Type something below")
lbl1.config(relief="sunken", bcolor="#C0C080")
ent1 = NCtkEntry(winSec, 0, "pack", "fill", "30%", pad=10)
ent1.config(relief="sunken", bcolor="#C080C0")
butExit =NCtkButton(winSec, 220, 160, 70, 30, content="Exit", command=hide)
winSec.protocol("WM_DELETE_WINDOW", bclose)
winSec.withdraw()

radNormal.invoke()

mainloop()