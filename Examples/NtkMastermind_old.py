import _setup           # allows import from parent folder
from Ntk import *
from random import choice, seed, random, randrange
from time import sleep


COLORS = ("#FF0000", "#FFFF00", "#FF8030", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF",
          "#B04040", "#B040B0", "#40B040")

MM_NONE, MM_COLOR, MM_SB, MM_ALL = 0, 1, 2, 3

NUM_TRIES = 12


class MoveLine:
    def __init__(self, parent):
        parent.add_row(40)
        self.boxes = []
        self.locked = MM_ALL
        for j in range(LEN):
            lab = NtkLabel(parent, PACK, 0, 40, 40, pad=5)
            lab.bind("<Button-1>", self.changeColor)
            lab.color = -1
            self.boxes.append(lab)
        for j in range(LEN):
            lab = NtkLabel(parent, PACK, CENTER, 30, 30, pad=5)
            lab.bind("<Button-1>", self.changeBlackWhite)
            lab.config(relief=SOLID, borderwidth=1)
            lab.color = -1
            self.boxes.append(lab)
            
    def reset(self, what=MM_ALL):
        for j in range(2 * LEN):
            if (j < LEN and what in (MM_COLOR, MM_ALL)) or (
                j >= LEN and what in (MM_SB, MM_ALL)):
                self.boxes[j].config(bcolor=BGCOLOR)
                self.boxes[j].color = -1                     
            
    def show(self, what):
        for j in range(2 * LEN):
            if j < LEN:
                if what in (MM_COLOR, MM_ALL):
                    self.boxes[j].show()
                else:
                    self.boxes[j].hide()
            else:
                if what in (MM_SB, MM_ALL):
                    self.boxes[j].show()
                else:
                    self.boxes[j].hide()
            
    def setLock(self, f):
        self.locked = f
        
    def setMove(self, pattern):
        """Given the four-digits string pattern, sets the appropriate
        colors for the boxes"""
        for i in range(LEN):
            color = int(pattern[i])
            self.boxes[i].color = color
            self.boxes[i].config(bcolor=COLORS[color])
            
    def getMove(self):
        """Returns the colors of the line as a string of LEN digits.
        If some color is unchosen (color = -1) raise a warning  and
        returns None"""
        move = ""
        for i in range(LEN):
            digit = self.boxes[i].color
            if digit == -1:
                tkmb.showwarning("Warning", "You must choose all colors")
                return None
            move += str(digit)
        return move
        
    def changeColor(self, event):
        if self.locked in (MM_NONE, MM_SB):
            col = event.widget.color
            col = (col + 1) % len(COLORS)
            event.widget.config(bcolor=COLORS[col])
            event.widget.color = col        

    def changeBlackWhite(self, event):
        if self.locked in (MM_NONE, MM_COLOR):
            col = (event.widget.color + 2) % 3 - 1
            if col == 0:
                event.widget.config(bcolor="black")
            elif col == 1:
                event.widget.config(bcolor="white")
            else:
                event.widget.config(bcolor=BGCOLOR)
            event.widget.color = col
        
    def setSB(self, strike, ball):
        self.reset(MM_SB)
        for i in range(strike):
            self.boxes[LEN + i].config(bcolor="black")
            self.boxes[LEN + i].color = 0
        for i in range(strike, strike + ball):
            self.boxes[LEN + i].config(bcolor="white")
            self.boxes[LEN + i].color = 1
            
    def getSB(self):
        strike, ball = 0, 0
        for i in range(LEN, 2 * LEN):
            if self.boxes[i].color == 0:
                strike += 1
            elif self.boxes[i].color == 1:
                ball += 1
        return strike, ball
                
            



