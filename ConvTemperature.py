from NCtk import *


def getFocus(event):
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
        cel = float(entCelsius.gettext())
        far = "{:.2f}".format(cel * 1.8 + 32)
    except ValueError:
        far=""    
    entFarenheit.delete(0, END)
    entFarenheit.insert(0, far)
        
def toCelsius(event):
    try:
        far = float(entFarenheit.gettext())
        cel = "{:.2f}".format((far - 32) / 1.8)
    except ValueError:
        cel = ""    
    entCelsius.delete(0, END)
    entCelsius.insert(0, cel)
    

winMain = NCtkWindow(100, 100, 300, 150, "Conversione C-F")
winMain.config_all(font=("Arial", 12))
labCelsius = NCtkLabel(winMain, 20, 20, 100, 40, "Celsius")
entCelsius = NCtkEntry(winMain, 140, 20, 140, 40)
entCelsius.config(bcolor="light grey", fcolor="red", sbcolor="red", sfcolor="white")
entCelsius.bind("<FocusIn>", getFocus)
labFarenheit = NCtkLabel(winMain, 20, 70, 100, 40, "Farenheit")
entFarenheit = NCtkEntry(winMain, 140, 70, 140, 40)
entFarenheit.config(bcolor="light grey", fcolor="green", sbcolor="green", sfcolor="white")
entFarenheit.bind("<FocusIn>", getFocus)

winMain.mainloop()