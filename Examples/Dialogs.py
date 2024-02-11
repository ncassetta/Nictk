# This file is part of Nictk - A simple tkinter wrapper.
#    Copyright (C) 2021-2024 Nicola Cassetta
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


"""The items of this dictionary are tuples with
   - the name of the function to call
   - its named parameters
"""
DIALOGS = { "Ok - Cancel": (Ntk.askokcancel, {"message":"  Do you want to proceed?  "}),
            "Yes - No": (Ntk.askquestion, {"message":"  Exit from the application?  "}),
            "Retry - Cancel": (Ntk.askretrycancel, {"message":"  Do you want to retry?  "}),
            "Yes - No  - Cancel": (Ntk.askyesnocancel, {"message":"  Exit from the application?  "}),
            "Error": (Ntk.showerror, {"message":"  File not found  "}),
            "Info": (Ntk.showinfo, {"message":"    File saved    "}),
            "Warning": (Ntk.showwarning, {"message":"  Data could be corrupted  "}),
            "Open File": (Ntk.askopenfilename, {}),
            "Save as File": (Ntk.asksaveasfilename, {"initialfile":"untitled.py"}),
            "Open Files": (Ntk.askopenfilenames, {}),
            "Choose Directory": (Ntk.askdirectory, {}),
            "Choose color": (Ntk.askcolor, {"color":"#FF0000"})
          }

        
def open_dialog(event):
    key = cmbType.get_content()
    func, arg = DIALOGS[key][0], DIALOGS[key][1]
    result = func(title=key + " dialog", **arg)
    diagResult.set("The dialog box returned:\n" + result.__repr__())
            


winMain = Ntk.Main(200, 150, 500, 400, "Dialog sample")
winMain.config_children(ALL, font=("Arial", 16))
# widgets are aligned with absolute coords

# upper button
butOpen= Ntk.Button(winMain, CENTER, 20, 320, 60, pad=10,
                       content="Open a dialog box", command=open_dialog)
butOpen.config(bcolor="#C0F0C0", fcolor="#2020C0")

# combobox for choosing the dialog to open
cmbType = Ntk.Combobox(winMain, CENTER, PACK, 320, 80, pad=10,
                      items=tuple(DIALOGS.keys()))

diagResult = Ntk.StringVar(value="")
# lower label for info
labResult = Ntk.Label(winMain, CENTER, PACK, 400, 160, pad=10, content=diagResult)
labResult.config(bcolor="#FFFFC0", fcolor="#202060", relief=RIDGE, anchor=CENTER)

Ntk.mainloop()