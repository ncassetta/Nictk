import _setup
from NCtk import *
from time import *

bcolors = ("#C00080", "#4040C0", "#804080", "#C08000", "#C04080")
fcolors = ("#C0FF80", "#FFC080", "#FF80FF", "#80FFFF", "#C0C0C0")
explstates = ("Now the button and the entry are enabled: you can type into the entry and press the button",
              "Now the button and the entry are disabled: you cannot type into the entry or press the button",
              "Now the button and the entry are hidden",
              "Now the button and the entry are visible, but still disabled")

def change(event):
    global colorind
    colorind = (colorind + 1) % 5
    entText.config(bcolor = bcolors[colorind], fcolor = fcolors[colorind])
        
def changelabstatus(event):
    txt = butHideShow.getcontent()
    if txt == "Disable":
        entText.config(state=DISABLED)
        butColor.config(state=DISABLED)
        newind = 1
    elif txt == "Hide":
        entText.hide()
        butColor.hide()
        newind = 2
    elif txt == "Show":
        entText.show()
        butColor.show()
        newind = 3
    else:
        entText.config(state=NORMAL)
        butColor.config(state=NORMAL)
        newind = 0
    butHideShow.setcontent(butHideShow.captions[newind])
    labExplain.setcontent(explstates[newind])


stringind = 0
colorind = 0
winMain = NCtkMain(200, 150, 400, 300, "States sample")
entText = NCtkEntry(winMain, 0, 0, "fill", 70, pad=10)
butColor = NCtkButton(winMain, 10, 100, 100, 40,
                      content="Change Color", command=change)
butHideShow = NCtkButton(winMain, 10, 200, 100, 40, command=changelabstatus)
butHideShow.captions = ("Disable", "Hide", "Show", "Enable")
butHideShow.config(text=butHideShow.captions[0])
labExplain = NCtkLabel(winMain, 210, 200, -10, -10)
labExplain.setcontent(explstates[0])
mainloop()