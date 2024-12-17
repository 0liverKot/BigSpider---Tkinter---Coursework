from tkinter import *
from configure_window import configure_window
from PIL import Image, ImageTk


def end_game(window, reason):
    ''' end game screen, says whether game ended due to quitting or dieing '''
    
    # destroys previous window and creates new window 
    window.destroy()
    window = Tk()

    # configure the window and gets user's screen dimensions
    screen_dimentsions = configure_window(window)
    screen_height = screen_dimentsions[0]
    screen_width = screen_dimentsions[1]

    canvas = Canvas(window,
                    width = screen_width,
                    height = screen_height)
    canvas.pack()

    # loading file for background
    with Image.open("blood_splatter.png") as img:

        # resizing the background
        img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

        # convert image back into appropriate type
        background = ImageTk.PhotoImage(img)

    # add background to canvas
    canvas.create_image(int(screen_width / 2), int(screen_height / 2), image = background)

    # add game over text
    canvas.create_text(int(screen_width / 2), int(screen_height / 2.3), text = "G A M E   O V E R",
                       fill = "black", font = ("Impact", 100))
    
    # text stating reason for game loss
    canvas.create_text(int(screen_width / 2), int(screen_height / 1.8), text = reason,
                       fill = "black", font = ("Impact", 40))

    # button to return to main menu
    button = Button(window,
                    text = "E x i t",
                    font = ("Impact", 20),
                    height = 2,
                    width = 20,
                    bd = 5,
                    relief = RIDGE,
                    command = exit)
    button.place(relx = 0.42, rely = 0.6)

    window.mainloop()