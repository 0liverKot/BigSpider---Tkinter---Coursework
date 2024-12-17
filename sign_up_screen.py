''' Contains the signup page for the game '''

from tkinter import *
from tkinter import messagebox
from configure_window import configure_window
from main_menu_screen import configure_main_menu
import json
from PIL import Image, ImageTk


def signup(window, username, password):
    ''' checks if details are already in json file, 
        if already present error pops up
        if not the details are added to the file and the user is logged in '''

    user_unique = False

        # checks for empty username 
    if username == "":
        messagebox.showerror(title = "error",
                             message = "enter a username")
        return

    # reads json file
    with open("userdetails.json", "r", encoding = "utf-8") as f:
        user_details = json.load(f)

    # checks if username is unique
    for user in user_details["players"]:
        if user["username"] == username:
            
            # error appears telling user account is already created 
            messagebox.showerror(title = "Error",
                                 message = "This Account Already Exists")
            return
        else:
            user_unique = True
        
    # details are unique at this point 
    if user_unique is True:
        
        # add the unique details to json file
        new_details = {"username": username, "password": password, "high-score": 1, "level": 1}
        players = user_details["players"]
        players.append(new_details)

        with open("userdetails.json", "w", encoding = "utf-8") as f:
            json.dump(user_details, f, indent = 4)

        # close current window and open main menu
        window.destroy()
        configure_main_menu(username)

    # entry is created
def configure_sign_up_screen():
    ''' Adds elements to the sign up screen '''

    window = Tk()

    # creates sign up screen window and get dimensions of user's screen
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


    # creating frame to contain, username, password and sign in button
    details_frame = Frame(window,
                        bg = "#141314",
                        width = 20,
                        height = 40)
    details_frame.place(relx = 0.27, rely = 0.50)
    
    
    # creating the label and entry for username
    username_label = Label(details_frame,
                           text = "Enter a username:",
                           bg = "#141314",
                           fg = "white",
                           font = ("Impact", 15),
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
                           text = "Enter a NOT USED IRL password:",
                           bg = "#141314",
                           fg = "white",
                           font = ("Impact", 15),
                           )
    password_label.grid(row = 1, column = 0, pady = 20, padx = 10)

    password_entry = Entry(details_frame,
                           font = ("Impact", 20),
                           width = 40,
                           bd = 5,
                           relief = RIDGE,
                           show = "*"
                           )
    password_entry.grid(row = 1, column = 1, pady = 20, padx = 10)


    # creating button and button for signing up 
    sign_up_button =  Button(window,
                           text = "S i g n   U p",
                           font = ("Impact", 20),
                           height = 1,
                           width = 50,
                           bd = 5,
                           relief = RIDGE,
                           command = lambda: signup(window,
                                                    username_entry.get().strip(" "),
                                                    password_entry.get().strip(" "),))
    sign_up_button.place(relx = 0.33, rely = 0.67)

    window.mainloop()