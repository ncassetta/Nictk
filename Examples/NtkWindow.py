import _setup           # allows import from parent folder
from Ntk import *


def showwindow(event):
   """This is called by butShow and shows the secondary window."""
   butShow.deactivate()
   ent1.setcontent("")
   winSec.show()


def hidewindow(event):
   """This is called by butDel (or if you click the upperleft close
   button): hides the secondary window and passes what we typed to
   the main."""
   winSec.hide()
   butShow.activate()
   s = ent1.getcontent()
   if len(s) > 0:
      labCont.setcontent("You tiped: " + s)
   else:
      labCont.setcontent("You don't type anything")


def changewindow(event):
   """This is called by the radiobuttons and sets the secondary
   window properties (normal, modal or persistent)."""
   winSec.setmodal(strType.get())


# Main window
winMain = NtkMain(200, 150, 600, 450, "Main Window")
# fill the window with a rowframe for aligning widgets
rfr1 = NtkRowFrame(winMain, 0, 0, FILL, FILL)
rfr1.config_children(ALL, fcolor="dark blue", font=("DefaultFont", 12))
rfr1.config_children(NtkLabel, bcolor="#E0E0A0", relief=RIDGE)

rfr1.add_row("10%")
# button for showing the secondary window
butShow = NtkButton(rfr1, CENTER, CENTER, "40%", "80%", content="Show the window",
                    command=showwindow)
# variable for radiobuttons
strType = StringVar()

rfr1.add_row("20%")
# radiobutton and label for normal window
radNormal = NtkRadiobutton(rfr1, 20, 0, 120, FILL, pad=(10, 10, 0, 10), content=" Normal ",
                           command=changewindow)
radNormal.setvariable(strtype, "normal")
labNormal = NtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 10, 20, 10),
                     content="The window will be a normal window")

rfr1.add_row("20%")
# radiobutton and label for modal window
radModal = NtkRadiobutton(rfr1, 20, 0, 120, FILL, pad=(10, 10, 0, 10), content=" Modal ",
                          command=changewindow)
radModal.setvariable(strtype, "modal")
labModal = NtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 10, 20, 10),
                    content="The window will always be visible, and mantain the focus until you close it")

# radiobutton and label for persistent window
rfr1.add_row("20%")
radPers = NtkRadiobutton(rfr1, 20, 0, 120, FILL, pad=(10, 10, 0, 10), content="Persistent",
                         command=changewindow)
radPers.setvariable(strtype, "persistent")
labPers = NtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(5, 10, 20, 10),
                   content="The window will always be visible, but can lose the focus")

# label to see what we typed in secondary window
rfr1.add_row("25%")
labCont = NtkLabel(rfr1, PACK, 0, FILL, FILL, pad=(10, 10, 20, 10))
labCont.config(anchor=CENTER)

# secondary window
winSec = NtkWindow(None, 220, 220, 300, 200, "Secondary Window")
lbl1 = NtkLabel(winSec, 0, 0, FILL, "30%", pad=10, content="Type something below")
lbl1.config(bcolor="#E0E0A0")
ent1 = NtkEntry(winSec, 0, PACK, FILL, "30%", pad=(30, 10))
ent1.config(bcolor="#F0D0D0")
butExit = NtkButton(winSec, 220, 160, 70, 30, content="Exit", command=hidewindow)
# binds a callback to closing window
winSec.onclose(hidewindow)
# initially hides secondary window
winSec.hide()
# initially sets normal window
radNormal.invoke()

mainloop()
