''' Contains the login page for the game '''

from tkinter import *
from tkinter import messagebox
from configure_window import configure_window
import json
from main_menu_screen import configure_main_menu
from PIL import Image, ImageTk

def login(window, username, password):
    ''' checks if account details given match with what is stored 
        if details match user is taken to the main menu '''

    # checks for empty username 
    if username == "":
        messagebox.showerror(title = "error",
                             message = "enter a username")
        return
        

    # reads json file
    with open("userdetails.json", "r", encoding = "utf-8") as f:
        user_details = json.load(f)
   

    # checks if username and password given match the details that are stored
    correct_details = False
    for user in user_details["players"]:
        if user["username"] == username and user["password"] == password:
            correct_details = True


    # close current window and open the main menu
    if correct_details is True:
        window.destroy()
        configure_main_menu(username)
    # if details incorrect error is shown
    else:
        messagebox.showerror(title = "error",
                             message = "Incorrect details entered")
        

    # entry is created
def configure_login_screen():
    ''' Adds elements to the login screen '''

    window = Tk()

    # creates login screen window and get dimensions of user's screen
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

    # add title text
    canvas.create_text(int(screen_width / 2), int(screen_height / 2.3), text = "B I G   S P I D E R ",
                       fill = "black", font = ("Impact", 100))


    # creating frame to contain, username, password and login button
    details_frame = Frame(window,
                        bg = "#141314",
                        width = 20,
                        height = 40)
    details_frame.place(relx = 0.27, rely = 0.5)
    
    
    # creating the label and entry for username
    username_label = Label(details_frame,
                           text = "Enter your username:",
                           font = ("Impact", 15),
                           bg = "#141314",
                           fg = "white"
                           )
    username_label.grid(row = 0, column = 0, sticky = "w", pady = 20, padx = 10)

    username_entry = Entry(details_frame,
                           font = ("Impact", 20),
                           width = 40,
                           bd = 5,
                           relief = RIDGE,
                           )
    username_entry.grid(row = 0, column = 1, pady = 20, padx = 10)


    # creating the label and entry for password
    password_label = Label(details_frame,
                           text = "Enter your NOT USED IRL password:",
                           font = ("Impact", 15),
                           bg = "#141314",
                           fg = "white"
                           )
    password_label.grid(row = 1, column = 0, pady = 20, padx = 10)

    password_entry = Entry(details_frame,
                           font = ("Impact", 20),
                           width = 40,
                           bd = 5,
                           relief = RIDGE,
                           show = "*")
    password_entry.grid(row = 1, column = 1, pady = 20, padx = 10)


    # creating button and button for logging in 
    login_button =  Button(window,
                           text = "L o g i n",
                           font = ("Impact", 20),
                           height = 1,
                           width = 50,
                           bd = 5,
                           relief = RIDGE,
                           command = lambda: login(window,
                                                   username_entry.get().strip(" "),
                                                   password_entry.get().strip(" "),))
    login_button.place(relx = 0.33, rely = 0.67)

    window.mainloop()

