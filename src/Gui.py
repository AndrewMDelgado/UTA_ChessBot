from tkinter import Tk, ttk, LEFT, RIGHT, BOTTOM, TOP, BOTH, Grid, \
    N, S, E, W, NW, NE, Button, Radiobutton, Label, Entry, IntVar, BooleanVar, StringVar, NORMAL, DISABLED
import os
import Game
import tkinter.messagebox as msgbox

WHITE = True
BLACK = False


class GUI:

    def __init__(self, physInput):
        self.physInput = physInput

    def dispAIMove(self, moveStr):
        msg = moveStr[5:7] + ' to ' + moveStr[7:]
        msg += "\nPlease move my piece for me and press OK."
        msgbox.showinfo("AI Move", msg)
        self.physInput.promptCamera(True)
        msg = "Make your move and press OK."
        msgbox.showinfo("Player Move", msg)

    def getPlayerMove(self):

        def giveMove():
            moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'
            filename = moveDir + 'playerMove.txt'
            output = open(filename, "w")
            output.write('1 ' + iFile.get() + iRank.get() + ' ' + fFile.get() + fRank.get())
            output.close()
            winMove.destroy()
            return

        winMove = Tk()
        winMove.wm_title("Player Move")
        winMove.config(width=480, height=300)
        frames = {}
        frames['spaces'] = ttk.Frame(winMove)
        frames['spaces'].pack(side=TOP, pady=10)

        frames['space_i'] = ttk.LabelFrame(frames['spaces'], text='From', labelanchor=NW, width=235, height=250)
        frames['space_f'] = ttk.LabelFrame(frames['spaces'], text='To', labelanchor=NW, width=235, height=250)
        frames['space_i'].pack(side=LEFT)
        frames['space_f'].pack(side=RIGHT)
        frames['space_i'].pack_propagate(False)
        frames['space_f'].pack_propagate(False)

        frames['space_iF'] = ttk.Frame(frames['space_i'], width=165, height=250)
        frames['space_iR'] = ttk.Frame(frames['space_i'], width=165, height=250)
        frames['space_fF'] = ttk.Frame(frames['space_f'], width=165, height=250)
        frames['space_fR'] = ttk.Frame(frames['space_f'], width=165, height=250)
        frames['space_iF'].pack(side=LEFT)
        frames['space_iR'].pack(side=RIGHT)
        frames['space_fF'].pack(side=LEFT)
        frames['space_fR'].pack(side=RIGHT)
        
        iFile = StringVar()
        iRank = StringVar()
        iFile.set('A')
        iRank.set('1')
        iF1 = Radiobutton(frames['space_iF'], text='A', variable=iFile, value='A')
        iF2 = Radiobutton(frames['space_iF'], text='B', variable=iFile, value='B')
        iF3 = Radiobutton(frames['space_iF'], text='C', variable=iFile, value='C')
        iF4 = Radiobutton(frames['space_iF'], text='D', variable=iFile, value='D')
        iF5 = Radiobutton(frames['space_iF'], text='E', variable=iFile, value='E')
        iF6 = Radiobutton(frames['space_iF'], text='F', variable=iFile, value='F')
        iF7 = Radiobutton(frames['space_iF'], text='G', variable=iFile, value='G')
        iF8 = Radiobutton(frames['space_iF'], text='H', variable=iFile, value='H')
        iF1.pack(anchor=NW)
        iF2.pack(anchor=NW)
        iF3.pack(anchor=NW)
        iF4.pack(anchor=NW)
        iF5.pack(anchor=NW)
        iF6.pack(anchor=NW)
        iF7.pack(anchor=NW)
        iF8.pack(anchor=NW)
        iR1 = Radiobutton(frames['space_iR'], text='1', variable=iRank, value='1')
        iR2 = Radiobutton(frames['space_iR'], text='2', variable=iRank, value='2')
        iR3 = Radiobutton(frames['space_iR'], text='3', variable=iRank, value='3')
        iR4 = Radiobutton(frames['space_iR'], text='4', variable=iRank, value='4')
        iR5 = Radiobutton(frames['space_iR'], text='5', variable=iRank, value='5')
        iR6 = Radiobutton(frames['space_iR'], text='6', variable=iRank, value='6')
        iR7 = Radiobutton(frames['space_iR'], text='7', variable=iRank, value='7')
        iR8 = Radiobutton(frames['space_iR'], text='8', variable=iRank, value='8')
        iR1.pack(anchor=E)
        iR2.pack(anchor=E)
        iR3.pack(anchor=E)
        iR4.pack(anchor=E)
        iR5.pack(anchor=E)
        iR6.pack(anchor=E)
        iR7.pack(anchor=E)
        iR8.pack(anchor=E)

        fFile = StringVar()
        fRank = StringVar()
        fFile.set('A')
        fRank.set('2')
        fF1 = Radiobutton(frames['space_fF'], text='A', variable=fFile, value='A')
        fF2 = Radiobutton(frames['space_fF'], text='B', variable=fFile, value='B')
        fF3 = Radiobutton(frames['space_fF'], text='C', variable=fFile, value='C')
        fF4 = Radiobutton(frames['space_fF'], text='D', variable=fFile, value='D')
        fF5 = Radiobutton(frames['space_fF'], text='E', variable=fFile, value='E')
        fF6 = Radiobutton(frames['space_fF'], text='F', variable=fFile, value='F')
        fF7 = Radiobutton(frames['space_fF'], text='G', variable=fFile, value='G')
        fF8 = Radiobutton(frames['space_fF'], text='H', variable=fFile, value='H')
        fF1.pack(anchor=NW)
        fF2.pack(anchor=NW)
        fF3.pack(anchor=NW)
        fF4.pack(anchor=NW)
        fF5.pack(anchor=NW)
        fF6.pack(anchor=NW)
        fF7.pack(anchor=NW)
        fF8.pack(anchor=NW)
        fR1 = Radiobutton(frames['space_fR'], text='1', variable=fRank, value='1')
        fR2 = Radiobutton(frames['space_fR'], text='2', variable=fRank, value='2')
        fR3 = Radiobutton(frames['space_fR'], text='3', variable=fRank, value='3')
        fR4 = Radiobutton(frames['space_fR'], text='4', variable=fRank, value='4')
        fR5 = Radiobutton(frames['space_fR'], text='5', variable=fRank, value='5')
        fR6 = Radiobutton(frames['space_fR'], text='6', variable=fRank, value='6')
        fR7 = Radiobutton(frames['space_fR'], text='7', variable=fRank, value='7')
        fR8 = Radiobutton(frames['space_fR'], text='8', variable=fRank, value='8')
        fR1.pack(anchor=E)
        fR2.pack(anchor=E)
        fR3.pack(anchor=E)
        fR4.pack(anchor=E)
        fR5.pack(anchor=E)
        fR6.pack(anchor=E)
        fR7.pack(anchor=E)
        fR8.pack(anchor=E)
        
        frames['button'] = ttk.Frame(winMove)
        frames['button'].pack()
        submit = Button(frames['button'], text="Give input", command=giveMove)
        submit.pack(side=LEFT, padx = 15, pady=15)
    
        winMove.mainloop()
    
    def promptMove(self):
        def giveMove():
            moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'
            filename = moveDir + 'playerMove.txt'
            output = open(filename, "w")
            output.write('1 ' + e1.get() + ' ' + e2.get())
            winPrompt.destroy()
            return

        winPrompt = Tk()
        Label(winPrompt, text="Initial Space (e.g. \"A2\")").grid(row=0)
        Label(winPrompt, text="Final Space (e.g. \"A3\")").grid(row=1)
        e1 = Entry(winPrompt)
        e2 = Entry(winPrompt)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        Button(winPrompt, text="Give move", command=giveMove).grid(row=3, pady=5)
        winPrompt.mainloop()
        return
    
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
        
        useCamera = inFormat.get()
        winStart.destroy()
        Game.startFromGui(playerSide, aiDepth, useCamera)
        guiMain()
    
    def exitGame():
        exit(0)

    winStart = Tk()
    winStart.wm_title("Config Game")
    winStart.config(width=480, height=225)
    winStart.pack_propagate(False)
    #winStart.resizable(False, False)
    
    frames = {}
    frames['options'] = ttk.Frame(winStart)
    frames['options'].pack(side=TOP, pady=10)
    
    frames['color'] = ttk.LabelFrame(frames['options'], text='Player Color', labelanchor=NW, width = 155, height = 150)
    frames['level'] = ttk.LabelFrame(frames['options'], text='AI Level', labelanchor=NW, width = 155, height = 150)
    frames['input'] = ttk.LabelFrame(frames['options'], text='Input Format', labelanchor=NW, width=155, height=150)
    frames['color'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT)
    frames['input'].pack(fill=BOTH, expand=True, anchor=N, side=RIGHT)
    frames['level'].pack(fill=BOTH, expand=True, anchor=N, side=RIGHT)
    frames['color'].pack_propagate(False)
    frames['level'].pack_propagate(False)
    frames['input'].pack_propagate(False)
    
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

    inFormat = BooleanVar()
    inFormat.set(False)
    I1 = Radiobutton(frames['input'], text="Camera", variable=inFormat, value=True)
    I2 = Radiobutton(frames['input'], text="GUI", variable=inFormat, value=False)
    I1.pack(anchor=W)
    I2.pack(anchor=W)

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
