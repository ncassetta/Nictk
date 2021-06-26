import _setup           # allows import from parent folder
from Ntk import *

CITTA = ("Bari", "Bologna", "Firenze", "Milano", "Napoli", "Palermo",
         "Roma", "Torino", "Venezia")

MODES = {"normal":"You can change the Spinbox value clicking on buttons or typing in it and pressing <RETURN>",
         "readonly":"You can only use up and down buttons",
         "autoadd":"As Normal, but every new value you type is added to Spinboz list"}

WRAPS = ["When you arrive at the end of the list you can continue from the beginning",
         "When you arrive at the end of the list you cannot go beyond"]

def changelabel(event):
    w = event.widget
    print("changelabel called\n")
    if w == spb1:
        labSample.config(fcolor="dark blue")
        labSample.setcontent("Selected city: " + w.getcontent())
    else:
        labSample.config(fcolor="brown")
        labSample.setcontent("Selected number: " + w.getcontent())
        
        
def changemode(event):
    opt = optMode.get()
    labMode.setcontent(MODES[opt])
    spb1.mode(opt)
        
def changewrap(event):
    opt = optWrap.get()
    labWrap.setcontent(WRAPS[0] if opt else WRAPS[1])
    spb1.config(wrap=opt)


winMain = NtkMain(200, 150, 640, 480, "Spinbox")
# main hor frame, containing left and right subframes
vfr1 = NtkHorFrame(winMain, 0, 0, FILL, -60)

#left frame
rfr1 = NtkRowFrame(vfr1, 0, 0, "50%", FILL)
rfr1.config(bcolor="#B0D0D0", text="Spinbox1", relief=RIDGE )
rfr1.config_children(ALL, bcolor="#B0D0B0")
rfr1.config_children(NtkSpinbox, rbcolor="#A0C0A0")

rfr1.add_row(40)
spb1 = NtkSpinbox(rfr1, CENTER, 0, "50%", FILL, pad=(0, 3), limits=CITTA, command=changelabel)

rfr1.add_row(50)
labModeTitle = NtkLabel(rfr1, 0, 0, FILL, FILL, pad=(0, 5), content="Spinbox modes")
labModeTitle.config(bcolor=rfr1.getconfig("bcolor"), relief=FLAT, anchor=S, font=("Arial", 16))

rfr1.add_row("30%")
optMode = StringVar()
vfrMode = NtkVerFrame(rfr1, 0, CENTER, "40%", "80%")
vfrMode.config(relief=SUNKEN)
tempT = tuple(MODES.keys())
radMode1 = NtkRadiobutton(vfrMode, 0, PACK, FILL, "33%", command=changemode)
radMode1.config(variable=optMode, value=tempT[0], text=tempT[0])
radMode2 = NtkRadiobutton(vfrMode, 0, PACK, FILL, "33%", command=changemode)
radMode2.config(variable=optMode, value= tempT[1], text=tempT[1])
radMode3 = NtkRadiobutton(vfrMode, 0, PACK, FILL, "33%", command=changemode)
radMode3.config(variable=optMode, value= tempT[2], text=tempT[2])
labMode = NtkLabel(rfr1, PACK, CENTER, FILL, "80%", pad=(5, 0,10, 0))
labMode.config(anchor=NW)

rfr1.add_row(50)
labWrapTitle = NtkLabel(rfr1, 0, 0, FILL, FILL, pad=(0, 5), content="Enable wrap")
labWrapTitle.config(bcolor=rfr1.getconfig("bcolor"), relief=FLAT, anchor=S, font=("Arial", 16))

rfr1.add_row("30%")
optWrap = BooleanVar()
vfrWrap = NtkVerFrame(rfr1, 0, CENTER, "40%", "80%")
vfrWrap.config(relief=SUNKEN)
radWrap1 = NtkRadiobutton(vfrWrap, 0, PACK, FILL, "50%", command=changewrap)
radWrap1.config(variable=optWrap, value=True, text="True")
radWrap2 = NtkRadiobutton(vfrWrap, 0, PACK, FILL, "50%", command=changewrap)
radWrap2.config(variable=optWrap, value= False, text="False")
labWrap = NtkLabel(rfr1, PACK, CENTER, FILL, "80%", pad=(5, 0,10, 0))
labWrap.config(anchor=NW)

# right frame
rfr2 = NtkRowFrame(vfr1, PACK, 0, FILL, FILL)
rfr2.config(bcolor="#FFFFA0", text="Spinbox2", relief=RIDGE)
rfr2.add_row(40)
spb2 = NtkSpinbox(rfr2, CENTER, 0, "50%", FILL, pad=(0,3), limits=(1.0, 10.0, 0.5), command=changelabel)

#bottom label
labSample = NtkLabel(winMain, CENTER, PACK, 280, FILL, pad=(0, 5))
labSample.config(bcolor="pink", text="Try the spinboxes!", anchor=CENTER, font=("Arial", 16))

radMode1.invoke()
radWrap2.invoke()

mainloop()
