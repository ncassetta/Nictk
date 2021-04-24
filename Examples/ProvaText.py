from NCtk import *

times = 0

def changed_callback():
    times += 1
    lab1.config(text='Changed ' + str(times) + ' times')

winMain = NCtkWindow(100, 100, 800, 600, "Prova NCtkText widget")
winMain.config_all(font=("Arial", 12))
vfr1 = NCtkVerFrame(winMain, 0, 0, '80%', '80%')
lab1 = NCtkLabel(vfr1, 10, 10, 'fill', 50, 'NCtkText widget', pad=(5, 5))
txt1 = NCtkText(vfr1, 10, 'pack', 'fill', 'fill', pad=(5, 5))
txt1.tag_add('ALL', '0.1', END)
txt1.tag_bind('ALL', func=changed_callback)


winMain.mainloop()