Ntk
===

A simple tkinter wrapper by Nicola Cassetta
-------------------------------------------

Ntk is a wrapper for **tkinter** written by Nicola Cassetta with the aim of simplifying its use for building graphical interfaces with Python.

As is known, tkinter is the Python standard library already included in the language distribution; it derives from **Tcl/Tk** and maintains its nomenclature and conventions in names and parameters of the functions, so they are often difficult to remember. It also has three different geometry managers (_pack_, _grid_ and _place_) for placing widgets, which can be confusing. One of the most popular features is its ability to easily resize widgets when the main window is resized, but this often leads to strange behavior. For example, the standard behavior of an Entry object (the text field widget) is to grow larger as we type text into it. If we packed other widgets to its right all of them will move. Another problem arises for widget dimensions, which are in pixel for some of them (for example Button, Canvas) and in charachters for other (Label, Entry).

These things are not a problem for experienced developers, but can confuse people approaching the design of a GUI using tkinter. So I tried to simplify these problems by adopting some general principles: 

 - All widgets have a similar constructor, which enable the user to easily position them, with sizes always specified in pixels.
 - As in tkinter, widgets can change their position and size when the main window is resized.
 - Some tkinter options for widget **config()** method have been renamed in a more coherent manner, so it is easier to remember them. Also the almost infinite series of **winfo_...** methods have been packed into the unique **get_winfo()** method, with a string parameter.
 - I renamed also some functions, trying to mantain the <em>xxxx_yyyy</em> scheme recommended in PEP 8 (this, however, is not complete)

This is the <a href="https://ncassetta.github.io/Ntk">link to the documentation</a>.

This is an example of a "Hello world"

    import Ntk

    #callback for the button
    def hide_show(event):
        if labHello.visible():
            labHello.hide()
            btnShow.set_content("Show label")
        else:
            labHello.show()
            btnShow.set_content("Hide label")

    # Creates the main window (400x300 with left upper corner in (100, 100)
    winMain = Ntk.NtkMain(100, 100, 400, 300, title="First Sample")
    # Creates a label in it (first argument of children widgets always is the parent,
    # subsequent four its dimensions, then other widget specific)
    labHello = Ntk.NtkLabel(winMain, "center", 60, "80%", 100, content="Hello world!")
    # Changes label properties: background color, foreground color, font, centered text
    labHello.config(bcolor="yellow", fcolor="dark blue", font=("Arial", 32), anchor="center")
    # Creates a button, assigning a callback to it
    btnShow = Ntk.NtkButton(winMain, "center", 200, 100, 40, content="Hide label", command=hide_show) 

    #enter the control loop
    Ntk.mainloop()
