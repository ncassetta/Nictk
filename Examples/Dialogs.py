import _setup
import Ntk
from Ntk.constants import *

"""The item of the dictionary is a tuple with
   - the name of the fnction to call
   - its named parameters
"""
DIALOGS = { "Ok - Cancel": [Ntk.mb.askokcancel, {"message":"  Do you want to proceed?  "}],
            "Yes - No": [Ntk.mb.askquestion, {"message":"  Exit from the application?  "}],
            "Retry - Cancel": [Ntk.mb.askretrycancel, {"message":"  Do you want to retry?  "}],
            "Error": [Ntk.mb.showerror, {"message":"  File not found  "}],
            "Info": [Ntk.mb.showinfo, {"message":"    File saved    "}],
            "Warning": [Ntk.mb.showwarning, {"message":"  Data could be corrupted  "}],
            "Open File": [Ntk.fd.askopenfilename, {}],
            "Save as File": [Ntk.fd.asksaveasfilename, {"initialfile":"untitled.py"}],
            "Choose color": [Ntk.cc.askcolor, {"color":"#FF0000"}]
          }

        
def open_dialog(event):
    key = cmbType.get_content()
    func, arg = DIALOGS[key][0], DIALOGS[key][1]
    result = func(title=key + " dialog", **arg)
    if isinstance(result, bool):
        result = "ok" if result == True else "cancel"
    if result == "":
        result = "cancel"
    if isinstance(result, tuple):
        result = "#{:02X}{:02X}{:02X}".format(result[0][0], result[0][1], result[0][2])
    diagResult.set("You have chosen " + result)
            


winMain = Ntk.NtkMain(200, 150, 600, 450, "Dialog sample")
winMain.config_children(ALL, font=("Arial", 16))
# widgets are aligned with absolute coords

# upper entry and button
butOpen= Ntk.NtkButton(winMain, CENTER, 20, 240, 80, pad=10,
                       content="Open a dialog box", command=open_dialog)
butOpen.config(bcolor="#C0F0C0", fcolor="#2020C0")

cmbType = Ntk.NtkCombobox(winMain, CENTER, PACK, 320, 80, pad=10,
                      items=tuple(DIALOGS.keys()))

diagResult = Ntk.StringVar(value="")
labResult = Ntk.NtkLabel(winMain, CENTER, PACK, 320, 120, pad=10, content=diagResult)
labResult.config(bcolor="#FFFFC0", fcolor="#202060", relief=RIDGE, anchor=CENTER)

Ntk.mainloop()