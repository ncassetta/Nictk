# This file is part of Ntk - A simple tkinter wrapper.
#    Copyright (C) 2021  Nicola Cassetta
#    See <https://github.com/ncassetta/Ntk>
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


import _setup           # allows import from parent folder
import Ntk


def change_label_text(ev):
    """This callback recognizes which widget called it,
    and updates the upper label content accordingly."""
    if ev.widget == chk1:
        s = "Pink button variable value:     " + chk1Var.get()
    elif ev.widget == chk2:
        s = "Orange button variable value:   " + str(chk2Var.get())
    else:
        s = "Option " + str(optVar.get()) + " selected"
    labSample.set_content(s)



winMain = Ntk.NtkMain(200, 150, 600, 400, "Radio and Check Buttons")
winMain.config(bcolor="#FFFFA0")
winMain.config_children("all", relief="groove")

# we dispose our widgets in rows
rfr1 = Ntk.NtkRowFrame(winMain, 0, 0, "fill", "fill")
rfr1.add_row(60)

# main label: its content is updated by the callback
labSample = Ntk.NtkLabel(rfr1, 0, 0, "fill", "fill", pad=10)
rfr1.add_row(80)

# creates pink checkbutton, and associates a StringVar to the button states 
chk1Var = Ntk.StringVar()
chk1 = Ntk.NtkCheckbutton(rfr1, 0, 0, "40%", "fill", pad=(10, 5, 5, 5),
                          content="This button controls a StrVar, which can get values: 'Value: on' and 'Value: off",
                          variable=(chk1Var, "Value: on", "Value: off"), command=change_label_text) 
chk1.config(bcolor="pink", abcolor="pink")
chk1.select()
# the label will be automatically updated with chk1Var content
labChk1 = Ntk.NtkLabel(rfr1, "pack", 0, "fill", "fill", pad=(5, 5, 10, 5), content=chk1Var)
rfr1.add_row(80)

# creates orange checkbutton, and associates an IntVar to the button states
# (its offvalue and onvalue are set to 0 and 1) 
chk2Var = Ntk.IntVar()
chk2 = Ntk.NtkCheckbutton(rfr1, 0, 0, "40%", "fill", pad=(10, 5, 5, 5),
                          content="This button controls an IntVar, which can get values: 0 and 1",
                          variable=chk2Var, command=change_label_text)
chk2.config(bcolor="orange", abcolor="orange")
chk2.deselect()
# the label will be automatically updated with chk2Var content
labChk2 = Ntk.NtkLabel(rfr1, "pack", 0 , "fill", "fill", pad=(5, 5, 10, 5), content=chk2Var)
rfr1.add_row(-10)

# we need this to stack radiobuttons vertically
frm3 = Ntk.NtkVerFrame(rfr1, 10, 10, -10, "fill")
frm3.config(relief="groove")
frm3.config_children("all", relief="flat")

# common variable for all radiobuttons
optVar = Ntk.IntVar()
# radiobuttons
rad1 = Ntk.NtkRadiobutton(frm3, 0, "pack", "fill", "33%", content="Option 1",
                          variable=(optVar, 1), command=change_label_text)
rad2 = Ntk.NtkRadiobutton(frm3, 0, "pack", "fill", "33%", content="Option 2",
                          variable=(optVar, 2), command=change_label_text)
rad3 = Ntk.NtkRadiobutton(frm3, 0, "pack", "fill", "33%", content="Option 3",
                          variable=(optVar, 3), command=change_label_text)
# sets rad2 at the beginning
rad2.invoke()
# clears the text set by the previous
labSample.set_content("")

Ntk.mainloop()