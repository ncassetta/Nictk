from NCtk import *


def getFocus(event):
    if event.widget == entryCelsius:
        entryCelsius.bind("<Return>", toFarenheit)
        entryCelsius.config(bcolor="white")
        entryFarenheit.bind("<FocusIn>", getFocus)
        entryFarenheit.config(bcolor="light grey")
    else:
        entryCelsius.bind("<FocusIn>", getFocus)
        entryCelsius.config(bcolor="light grey")
        entryFarenheit.bind("<Return>", toCelsius)    
        entryFarenheit.config(bcolor="white")

def toFarenheit(event):
    try:
        print(entryCelsius.get())
        cel = float(entryCelsius.get())
        far = "{:.2f}".format(cel * 1.8 + 32)
        entryFarenheit.delete(0, END)
        entryFarenheit.insert(0, far)
    except:
        entryFarenheit.delete(0, END)
        
def toCelsius(event):
    try:
        far = float(entryFarenheit.get())
        cel = "{:.2f}".format((far - 32) / 1.8)
        entryCelsius.delete(0, END)
        entryCelsius.insert(0, cel)
    except:
        entryCelsius.delete(0, END)


mainWindow = NCtkWindow(100, 100, 300, 150, "Prova")
labCelsius = NCtkLabel(mainWindow, 20, 20, 100, 40, "Celsius")
entryCelsius = NCtkEntry(mainWindow, 140, 20, 140, 40)
entryCelsius.bind("<FocusIn>", getFocus)
labFarenheit = NCtkLabel(mainWindow, 20, 70, 100, 40, "Farenheit")
entryFarenheit = NCtkEntry(mainWindow, 140, 70, 140, 40)
entryFarenheit.bind("<FocusIn>", getFocus)

mainWindow.mainloop()