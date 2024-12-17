''' File holds the configure window function '''

from tkinter import *

def configure_window(window):
    ''' configures the winow, (defualt template for window)
        additionally this function returns the height and width
        of the users screen, this is to help with positioning elements '''

    # get dimensions of user's screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # set size of window to screen size
    # window size cannot be changed 
    window.geometry(f"{screen_width}x{screen_height}")
    window.maxsize(screen_width, screen_height)
    window.minsize(screen_width, screen_height)

    # window opens at fullscreen
    window.attributes("-fullscreen", True)

    # title of the game
    window.title("Big Spider")

    return screen_height, screen_width