class Game:
    status = "idle"
    training = False
    difficulty = 3
    assistance = 2
    nmoves = 1   
    
    def start(event=None):
        if Game.status == "idle":
            
            if Game.training:
                Game.trainingGame()
            else:
                if not comp_moves[0].getMove():
                    return
                Game.challengeGame()
            butStart.set_content("Reset")
            configButtons("ndd")
        
    def reset():
        Game.nmoves = 1
        for i in range(0, NUM_TRIES + 1):
            your_moves[i].show(MM_NONE)
            your_moves[i].reset()
            your_moves[i].setLock(MM_SB)
            comp_moves[i].show(MM_NONE)
            comp_moves[i].reset()
            comp_moves[i].setLock(MM_COLOR)
        if not Game.training:
            comp_moves[0].show(MM_COLOR)
            comp_moves[0].setLock(MM_NONE)
            labStat.set_content("Choose your pattern")
        butStart.set_content("Start")
        configButtons("ndd")
        Game.status = "idle"
        
    def trainingGame():
        configButtons("dnd")
        comp.start()
        Game.status = "playing"
        while Game.status != "end":
            move = you.move()
            strike, ball = comp.answer(move)
            you.getAnswer(strike, ball) 
            Game.checkWin()
            Game.nmoves += 1
            
    def challengeGame():
        configButtons("dnd")
        comp.start()
        you.start()
        Game.status = "playing"
        while Game.status != "end":
            configButtons("dnd")
            move = you.move()
            configButtons("ddd")
            strike, ball = comp.answer(move)
            you.getAnswer(strike, ball)
            winMain.update()
            move = comp.move()
            configButtons("ddn")
            strike, ball = you.answer(move)
            comp.getAnswer(strike, ball)
            configButtons("ddd")
            Game.checkWin()
            Game.nmoves += 1
            
            
    def checkWin():
        comp_strikes = comp_moves[Game.nmoves].getSB()[0]
        your_strikes = your_moves[Game.nmoves].getSB()[0]
        if your_strikes == LEN and comp_strikes == LEN:
            tkmb.showinfo("Mastermind", "Both computer and player win!")
        elif your_strikes == LEN:
            tkmb.showinfo("Mastermind", "You win!")
        elif comp_strikes == LEN:
            tkmb.showinfo("Mastermind", "The computer wins!")
        else:
            return
        your_moves[0].show(MM_COLOR)
        Game.status = "end"
        
                        
    def evaluate(patt, move):
        # patt, move are strings of digits 0 - 9
        # transform the strings in lists of integer
        pattcopy = [int(patt[i]) for i in range(LEN)]
        movecopy = [int(move[i]) for i in range(LEN)]
        strike, ball = 0, 0
        # find strikes (right number in right place)
        for i in range(LEN):
            if pattcopy[i] == movecopy[i]:
                strike += 1
                # if strike found exclude from further search
                pattcopy[i], movecopy[i] = -1, -1
        # find balls (right number in wrong place)
        for i in range(LEN):
            # skip already found as strike 
            if pattcopy[i] == -1:
                continue
            for j in range(LEN):
                if movecopy[j] == -1:
                    continue
                if pattcopy[i] == movecopy[j]:
                    ball += 1
                    pattcopy[i], movecopy[j] = -1, -1
                    break
        return strike, ball
    
            
            
class HumanPlayer:
    def __init__(self, moves1, moves2):
        self.your_moves = moves1
        self.other_moves = moves2
        self.your_patt = self.other_moves[0]
        self.pattern = ""
        
    def start(self):
        you.your_patt.setLock(MM_COLOR)
        self.pattern = you.your_patt.getMove()

    
    def move(self):
        """Show line n for the player and waits until he sets
        the colors. Returns the move as a string of digits"""
        line = self.your_moves[Game.nmoves]
        line.show(MM_ALL)
        line.setLock(MM_SB)
        self.done = False
        while not self.done:
            winMain.update()
        line.setLock(MM_ALL)
        return self.your_moves[Game.nmoves].getMove()
    
    def getAnswer(self, strike, ball):
        self.your_moves[Game.nmoves].setSB(strike, ball)
        
    def answer(self, move):
        line = self.other_moves[Game.nmoves]
        right_ans = False
        while not right_ans:
            self.done = False
            while not self.done:
                winMain.update()
            if Game.assistance == 1:
                strike, ball = Game.evaluate(self.pattern, line.getMove())
                line.setSB(strike, ball)
                right_ans = True
            else:
                if Game.assistance == 2:
                    strike, ball = line.getSB()
                    if (strike, ball) != Game.evaluate(self.pattern, line.getMove()):
                        tkmb.showwarning("Mastermind", "Your answer is incorrect!")
                        line.reset(MM_SB)
                    else:
                        right_ans = True
                else:
                    right_ans = True
        line.setLock(MM_ALL)
        return strike, ball
    
    def tryPattern(self, event):
        if not self.done and your_moves[Game.nmoves].getMove():
            self.done = True
            
    def tryAnswer(self, event):
        self.done = True


