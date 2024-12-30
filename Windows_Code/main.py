from tkinter import Tk
from ui import LinOLS

if __name__ == "__main__":
    window = Tk(className='LinOLS')
    app = LinOLS(window)
    window.mainloop()