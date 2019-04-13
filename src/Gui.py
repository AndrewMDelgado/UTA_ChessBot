from tkinter import Tk, ttk, LEFT, RIGHT, BOTTOM, TOP, BOTH, \
    N, S, E, W, NW, Button, Radiobutton, Label, IntVar, NORMAL, DISABLED
import Game
import tkinter.messagebox as msgbox

WHITE = True
BLACK = False


class GUI:

    def dispAIMove(self, moveStr):
        msg = moveStr[5:7] + ' to ' + moveStr[7:]
        msg += "\nMake your move and press OK."
        msgbox.showinfo("AI Move", msg)

    def getPlayerMove(self):
        window = Tk()
        window.wm_title("Player Move")
        window.mainloop()
    
    def showinfo(self, title, msg):
        msgbox.showinfo(title, msg)


def guiMain():
    winMain = Tk()
    winMain.wm_title("UTA Chess Bot")
    winMain.config(width=480, height=270)
    winMain.pack_propagate(False)
    winMain.resizable(False, False)
    winMain.mainloop()


def guiStart():

    def plSel():
        if int(plColor.get()) == 1:
            msg = "White goes first."
            L1.config(state=NORMAL)
            L2.config(state=NORMAL)
            L3.config(state=NORMAL)
            aiLabel.config(state=NORMAL)

        elif int(plColor.get()) == 2:
            msg = "Black goes second."
            L1.config(state=NORMAL)
            L2.config(state=NORMAL)
            L3.config(state=NORMAL)
            aiLabel.config(state=NORMAL)

        elif int(plColor.get()) == 3:
            msg = "Two-player; no AI"
            L1.config(state=DISABLED)
            L2.config(state=DISABLED)
            L3.config(state=DISABLED)
            aiLabel.config(state=DISABLED)
        
        plLabel.config(text=msg)

    def aiSel():
        if int(aiLevel.get()) == 1:
            msg = "AI does not look ahead."
        elif int(aiLevel.get()) == 2:
            msg = "AI looks one move ahead."
        elif int(aiLevel.get()) == 3:
            msg = "AI looks two moves ahead."

        aiLabel.config(text=msg)
    
    def startGame():
        aiDepth = aiLevel.get()
        playerSide = (plColor.get() == 1) #True corresponds to WHITE
        if plColor.get() == 3: #Two-player game
            aiDepth = 0
        
        if playerSide or (aiDepth == 0): #WHITE; white goes first
            msgbox.showinfo("First move", "WHITE, make your first move and press OK.")
        Game.startFromGui(playerSide, aiDepth)
        winStart.destroy()
        guiMain()
    
    def exitGame():
        exit(0)

    winStart = Tk()
    winStart.wm_title("Config Game")
    winStart.config(width=360, height=225)
    winStart.pack_propagate(False)
    #winStart.resizable(False, False)
    
    frames = {}
    frames['options'] = ttk.Frame(winStart)
    frames['options'].pack(side=TOP, pady=10)
    
    frames['color'] = ttk.LabelFrame(frames['options'], text='Player Color', labelanchor=NW, width = 175, height = 150)
    frames['level'] = ttk.LabelFrame(frames['options'], text='AI Level', labelanchor=NW, width = 175, height = 150)
    frames['color'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT)
    frames['level'].pack(fill=BOTH, expand=True, anchor=N, side=RIGHT)
    frames['color'].pack_propagate(False)
    frames['level'].pack_propagate(False)
    
    plColor = IntVar()
    plColor.set(1)
    P1 = Radiobutton(frames['color'], text="White", variable=plColor, value=1, command=plSel)
    P2 = Radiobutton(frames['color'], text="Black", variable=plColor, value=2, command=plSel)
    P3 = Radiobutton(frames['color'], text="Two-Player", variable=plColor, value=3, command=plSel)
    P1.pack(anchor=W)
    P2.pack(anchor=W)
    P3.pack(anchor=W)

    plLabel = Label(frames['color'], text="White goes first.")
    plLabel.pack(anchor=W, pady=20)

    aiLevel = IntVar()
    aiLevel.set(2)
    L1 = Radiobutton(frames['level'], text="Level 1", variable=aiLevel, value=1, command=aiSel)
    L2 = Radiobutton(frames['level'], text="Level 2", variable=aiLevel, value=2, command=aiSel)
    L3 = Radiobutton(frames['level'], text="Level 3", variable=aiLevel, value=3, command=aiSel)
    L1.pack(anchor=W)
    L2.pack(anchor=W)
    L3.pack(anchor=W)

    aiLabel = Label(frames['level'], text="AI looks one move ahead.")
    aiLabel.pack(anchor=W, pady=20)

    frames['start'] = ttk.Frame(winStart)
    frames['start'].pack()
    startButton = Button(frames['start'], text="Start Game", command=startGame)
    startButton.pack(side=LEFT, padx = 15, pady=15)
    exitButton = Button(frames['start'], text="Exit", command=exitGame)
    exitButton.pack(side=RIGHT, pady=15)
    
    #winStart.state('zoomed')
    winStart.mainloop()


if __name__ == '__main__':
    guiStart()