class CompPlayer:
    def __init__(self, moves1, moves2):
        self.your_moves = moves1
        self.other_moves = moves2
        self.your_patt = self.your_moves[0]
        self.pattern = ""
    
    def start(self):
        self.pattern =  ""
        for i in range(LEN):
            self.pattern += str(randrange(10))
        self.other_moves[0].setMove(self.pattern)
        if Game.training == False:
            self.generateChoices()
            labStat.set_content(str(len(self.choices)) + " moves left")
    
    def move(self):
        self.your_moves[Game.nmoves].show(MM_ALL)
        self.your_moves[Game.nmoves].setLock(MM_COLOR)
        your_move = choice(self.bestChoices())
        self.your_moves[Game.nmoves].setMove(your_move)
        return your_move
    
    
    def getAnswer(self, strike, ball):
        move = self.your_moves[Game.nmoves].getMove()
        self.cutChoices(move, strike, ball, self.choices, Game.difficulty)
        labStat.set_content(str(len(self.choices)) + " moves left")
        
        
    def answer(self, move):
        return Game.evaluate(self.pattern, move)
    
    
    def generateChoices(self):
        self.choices = []
        for i in range(10000):
            self.choices.append(format(str(i), "0>4"))    
    
    def cutChoices(self, move, strike, ball, choices, prob):
        """Removes from the list choices many moves which do not match
        the strike-ball pattern with respect to move. It does This
        in a probabilistic way to obtain different levels of difficulty"""
        if strike != LEN:
            choices.remove(move)
        new_choices = choices.copy()
        for patt in new_choices:
            tstrike, tball = Game.evaluate(patt, move)
            if (tstrike, tball) != (strike, ball) and random() < prob:
                choices.remove(patt)
                      
    TOO_BIG = 1000
    MAX_MOVES = 100
            
    def bestChoices(self):
        if len(self.choices) > self.TOO_BIG:
            sleep(1.0)
            return self.choices
        labStat.set_content("Thinking in Python!\nPlease be patient")
        betterChoices = []
        better = 100000
        num = 0
        for move in self.choices:
            num += 1
            print("Evaluating", num, "of", len(self.choices), "; better number =", better)
            temp_better = 0
            for patt in self.choices:
                if patt == move:
                    temp_better += 1
                    continue
                tstrike, tball = Game.evaluate(patt, move)
                for other_patt in self.choices:
                    if (tstrike, tball) == Game.evaluate(other_patt, move):
                        temp_better += 1
                        if temp_better > better:
                            break
                if temp_better > better:
                    break
            if temp_better < better:
                betterChoices.clear()
                better = temp_better
                betterChoices.append(move)
            elif temp_better == better:
                betterChoices.append(move)
            if num > self.MAX_MOVES:
                print("Max analysis limit reached")
                break
            winMain.update()
        if len(betterChoices) == 0:
            return self.choices
        else:
            return betterChoices
                            
            
            
            ##########################################################################
            
                        
LEN = 4
STR_RULES = "You must guess the combination of 4 colors chosen by the computer (colors can be repeated)."
"At each attempt the computer will report the number of strikes (black squares: right colors in the right "
"position) and balls (white squares: right colors but in the wrong position)"""
            
STR_CREDITS = """
M  A  S  T  E  R  M  I  N  D
copyright 2021 by Nicola Cassetta"""

AUTO_ANS, CORRECT_WRONG, NO_CORRECT = 1, 2, 3
                        
def howtoplay(event):
    tkmb.showinfo("Mastermind", STR_RULES)
    
def credits(event):
    tkmb.showinfo("Mastermind", STR_CREDITS)

def setMode(event):
    Game.training = event.value
            
def setDifficulty(event):
    Game.difficulty = 0.2 * event.value
    
def setAssistance(event):
    Game.assistance = event.value

def startReset(event):
    if event.widget.get_content() == "Reset":
        event.widget.set_content("Start")
        Game.reset()
    else:
        Game.start()

def configButtons(state):
    """To spare a lot of config. This sets the three buttons
    butStart, butTry and ButAns normal or disabled. state is a string
    of three chars: "x" leave the button in its state, "n" set it
    normal and "d" set it disabled"""
    buttons = (butStart, butTry, butAns)
    state.lower()
    for i in range(3):
        if state[i] == "x":
            continue
        elif state[i] == "n":
            buttons[i].config(state="normal")
        elif state[i] == "d":
            buttons[i].config(state="disabled")




