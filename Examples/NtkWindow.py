import _setup           # allows import from parent folder
import Ntk


def show_window(event):
   """This is called by butShow and shows the secondary window."""
   butShow.deactivate()
   ent1.set_content("")
   winSec.show()


def hide_window(event):
   """This is called by butDel (or if you click the upperleft close
   button): hides the secondary window and passes what we typed to
   the main."""
   winSec.hide()
   butShow.activate()
   s = ent1.get_content()
   if len(s) > 0:
      labCont.set_content("You typed: " + s)
   else:
      labCont.set_content("You don't type anything")


def change_window(event):
   """This is called by the radiobuttons and sets the secondary
   window properties (normal, modal or persistent)."""
   winSec.set_modal(strType.get())


# Main window
winMain = Ntk.NtkMain(200, 150, 600, 450, "Main Window")
# fill the window with a rowframe for aligning widgets
rfr1 = Ntk.NtkRowFrame(winMain, 0, 0, "fill", "fill")
rfr1.config_children("all", fcolor="dark blue", font=("DefaultFont", 12))
rfr1.config_children(Ntk.NtkLabel, bcolor="#E0E0A0", relief="ridge")

rfr1.add_row("10%")
# button for showing the secondary window
butShow = Ntk.NtkButton(rfr1, "center", "center", "40%", "80%", content="Show the window",
                        command=show_window)
# variable for radiobuttons
strType = Ntk.StringVar()

rfr1.add_row("20%")
# radiobutton and label for normal window
radNormal = Ntk.NtkRadiobutton(rfr1, 20, 0, 120, "fill", pad=(10, 10, 0, 10),
                               content=" Normal ", command=change_window)
radNormal.set_variable(strType, "normal")
labNormal = Ntk.NtkLabel(rfr1, "pack", 0, "fill", "fill", pad=(5, 10, 20, 10),
                         content="The window will be a normal window")

rfr1.add_row("20%")
# radiobutton and label for modal window
radModal = Ntk.NtkRadiobutton(rfr1, 20, 0, 120, "fill", pad=(10, 10, 0, 10),
                              content=" Modal ", command=change_window)
radModal.set_variable(strType, "modal")
labModal = Ntk.NtkLabel(rfr1, "pack", 0, "fill", "fill", pad=(5, 10, 20, 10),
           content="The window will always be visible, and mantain the focus until you close it")

# radiobutton and label for persistent window
rfr1.add_row("20%")
radPers = Ntk.NtkRadiobutton(rfr1, 20, 0, 120, "fill", pad=(10, 10, 0, 10),
                             content="Persistent", command=change_window)
radPers.set_variable(strType, "persistent")
labPers = Ntk.NtkLabel(rfr1, "pack", 0, "fill", "fill", pad=(5, 10, 20, 10),
                       content="The window will always be visible, but can lose the focus")

# label to see what we typed in secondary window
rfr1.add_row("25%")
labCont = Ntk.NtkLabel(rfr1, "pack", 0, "fill", "fill", pad=(10, 10, 20, 10))
labCont.config(anchor="center")

# secondary window
winSec = Ntk.NtkWindow(None, 220, 220, 300, 200, "Secondary Window")
lbl1 = Ntk.NtkLabel(winSec, 0, 0, "fill", "30%", pad=10, content="Type something below")
lbl1.config(bcolor="#E0E0A0")
ent1 = Ntk.NtkEntry(winSec, 0, "pack", "fill", "30%", pad=(30, 10))
ent1.config(bcolor="#F0D0D0")
butExit = Ntk.NtkButton(winSec, 220, 160, 70, 30, content="Exit", command=hide_window)
# binds a callback to closing window
winSec.onclose(hide_window)
# initially hides secondary window
winSec.hide()
# initially sets normal window
radNormal.invoke()

Ntk.mainloop()
