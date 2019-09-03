from Mtki import *


def getFocus(event):
    if event.widget == entryCelsius:
        entryCelsius.bind("<Return>", toFarenheit)
        entryCelsius.configure(bg="white")
        entryFarenheit.bind("<FocusIn>", getFocus)
        entryFarenheit.configure(bg="light grey")
    else:
        entryCelsius.bind("<FocusIn>", getFocus)
        entryCelsius.configure(bg="light grey")
        entryFarenheit.bind("<Return>", toCelsius)    
        entryFarenheit.configure(bg="white")

def toFarenheit(event):
    try:
        print(entryCelsius.get())
        cel = float(entryCelsius.get())
        far = cel * 1.8 + 32
        entryFarenheit.delete(0, END)
        entryFarenheit.insert(0, str(far))
    except:
        entryFarenheit.delete(0, END)
        
def toCelsius(event):
    try:
        far = float(entryFarenheit.get())
        cel = (far - 32) / 1.8 
        entryCelsius.delete(0, END)
        entryCelsius.insert(0, str(cel))
    except:
        entryCelsius.delete(0, END)


mainWindow = MtkiWindow(400, 300, 100, 100, "Prova")
labCelsius = MtkiLabel(mainWindow, 100, 20, 20, 20, "Celsius")
entryCelsius = MtkiEntry(mainWindow, 100, 20, 130, 20)
entryCelsius.bind("<FocusIn>", getFocus)
labFarenheit = MtkiLabel(mainWindow, 100, 20, 20, 50, "Farenheit")
entryFarenheit = MtkiEntry(mainWindow, 100, 20, 130, 50)
entryFarenheit.bind("<FocusIn>", getFocus)

mainWindow.mainloop()