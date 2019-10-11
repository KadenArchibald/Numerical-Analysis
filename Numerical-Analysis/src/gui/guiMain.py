'''
Kaden Archibald

Created: Aug 10, 2019
Revised: 
Version: IPython 7.2.0 (Anaconda distribution) with Python 3.7.1

Desktop Application Driver
'''

import threading
import traceback

from Application import Application


def main():
    
    exitCode = 0
    
    try:
        app = Application()
        app.start()

    except Exception as error:
        exitCode = -1
        
        print('Exception: ' + str(error))
        traceback.print_exc()
        
        if app.root.state() == 'normal':
            app.root.destroy()

    finally:
        pass
        
    
    return exitCode



if __name__ == '__main__':
    main()
    




from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def demo():
    root = tk.Tk()
    root.title("ttk.Notebook")

    nb = ttk.Notebook(root)

    # adding Frames as pages for the ttk.Notebook 
    # first page, which would get widgets gridded into it
    page1 = ttk.Frame(nb)

    # second page
    page2 = ttk.Frame(nb)
    text = ScrolledText(page2)
    text.pack(expand=1, fill="both")

    nb.add(page1, text='One')
    nb.add(page2, text='Two')

    nb.pack(expand=1, fill="both")

    root.mainloop()


