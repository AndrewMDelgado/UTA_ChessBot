#from tkinter import *
#import tkinter
from tkinter import Tk, ttk, LEFT, RIGHT, BOTTOM, TOP, BOTH, N, S, E, W, NW
import tkinter.messagebox as msgbox




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
    winMain.resizable(False, False)
    
    frames = {}
    notebook = ttk.Notebook(winMain)
    frames['main_tab'] = ttk.Frame(notebook)
    frames['misc_tab'] = ttk.Frame(notebook)
    notebook.add(frames['main_tab'], text='Main Rules')
    notebook.add(frames['misc_tab'], text='Misc Rules')
    #frames['color_tab'] = ttk.Frame(notebook)
    #frames['level_tab'] = ttk.Frame(notebook)
    #frames['misc_tab'] = ttk.Frame(notebook)
    #notebook.add(frames['color_tab'], text='Player color')
    #notebook.add(frames['level_tab'], text='AI level')
    #notebook.add(frames['misc_tab'], text='Other options')
    #notebook.pack()
    
    frames['color'] = ttk.LabelFrame(frames['main_tab'], text='Player Color', labelanchor=NW, width = 200, height = 200)
    frames['level'] = ttk.LabelFrame(frames['main_tab'], text='AI Level', labelanchor=NW, width = 200, height = 200)
    frames['misc'] = ttk.LabelFrame(frames['misc_tab'], text='Misc. Rules', labelanchor=NW, width = 200, height = 200)
    #frames['color'].pack(side = LEFT)
    #frames['level'].pack(side = RIGHT)
    #frames['misc'].pack(side = BOTTOM)

    frames['color'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT)
    frames['level'].pack(fill=BOTH, expand=True, anchor=N, side=RIGHT)
    frames['misc'].pack(fill=BOTH, expand=True, anchor=N, side=BOTTOM)
    notebook.pack()

    winMain.mainloop()

if __name__ == '__main__':
    guiMain()
    #getPlayerMove()