''' File loads the opening screen for the game
    Run this file to play '''

from tkinter import *
from sign_up_screen import configure_sign_up_screen
from login_screen import configure_login_screen
from configure_window import configure_window
from PIL import Image, ImageTk

def login(window):
    ''' Login with an existing account '''

    window.destroy()
    configure_login_screen()

def sign_up(window):
    ''' Taken to a new window to create an account '''
    window.destroy()
    configure_sign_up_screen()


def configure_opening_screen():
    ''' adds elements to the opening screen '''

    window = Tk()

    # configure window and get dimensions of the user's screen
    screen_dimensions = configure_window(window)
    screen_height = screen_dimensions[0]
    screen_width = screen_dimensions[1]

    # create canvas
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

    # add title text
    canvas.create_text(int(screen_width / 2), int(screen_height / 2.3), text = "B I G   S P I D E R ",
                       fill = "black", font = ("Impact", 100))
    

    # creating frame for menu
    menu_frame = Frame(window,
                       bg = "#141314",
                       width = 20,
                       height = 40)
    menu_frame.place(relx = 0.35, rely = 0.50)

    # adding menu buttons to frame
    # buttons will have mainly the same design throughout programme
    # these will be used as a (template)
    login_button = Button(menu_frame,
                          font = ("Impact", 20),
                          text = "L o g i n",
                          height = 3,
                          width = 40,
                          bd = 5,
                          relief = RIDGE,
                          command = lambda: login(window))
    login_button.pack(padx = 20, pady = 20)

    sign_up_button = Button(menu_frame,
                            text = "S i g n   U p",
                            font = ("Impact", 20),
                            height = 3,
                            width = 40,
                            bd = 5,
                            relief = RIDGE,
                            command = lambda: sign_up(window))                        
    sign_up_button.pack(padx = 20, pady = 20)

    quit_button = Button(menu_frame,
                         text = "Q u i t",
                         font = ("Impact", 20),
                         height = 3,
                         width = 40,
                         bd = 5,
                         relief = RIDGE,
                         command = quit)
    quit_button.pack(padx = 20, pady = 20)

    window.mainloop()
                                                                                                                              
configure_opening_screen()

