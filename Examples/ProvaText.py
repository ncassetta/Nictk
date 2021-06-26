import _setup           # allows import from parent folder
from Ntk import *

times = 0

def changed_callback():
    times += 1
    lab1.config(text='Changed ' + str(times) + ' times')

winMain = NtkMain(100, 100, 800, 600, "Prova NtkText widget")
winMain.config_children("all", font=("Arial", 12))
vfr1 = NtkVerFrame(winMain, 0, 0, '80%', '80%')
lab1 = NtkLabel(vfr1, 10, 10, 'fill', 50, pad=(5, 5), content="Ntk text")
txt1 = NtkText(vfr1, 10, 'pack', 'fill', 'fill', pad=(5, 5))
txt1.tag_add(ALL, '0.1', END)
txt1.tag_bind(ALL, func=changed_callback)


winMain.mainloop()