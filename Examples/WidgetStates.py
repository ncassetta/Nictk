# This file is part of Nictk - A simple tkinter wrapper.
#    Copyright (C) 2021  Nicola Cassetta
#    See <https://github.com/ncassetta/Nictk>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Allows import from parent folder. You can delete this if you install the package
import _setup

import Nictk as Ntk
from Nictk.constants import *
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



winMain = Ntk.Main(200, 150, 400, 300, "Widget states sample")
# widgets are aligned with absolute coords

# upper entry and button
entText = Ntk.Entry(winMain, 0, 0, "fill", 60, pad=10)
entText.config(font=("Arial", 14), bcolor=bcolors[0], fcolor=fcolors[0], dfcolor = dfcolors[0])

butColor = Ntk.Button(winMain, CENTER, 70, 100, 30,
                      content="Change Color", command=change_color)

# frame and its children
hfr1 = Ntk.HorFrame(winMain, 0, 110, FILL, 80, content="This is a HorFrame")
hfr1.config(relief=RIDGE)
labFrame= Ntk.Label(hfr1, 0, 0, "70%", FILL, pad=(8, 8, 8, 28), content=texts[0])
labFrame.config(fcolor="#FFFFC0", bcolor="#202060", dfcolor="#D0D0A0",
                     relief=RIDGE)
butFrame= Ntk.Button(hfr1, PACK, 0, FILL, FILL, pad=(8, 8, 8, 28), content=
                     "Click me", command=change_text)

# lower button and label
butHideShow = Ntk.Button(winMain, 10, 220, 110, 50,
                         content=butcaptions[0], command=change_status)
butHideShow.config(bcolor="#C0C0FF")
labExplain = Ntk.Label(winMain, 130, 220, -10, 50)
labExplain.config(bcolor="#C0C0FF")
labExplain.set_content(explstates[0])

Ntk.mainloop()