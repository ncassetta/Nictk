import _setup           # allows import from parent folder
from Ntk import *


# italian cities
CITIES = ("Bari", "Bologna", "Firenze", "Milano", "Napoli", "Palermo",
         "Roma", "Torino", "Venezia")


def change_label(event):
    """This is called when you select a city in the upper combo;
    it prints the selected city on the helper label."""
    sel = cmbCities.getcontent()
    labHelp.setcontent("You selected: " + sel)
    

def delete_sel(event):
    """This is called by ButDel; it deletes the selected city
    from the upper combo and adds it to the lower."""
    # gets the selected string
    sel = cmbCities.getcontent()
    if len(sel):
        # gets its numeric index (from 0)
        ind = cmbCities.index(sel)
        # deletes from upper combo (cmbCities.delete(sel) also works)
        cmbCities.delete(ind)
        # adds the string to the lower combo
        cmbIns.add(sel)
        if cmbCities.getmenu().len() > 0:
            # selects the next city in the upper combobox (if sel was the last string
            # the menu auto adjust the index, so no out of range errors)
            cmbCities.setcontent(cmbCities.getmenuentry(ind))
            labHelp.setcontent("You deleted {} (but it is now in the lower combobox".format(sel))
        else:
            # the upper combo is empty
            cmbCities.setcontent("")
            labHelp.setcontent("Empty menu")

        
def insert_sel(event):
    """This is called by ButIns; it deletes a city in the lower combo
    and adds it to the upper."""
    sel = cmbIns.getcontent()
    if len(sel):
        # see delete_sel
        ind = cmbIns.index(sel)
        cmbCities.add(sel)
        cmbIns.delete(sel)
        labHelp.setcontent("You newly added {} to the upper combobox".format(sel))
        if cmbIns.getmenu().len() > 0:
            cmbIns.setcontent(cmbIns.getmenuentry(ind))
        else:
            cmbIns.setcontent("")


def reset_combo(event):
    """This callback resets the contents of the two combos"""
    # empties and refills the upper combo
    cmbCities.delete(0, END)
    for i in CITIES:
        cmbCities.add(i)
    # selects the first city
    cmbCities.setcontent(CITIES[0])
    # empties the lower combo
    cmbIns.delete(0, END)
    cmbIns.setcontent("")
    labHelp.setcontent("You reset the combos")
    

winMain = NtkMain(200, 150, 400, 300, "Combobox sample")
winMain.config_children(ALL, font=("Arial", 16))
winMain.config_children((NtkButton, NtkCombobox), bcolor="#D0D080", abcolor="#E0E090")
# creates the combobox with the cities
cmbCities = NtkCombobox(winMain, 0, 0, FILL, 70, pad=(10, 20, 10, 10), values=CITIES, command=change_label)
# creates the label under it
labHelp = NtkLabel(winMain, 0, PACK, FILL, 90, pad=10, content="Initially selected: " + CITIES[0])
labHelp.config(bcolor="#B0D0F0", relief=RIDGE, anchor=CENTER)
# rowframe for aligning other widgets
rfr1 = NtkRowFrame(winMain, 0, PACK, FILL, FILL)
rfr1.add_row(55)
# button for deleting a city from cmbCities
butDel = NtkButton(rfr1, 0, 0, "50%", FILL, pad=(10, 10, 10, 5), content="Delete selected", command=delete_sel)
# button for reset
butRes = NtkButton(rfr1, PACK, 0, FILL, FILL, pad=(10, 10, 10, 5), content="Reset", command=reset_combo)
rfr1.add_row(55)
# button for reinserting a deleted city
butIns = NtkButton(rfr1, 0, 0, "50%", FILL, pad=(10, 5, 10, 10), content="Insert selected", command=insert_sel)
butIns.deactivate()
# combobox for deleted cities
cmbIns = NtkCombobox(rfr1, PACK, 0, FILL, FILL, pad=(10, 5, 10, 10))
# auto activate - deactivate buttons 
cmbCities.bind("<<ChangedVar>>", lambda ev: butDel.activate() if len(ev.widget.getcontent()) else butDel.deactivate())
cmbIns.bind("<<ChangedVar>>", lambda ev: butIns.activate() if len(ev.widget.getcontent()) else butIns.deactivate())

mainloop()