winMain= NtkMain(100, 100, 800, 600, "Ntk Mastermind")
BGCOLOR = winMain.get_config("bcolor")

## menu
menuBar = NtkMenu(winMain)
menuFile = NtkMenu(menuBar, "File   ")
menuFile.add_command(label="Quit", command=winMain.destroy)
menuGame = NtkMenu(menuBar, "Game   ")
menuMode = NtkMenu(menuGame, "Mode   ")
modeStr = StringVar("")
menuMode.add_radiobutton(label="Training", variable=modeStr,
                         command=lambda ev: comp.settattr(training, True))
menuMode.add_radiobutton(label="Play against computer", variable=modeStr,
                         command=lambda ev: comp.setattr(training, False))
menuDiff = NtkMenu(menuGame, "Difficulty")
diffStr = StringVar("")
menuDiff.add_radiobutton(label="1 - Easier", variable=diffStr,
                         command=lambda ev: comp.setattr(difficulty, 0.2))
menuDiff.add_radiobutton(label="2         ", variable=diffStr,
                         command=lambda ev: comp.setattr(difficulty, 0.4))
menuDiff.add_radiobutton(label="3 - Normal", variable=diffStr,
                         command=lambda ev: comp.setattr(difficulty, 0.6))
menuDiff.add_radiobutton(label="4         ", variable=diffStr,
                         command=lambda ev: comp.setattr(difficulty, 0.8))
menuDiff.add_radiobutton(label="5 - Harder", variable=diffStr,
                         command=lambda ev: comp.setattr(difficulty, 1.0))
menuAss = NtkMenu(menuGame, "Assistance")
assStr = StringVar("")
menuAss.add_radiobutton(label="Auto answer", variable=assStr,
                        command=lambda ev: comp.setattr(assistance, AUTO_ANS))
menuAss.add_radiobutton(label="Correct wrong answers", variable=assStr,
                        command=lambda ev: comp.setattr(assistance, CORRECT_WRONG))
menuAss.add_radiobutton(label="No correction", variable=assStr,
                        command=lambda ev: comp.setattr(assistance, NO_CORRECT))
menuHelp = NtkMenu(menuBar, "Help   ")
menuHelp.add_command(label="How to play", command=lambda ev: tkmb.showinfo("Mastermind", STR_RULES))
menuHelp.add_command(label="Credits", command=lambda ev: tkmb.showinfo("Mastermind", STR_CREDITS)) 

# frames for player and computer
rfrYou = NtkRowFrame(winMain, 10, 10, "40%", -10)
rfrYou.config(relief=RIDGE, borderwidth=2)
rfrYou.add_row(50)
labYou = NtkLabel(rfrYou, 0, 0, FILL, FILL, pad=(10,5), content="you")
labYou.config(bcolor="light blue", fcolor="dark blue", anchor="center",
                   font=("Arial", 16, "bold"))

rfrComp = NtkRowFrame(winMain, "40%", 10,  "40%", -10)
rfrComp.config(relief=RIDGE, borderwidth=2)
rfrComp.add_row(50)
labComp = NtkLabel(rfrComp, 0, 0, FILL, FILL, pad=(10,5), content="the computer")
labComp.config(bcolor="light green", fcolor="dark green", anchor="center",
                   font=("Arial", 16, "bold"))

your_moves = []
comp_moves = []
for i in range(NUM_TRIES + 1):
    your_moves.append(MoveLine(rfrYou))
    comp_moves.append(MoveLine(rfrComp))

you = HumanPlayer(your_moves, comp_moves)
comp = CompPlayer(comp_moves, your_moves)

butStart = NtkButton(winMain,"80%", 100, 80, 40, pad=(10,5), content="Start", command=startReset)
butTry = NtkButton(winMain, "80%", 140, 80, 40, pad=(10,5), content="Try", command=you.tryPattern)
butAns = NtkButton(winMain, "80%", 180, 80, 40, pad=(10,5), content="Answer", command=you.tryAnswer)

labStat = NtkLabel(winMain, "80%", 220, -20, 60, pad=(10,5))
labStat.config(bcolor="white", font=("Arial", 10))

# set correct menu items
menuMode.invoke("Play against computer")
menuDiff.invoke("3 - Normal")
menuAss.invoke("Correct wrong answers")

winMain.update_idletasks()
Game.reset() 

mainloop()