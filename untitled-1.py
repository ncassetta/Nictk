#import _setup
import NCtk


m = NCtk.NCtkMenu(None)
m.add_command(label="O1")
m.add_command(label="O2")
m.add_separator()
m.delete(2, 5)
