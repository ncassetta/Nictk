from Mtki import *
from time import *

strings = ["aaaa", "bbbb", "cccc", "dddd", "eeee"]
bcolors = ("#C00080", "#4040C0", "#804080", "#C08000", "#C04080")
fcolors = ("#C0FF80", "#FFC080", "#FF80FF", "#80FFFF", "#C0C0C0")


def change(event):
    global stringind, colorind
    if event.widget == buttText:
        stringind = (stringind + 1) % len(strings)
        labText.settext(strings[stringind])
    elif event.widget == buttColor:
        colorind = (colorind + 1) % 5
        labText.config(bg = bcolors[colorind], fg = fcolors[colorind])
    else:
        strings.append(entryText.gettext())
        stringind = len(strings) - 1
        labText.settext(strings[stringind])


stringind = 0
colorind = 0
winMain = MtkiWindow(400, 300, 200, 150, "App prova")
labText = MtkiLabel(winMain, "fill", 60, 10, 10, strings[0])
buttText = MtkiButton(winMain, "50%", 30, 10, 80, "Cambia Testo", change)
buttText.configure(highlightcolor="#ABCDEF")
buttColor = MtkiButton(winMain, "50%", 30, 120, 80, "Cambia Colori", change)
entryText = MtkiEntry(winMain, 120, 30, 10, 120, "", change)
mainloop()