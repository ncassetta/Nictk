import _setup
from Ntk import *
from time import *

bcolors =  ("#FFFFFF", "#202060", "#D0D0A0", "#206020", "#FFA0A0", "#402000")
fcolors =  ("#000000", "#FFFFC0", "#002060", "#FFFFC0", "#004040", "#D0B0FF")
dfcolors = ("#202020", "#D0D0A0", "#204080", "#D0D0A0", "#206060", "#A0A0D0")
explstates = ("Now the buttons and the entry are enabled: you can type into the entry and press the buttons",
              "Now the buttons and the entry are disabled: you cannot type into the entry or press the buttons",
              "Now the buttons and the entry are hidden")
texts = ("If you change the state of a container ...", "... all of its children inherits it")
butcaptions = ("Disable", "Hide", "Show")
colorind, textind = 0, 0


def change_color(event):
    """This is called by butColor and changes the colors for the entText entry."""
    global colorind
    colorind = (colorind + 1) % len(bcolors)
    entText.config(bcolor = bcolors[colorind], fcolor = fcolors[colorind], dfcolor= dfcolors[colorind])
    
def change_text(event):
    """This is called by butFeame and changes the text of labFrame."""
    global textind
    textind = (textind + 1) % 2
    labFrame.set_content(texts[textind])

def change_status(event):
    """This is called by butHideShow and ciclicaly disables and hides
    butColor, entText and hfr1."""
    # event.widget.get_content() also works
    txt = butHideShow.get_content()
    if txt == "Disable":
        entText.deactivate()
        butColor.deactivate()
        hfr1.deactivate()
        newind = 1
    elif txt == "Hide":
        entText.hide()
        butColor.hide()
        hfr1.hide()
        newind = 2
    elif txt == "Show":
        entText.show()
        entText.activate()
        butColor.show()
        butColor.activate()
        hfr1.show()
        hfr1.activate()
        newind = 0
    butHideShow.set_content(butcaptions[newind])
    labExplain.set_content(explstates[newind])



winMain = NtkMain(200, 150, 400, 300, "Widget states sample")
# widgets are aligned with absolute coords

# upper entry and button
entText = NtkEntry(winMain, 0, 0, "fill", 60, pad=10)
entText.config(font=("Arial", 14), bcolor=bcolors[0], fcolor=fcolors[0], dfcolor = dfcolors[0])

butColor = NtkButton(winMain, CENTER, 70, 100, 30,
                      content="Change Color", command=change_color)

# frame and its children
hfr1 = NtkHorFrame(winMain, 0, 110, FILL, 80, content="This is a HorFrame")
hfr1.config(relief=RIDGE)
labFrame= NtkLabel(hfr1, 0, 0, "70%", FILL, pad=(8, 8, 8, 28), content=texts[0])
labFrame.config(fcolor="#FFFFC0", bcolor="#202060", dfcolor="#D0D0A0",
                     relief=RIDGE)
butFrame= NtkButton(hfr1, PACK, 0, FILL, FILL, pad=(8, 8, 8, 28), content=
                   "Click me", command=change_text)

# lower button and label
butHideShow = NtkButton(winMain, 10, 220, 110, 50,
                         content=butcaptions[0], command=change_status)
butHideShow.config(bcolor="#C0C0FF")
labExplain = NtkLabel(winMain, 130, 220, -10, 50)
labExplain.config(bcolor="#C0C0FF")
labExplain.set_content(explstates[0])

mainloop()