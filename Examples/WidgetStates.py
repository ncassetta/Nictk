import _setup
from Ntk import *
from time import *

bcolors =  ("#FFFFFF", "#202060", "#D0D0A0", "#206020", "#FFA0A0", "#402000")
fcolors =  ("#000000", "#FFFFC0", "#002060", "#FFFFC0", "#004040", "#D0B0FF")
#dbcolors = ("#D0D0D0", "#000040", "#C0C080", "#408040", "#D08080", "#604020")
dfcolors = ("#202020", "#D0D0A0", "#204080", "#D0D0A0", "#206060", "#A0A0D0")
explstates = ("Now the button and the entry are enabled: you can type into the entry and press the button",
              "Now the button and the entry are disabled: you cannot type into the entry or press the button",
              "Now the button and the entry are hidden")
butcaptions = ("Disable", "Hide", "Show")

def change(event):
    global colorind
    colorind = (colorind + 1) % len(bcolors)
    entText.config(bcolor = bcolors[colorind], fcolor = fcolors[colorind], dfcolor= dfcolors[colorind])
        
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
        entText.config(state=NORMAL)
        butColor.show()
        butColor.config(state=NORMAL)
        newind = 0
    butHideShow.setcontent(butcaptions[newind])
    labExplain.setcontent(explstates[newind])


stringind = 0
colorind = 0
winMain = NtkMain(200, 150, 400, 300, "Widget states sample")
entText = NtkEntry(winMain, 0, 0, "fill", 70, pad=10)
entText.config(font=("Arial", 14), bcolor=bcolors[0], fcolor=fcolors[0], dfcolor = dfcolors[0])
butColor = NtkButton(winMain, CENTER, 90, 100, 40,
                      content="Change Color", command=change)
butHideShow = NtkButton(winMain, 10, 200, 110, 50,
                         content=butcaptions[0], command=changelabstatus)
butHideShow.config(bcolor="#C0C0FF")
labExplain = NtkLabel(winMain, 130, 200, -10, 50)
labExplain.config(bcolor="#C0C0FF")
labExplain.setcontent(explstates[0])
mainloop()