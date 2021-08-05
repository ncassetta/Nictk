import _setup           # allows import from parent folder
import Ntk


# italian cities
CITIES = ("Bari", "Bologna", "Firenze", "Milano", "Napoli", "Palermo",
         "Roma", "Torino", "Venezia")


def change_label(event):
    """This is called when you select a city in the upper combo;
    it prints the selected city on the helper label."""
    sel = cmbCities.get_content()
    labHelp.set_content("You selected: " + sel)
    

def delete_sel(event):
    """This is called by ButDel; it deletes the selected city
    from the upper combo and adds it to the lower."""
    # gets the selected string
    sel = cmbCities.get_content()
    if len(sel):
        # gets its numeric index (from 0)
        ind = cmbCities.index(sel)
        # deletes from upper combo (cmbCities.delete(sel) also works)
        cmbCities.delete(ind)
        # adds the string to the lower combo
        cmbIns.add(sel)
        if cmbCities.get_menu().size() > 0:
            # selects the next city in the upper combobox (if sel was the last string
            # the menu auto adjust the index, so no out of range errors)
            cmbCities.set_content(cmbCities.get_item(ind))
            labHelp.set_content("You deleted {} (but it is now in the lower combobox".format(sel))
        else:
            # the upper combo is empty
            cmbCities.set_content("")
            labHelp.set_content("Empty menu")

        
def insert_sel(event):
    """This is called by ButIns; it deletes a city in the lower combo
    and adds it to the upper."""
    sel = cmbIns.get_content()
    if len(sel):
        # see delete_sel
        ind = cmbIns.index(sel)
        cmbCities.add(sel)
        cmbIns.delete(sel)
        labHelp.set_content("You newly added {} to the upper combobox".format(sel))
        if cmbIns.get_menu().size() > 0:
            cmbIns.set_content(cmbIns.get_item(ind))
        else:
            cmbIns.set_content("")


def reset_combo(event):
    """This callback resets the contents of the two combos"""
    # empties and refills the upper combo
    cmbCities.delete(0, Ntk.END)
    for i in CITIES:
        cmbCities.add(i)
    # selects the first city
    cmbCities.set_content(CITIES[0])
    # empties the lower combo
    cmbIns.delete(0, Ntk.END)
    cmbIns.set_content("")
    labHelp.set_content("You reset the combos")
    

winMain = Ntk.NtkMain(200, 150, 400, 300, "Combobox sample")
# configures all children widget when they are created
winMain.config_children(Ntk.ALL, font=("Arial", 16))
winMain.config_children((Ntk.NtkButton, Ntk.NtkCombobox), bcolor="#D0D080", abcolor="#E0E090")
# creates the combobox with the cities
cmbCities = Ntk.NtkCombobox(winMain, 0, 0, Ntk.FILL, 70, pad=(10, 20, 10, 10),
                            items=CITIES, command=change_label)
# creates the label under it
labHelp = Ntk.NtkLabel(winMain, 0, Ntk.PACK, Ntk.FILL, 90, pad=10, 
                       content="Initially selected: " + CITIES[0])
labHelp.config(bcolor="#B0D0F0", relief=Ntk.RIDGE, anchor=Ntk.CENTER)
# rowframe for aligning other widgets
rfr1 = Ntk.NtkRowFrame(winMain, 0, Ntk.PACK, Ntk.FILL, Ntk.FILL)
rfr1.add_row(55)
# button for deleting a city from cmbCities
butDel = Ntk.NtkButton(rfr1, 0, 0, "50%", Ntk.FILL, pad=(10, 10, 10, 5),
                       content="Delete selected", command=delete_sel)
# button for reset
butRes = Ntk.NtkButton(rfr1, Ntk.PACK, 0, Ntk.FILL, Ntk.FILL, pad=(10, 10, 10, 5), 
                       content="Reset", command=reset_combo)
rfr1.add_row(55)
# button for reinserting a deleted city
butIns = Ntk.NtkButton(rfr1, 0, 0, "50%", Ntk.FILL, pad=(10, 5, 10, 10), 
                       content="Insert selected", command=insert_sel)
butIns.deactivate()
# combobox for deleted cities
cmbIns = Ntk.NtkCombobox(rfr1, Ntk.PACK, 0, Ntk.FILL, Ntk.FILL, pad=(10, 5, 10, 10))
# auto activate - deactivate buttons 
cmbCities.bind("<<ChangedVar>>",
               lambda ev: butDel.activate() if len(ev.widget.get_content()) else butDel.deactivate())
cmbIns.bind("<<ChangedVar>>",
            lambda ev: butIns.activate() if len(ev.widget.get_content()) else butIns.deactivate())

Ntk.mainloop()
