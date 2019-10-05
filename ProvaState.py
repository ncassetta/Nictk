from NCtk import *
from time import *

strings = ["aaaa", "bbbb", "cccc", "dddd", "eeee"]
bcolors = ("#C00080", "#4040C0", "#804080", "#C08000", "#C04080")
fcolors = ("#C0FF80", "#FFC080", "#FF80FF", "#80FFFF", "#C0C0C0")


def change(event):
    global stringind, colorind
    if event.widget == butText:
        stringind = (stringind + 1) % len(strings)
        labText.settext(strings[stringind])
    elif event.widget == butColor:
        colorind = (colorind + 1) % 5
        labText.config(bcolor = bcolors[colorind], fcolor = fcolors[colorind])
    else:
        strings.append(entText.gettext())
        stringind = len(strings) - 1
        labText.settext(strings[stringind])
        
def changelabstatus(event):
    txt = butHideShow.gettext()
    if txt == "Disabilita":
        labText.config(state=DISABLED)
        k = entText.config(state=DISABLED)
        newind = 1
    elif txt == "Nascondi":
        labText.hide()
        entText.hide()
        newind = 2
    elif txt == "Mostra":
        labText.show()
        entText.show()
        newind = 3
    else:
        labText.config(state=NORMAL)
        entText.config(state=NORMAL)
        newind = 0
    butHideShow.settext(butHideShow.captions[newind])    


stringind = 0
colorind = 0
winMain = NCtkWindow(200, 150, 400, 300, "App prova")
labText = NCtkLabel(winMain, 10, 10, "fill", 60, strings[0])
labText.config(dfcolor="red", abcolor="gold")
hfr1 = NCtkHorFrame(winMain, 0, "pack", "fill", 50)
butText = NCtkButton(hfr1, 10, 5, "20%", "fill", "Cambia Testo", change)
butText.config(hcolor="#ABCDEF")
butColor = NCtkButton(hfr1, "pack", 5, "20%", "fill", "Cambia Colori", change)
entText = NCtkEntry(winMain, 10, 130, 120, 30, "", change)
butHideShow = NCtkButton(winMain, 10, 200, "15%", 40, "", changelabstatus)
butHideShow.captions = ("Disabilita", "Nascondi", "Mostra", "Abilita")
butHideShow.config(text=butHideShow.captions[0])
mainloop()