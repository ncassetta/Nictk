from Mtki import *


COLORS = ("red", "yellow", "cyan", "green", "purple", "blue", "orange",
          "light green", "violet", "brown")

NUM_TRIES = 12
XYOU_BASE = 10
XCOMP_BASE = 300
Y_BASE = 100

you_pattern = []
you_tries = []
comp_tries = []
you_results = []
comp_results = []
game_status = ""
moves = 0

def getColor(w):
    return w.data[2]

def setColor(w, col):
    w.data[2] = col
    
def resetColor(w):
    w.configure(bg=BGCOLOR)
    setColor(w, -1)

def changeColor(event):
    col = getColor(event.widget)
    col = (col + 1) % len(COLORS)
    event.widget.configure(bg=COLORS[col])
    setColor(event.widget, col)
    
def changeBlackWhite(event):
    col = getColor(event.widget)
    if col == 0:
        event.widget.configure(bg="black")
        setColor(event.widget, 1)
    else:
        event.widget.configure(bg="white")
        setColor(event.widget, 0)

def createLines():
    for j in range(4):
        lab = MtkiLabel(mainWindow, 25, 25, XCOMP_BASE + 30 * j, Y_BASE - 40, "")
        lab.data.extend([0, 0, -1])
        lab.bind("<Button-1>", changeColor)
        you_pattern.append(lab)
    for i in range(NUM_TRIES):
        y = Y_BASE + i * 40
        you_tries.append([])
        for j in range(4):
            lab = MtkiLabel(mainWindow, 25, 25, XYOU_BASE + 30 * j, y, "")
            lab.data.extend([i, j, -1])
            lab.bind("<Button-1>", changeColor)
            you_tries[i].append(lab)
        you_results.append([])
        for j in range(4):
            lab = MtkiLabel(mainWindow, 15, 15, XYOU_BASE + 125 + 20 * j, y + 5, "")
            lab.data.extend([i, j, -1])
            you_results[i].append(lab)
        comp_tries.append([])
        for j in range(4):
            lab = MtkiLabel(mainWindow, 25, 25, XCOMP_BASE + 30 * j, y, "")
            lab.data.extend([i, j, -1])
            comp_tries[i].append(lab)
        comp_results.append([])
        for j in range(4):
            lab = MtkiLabel(mainWindow, 15, 15, XCOMP_BASE + 125 + 20 * j, y + 5, "")
            lab.data.extend([i, j, -1])
            lab.bind("<Button-1>", changeBlackWhite)
            comp_results[i].append(lab)
            
def showLine(n, who):
    if who == "you":
        for i in range(4):
            you_tries[n][i].show()
            you_results[n][i].show()
    else:
        for i in range(4):
            comp_tries[n][i].show()
            comp_results[n][i].show()
        
    
def resetGame():
    global game_status, moves
    game_status = "idle"
    moves = 0
    for j in range(4):
        resetColor(you_pattern[j])
    for i in range(NUM_TRIES):
        for j in range(4):
            you_tries[i][j].hide()
            resetColor(you_tries[i][j])
            you_results[i][j].hide()
            resetColor(you_results[i][j])
            comp_tries[i][j].hide()
            resetColor(comp_tries[i][j])
            comp_results[i][j].hide()
            resetColor(comp_results[i][j])
            
def start(event):
    global game_status
    if game_status == "idle":
        resetGame()
        game_status = "choose_pattern"
        print("Start 1")
    elif game_status == "choose_pattern":
        print("Start 2")
    game()
        
        
def trypattern(event):
    global game_status
    if game_status == "waiting_for_you":
        game_status = "waiting_for_comp"
        
def game():
    global game_status, moves, mainWindow
    while game_status != "end":
        game_status = "waiting_for_you"
        showLine(moves, "you")
        while game_status == "waiting_for_you":
            mainWindow.update()
        print("Ciao")
        moves += 1


mainWindow = MtkiWindow(800, 600, 100, 100, "Mtki Mastermind")
BGCOLOR = mainWindow.cget("bg")
youLabel = MtkiLabel(mainWindow, 200, 30, XYOU_BASE, 10, "you")
youLabel.configure(bg="light blue", fg="dark blue", anchor="center",
                   font=("Arial", 16, "bold"))
compLabel = MtkiLabel(mainWindow, 200, 30, XCOMP_BASE, 10, "the computer")
compLabel.configure(bg="light green", fg="dark green", anchor="center",
                   font=("Arial", 16, "bold"))
startButton = MtkiButton(mainWindow, 50, 30, 560, 100, "Start", start)
tryButton = MtkiButton(mainWindow, 50, 30, 560, 140, "Try", trypattern)
ansButton = MtkiButton(mainWindow, 50, 30, 560, 180, "Answer")
createLines()
resetGame()


mainWindow.mainloop()