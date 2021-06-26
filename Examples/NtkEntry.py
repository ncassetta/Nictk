import _setup           # allows import from parent folder
from Ntk import *


def getFocus(event):
    """This is called when you click on one of the two entries."""
    if event.widget == entCelsius:
         # the Celsius entry got the focus ...
        entCelsius.bind("<Return>", toFarenheit)
        entCelsius.bind("<<ChangedVar>>", toFarenheit)
        entFarenheit.unbind("<<ChangedVar>>")
    else:
         # if the Farenheit entry got the focus ...
        entFarenheit.bind("<Return>", toCelsius)
        entFarenheit.bind("<<ChangedVar>>", toCelsius)
        entCelsius.unbind("<<ChangedVar>>")

def toFarenheit(event):
    """Conversion F -> C"""
    try:
        cel = float(entCelsius.getcontent())
        far = "{:.2f}".format(cel * 1.8 + 32)
    except ValueError:
        far=""    
    entFarenheit.setcontent(far)
        
def toCelsius(event):
    """Conversion C -> F"""
    try:
        far = float(entFarenheit.getcontent())
        cel = "{:.2f}".format((far - 32) / 1.8)
    except ValueError:
        cel = ""    
    entCelsius.setcontent(cel)
    

winMain = NtkMain(100, 100, 300, 150, "C-F Conversion")
winMain.config_children(ALL, font=("Arial", 12))

# here we have positioned  the widgets using absolute coords
labCelsius = NtkLabel(winMain, 20, 20, 100, 40, content="Celsius")
labCelsius.config(fcolor="red")
entCelsius = NtkEntry(winMain, 140, 20, 140, 40)
entCelsius.config(bcolor="light grey", fcolor="red", sbcolor="red", sfcolor="white")
entCelsius.bind("<FocusIn>", getFocus)

labFarenheit = NtkLabel(winMain, 20, 70, 100, 40, content="Farenheit")
labFarenheit.config(fcolor="green")
entFarenheit = NtkEntry(winMain, 140, 70, 140, 40)
entFarenheit.config(bcolor="light grey", fcolor="green", sbcolor="green", sfcolor="white")
entFarenheit.bind("<FocusIn>", getFocus)

mainloop()