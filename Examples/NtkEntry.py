import _setup           # allows import from parent folder
import Ntk
from Ntk.constants import *


def get_focus(event):
    """This is called when you click on one of the two entries."""
    if event.widget == entCelsius:
        # the Celsius entry got the focus ...
        entCelsius.bind("<Return>", to_Farenheit)
        entCelsius.bind("<<ChangedVar>>", to_Farenheit)
        entFarenheit.unbind("<<ChangedVar>>")
    else:
        # if the Farenheit entry got the focus ...
        entFarenheit.bind("<Return>", to_Celsius)
        entFarenheit.bind("<<ChangedVar>>", to_Celsius)
        entCelsius.unbind("<<ChangedVar>>")

def to_Farenheit(event):
    """Conversion F -> C"""
    try:
        cel = float(entCelsius.get_content())
        far = "{:.2f}".format(cel * 1.8 + 32)
    except ValueError:
        far=""    
    entFarenheit.set_content(far)
        
def to_Celsius(event):
    """Conversion C -> F"""
    try:
        far = float(entFarenheit.get_content())
        cel = "{:.2f}".format((far - 32) / 1.8)
    except ValueError:
        cel = ""    
    entCelsius.set_content(cel)
    

winMain = Ntk.NtkMain(100, 100, 300, 150, "C-F Conversion")
winMain.config_children(ALL, font=("Arial", 12))

# here we place  the widgets using absolute coords
labCelsius = Ntk.NtkLabel(winMain, 20, 20, 100, 40, content="Celsius") 
labCelsius.config(fcolor="red")
entCelsius = Ntk.NtkEntry(winMain, 140, 20, 140, 40)
entCelsius.config(bcolor="light grey", fcolor="red", sbcolor="red", sfcolor="white")
entCelsius.bind("<FocusIn>", get_focus)

labFarenheit = Ntk.NtkLabel(winMain, 20, 70, 100, 40, content="Farenheit")
labFarenheit.config(fcolor="green")
entFarenheit = Ntk.NtkEntry(winMain, 140, 70, 140, 40)
entFarenheit.config(bcolor="light grey", fcolor="green", sbcolor="green", sfcolor="white")
entFarenheit.bind("<FocusIn>", get_focus)

Ntk.mainloop()