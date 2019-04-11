#from tkinter import *
from tkinter import Tk, ttk
import tkinter.messagebox as msgbox




def alertPlayer(msgType, msg):
    msgbox.showinfo(msgType, msg)

def dispAIMove(moveStr):
    msg = moveStr[:2] + ' to ' + moveStr[2:]
    msgbox.showinfo("AI Move", msg)

def getPlayerMove():
    window = Tk()
    window.wm_title("Player Move")
    window.mainloop()


def guiMain():
    winMain = Tk()
    winMain.wm_title("UTA Chess Bot")
    
    frames = {}
    notebook = ttk.Notebook(winMain)
    frames['color_tab'] = ttk.Frame(notebook)
    frames['level_tab'] = ttk.Frame(notebook)
    frames['misc_tab'] = ttk.Frame(notebook)
    notebook.add(frames['color_tab'], text='Player color')
    notebook.add(frames['level_tab'], text='AI level')
    notebook.add(frames['misc_tab'], text='Other options')

    
    
    

    winMain.mainloop()

if __name__ == '__main__':
    #guiMain()
    getPlayerMove()