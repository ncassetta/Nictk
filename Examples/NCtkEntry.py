import _setup           # allows import from parent folder
from NCtk import *


def getFocus(event):
    # if the Celsius entry got the focus ...
    if event.widget == entCelsius:
        entCelsius.bind("<Return>", toFarenheit)
        entCelsius.bind("<<CHANGEDVAR>>", toFarenheit)
        entFarenheit.unbind("<<CHANGEDVAR>>")
    else:
        entFarenheit.bind("<Return>", toCelsius)
        entFarenheit.bind("<<CHANGEDVAR>>", toCelsius)
        entCelsius.unbind("<<CHANGEDVAR>>")

def toFarenheit(event):
    try:
        cel = float(entCelsius.getcontent())
        far = "{:.2f}".format(cel * 1.8 + 32)
    except ValueError:
        far=""    
    entFarenheit.setcontent(far)
        
def toCelsius(event):
    try:
        far = float(entFarenheit.getcontent())
        cel = "{:.2f}".format((far - 32) / 1.8)
    except ValueError:
        cel = ""    
    entCelsius.setcontent(cel)
    

winMain = NCtkMain(100, 100, 300, 150, "C-F Conversion")
winMain.config_children(ALL, font=("Arial", 12))
labCelsius = NCtkLabel(winMain, 20, 20, 100, 40, content="Celsius")
labCelsius.config(fcolor="red")
entCelsius = NCtkEntry(winMain, 140, 20, 140, 40)
entCelsius.config(bcolor="light grey", fcolor="red", sbcolor="red", sfcolor="white")
entCelsius.bind("<FocusIn>", getFocus)
labFarenheit = NCtkLabel(winMain, 20, 70, 100, 40, content="Farenheit")

entFarenheit = NCtkEntry(winMain, 140, 70, 140, 40)
entFarenheit.config(bcolor="light grey", fcolor="green", sbcolor="green", sfcolor="white")
entFarenheit.bind("<FocusIn>", getFocus)

winMain.mainloop()