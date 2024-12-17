from tkinter import *
from tkinter import messagebox
from configure_window import configure_window
from main_loop import game_loop
import json
from PIL import Image, ImageTk

controls = ["w", "a", "s", "d", "b"]
cheat_mode = False

def play(window, screen_width, screen_height, current_user):
    ''' pop up appears asking user if they wish to create a new game
        or load into their previous save, if no previous save the load game
        button will be disabled, then a new game/ saved game loads according
        to the user's choice'''
    
    username = current_user

    # creating the play game popup 
    top = Toplevel(window)
    top.geometry(f"{int(screen_width * 0.45)}x{int(screen_height * 0.25)}")
    top.title("Play Game")

    # position the window
    top.geometry(f"+{int(screen_width * 0.27)}+{int(screen_height * 0.3)}")

    # reads json file
    with open("userdetails.json", "r", encoding = "utf-8") as f:
        user_details = json.load(f)

    # gets the saved level from user details
    user_level = 1
    for user in user_details["players"]:
        if user["username"] == current_user:
            user_level = user["level"]
    

    # text informing the user
    # notifies that saved game will be deleted if they start a new one
    text = Label(top,
                 text = """Choose whether you would like to start a new game or load a saved game \n
                 WARNING: If you choose a new game the saved game will be deleted""",
                 font = ("Impact", 20),
                 pady = 10)
    text.pack()
    
    # frame to contain the two button 
    frame = Frame(top,
                  bg = "purple",
                  width = 20,
                  height = 40,)
    frame.pack(pady = 5)

    # create new game button
    new_game_button = Button(frame,
                             text = "N e w   G a m e",
                             font = ("Impact", 20),
                             height = 2,
                             width = 20,
                             bd = 5,
                             relief = RIDGE,
                            command = lambda: game_loop(window, 1, username, controls, cheat_mode))
    new_game_button.grid(row = 0, column = 0)

    # load game button
    load_game_button = Button(frame,
                             text = "L o a d   G a m e",
                             font = ("Impact", 20),
                             height = 2,
                             width = 20,
                             bd = 5,
                             relief = RIDGE,
                            command = lambda: game_loop(window, user_level, username, controls, cheat_mode))
    load_game_button.grid(row = 0, column = 1)


    if user_level == 1:
        load_game_button.configure(state = DISABLED)



def leaderboard(window, screen_width, screen_height):
    ''' opens pop up showcasing the 10 users with the highest scores '''

    # creating the leaderboard pop up 
    top = Toplevel(window)
    top.geometry(f"{int(screen_width * 0.3)}x{int(screen_height * 0.65)}")
    top.title("Leaderboards")

    # position the leaderboard 
    top.geometry(f"+{int(screen_width * 0.35)}+{int(screen_height * 0.15)}")

    # read json file
    with open("userdetails.json", "r", encoding = "utf-8") as f:
        user_details = json.load(f)

    # collect all highscores in json file
    high_scores = []
    for user in user_details["players"]:
        high_scores.append([user["username"], user["high-score"]])
        


    def sort_high_score(user):
        ''' Function to be taken as an argument for sort 
            each user in the list is within its own list 
            with the username then high score, [[user1, 1], [user2, 2]]'''
        return user[1]

    # sort all high scores, highest score at inddex 0
    high_scores.sort(reverse = True, key = sort_high_score)

    # remove scores not in the top 10
    temp = high_scores
    high_scores = []
    for i in temp:
        if temp.index(i) < 10:
            high_scores.append(i)
        else:
            break

    # display the top 10 highscores and the corresponding username
    # for each high score create a label containing the username and the highscore

    for i in high_scores:
        username = i[0]
        for char in username:
            username = username.replace(char, f"{char} ")

        high_score = i[1]

        label = Label(top,
                      text = f"{username}:                        {high_score}",
                      font = ("Impact", 30),
                      pady = 10,
                      width = 100,
                      bd = 5,
                      fg = "white",
                      bg = "#141314",
                      relief = RIDGE)
        label.pack()


def settings(window, screen_width, screen_height):
    ''' showcases popup allowing user to change movement controls '''

    # creating the settings pop up 
    top = Toplevel(window)
    top.geometry(f"{int(screen_width * 0.5)}x{int(screen_height * 0.5)}")
    top.title("Settings")
    top.configure(bg = "#141314")

    # position the settings 
    top.geometry(f"+{int(screen_width * 0.35)}+{int(screen_height * 0.35)}")

    # creating frame to contain controls
    frame = Frame(top,
                  bg = "#141314",
                  width = int(screen_width * 0.50),
                  height = int(screen_height * 0.70))
    frame.pack(pady = 20)

    # move up control
    move_up_entry = Entry(frame,
                          text = f"{controls[0]}",
                          font = ("Impact", 20),
                          width = 10,
                          bd = 5,
                          relief = RIDGE)
    move_up_entry.grid(row = 0, column = 1)
    move_up_entry.insert(0, controls[0])

    # move up label
    move_up_label = Label(frame,
                          text = "M o v e  U p  ",
                          font = ("Impact", 20),
                          width = 15,
                          padx = 10,
                          fg = "white",
                          bg = "#141314",
                          anchor = W)
    move_up_label.grid(row = 0, column = 0)

    # move left control
    move_left_entry = Entry(frame,
                            font = ("Impact", 20),
                            width = 10,
                            bd = 5,
                            relief = RIDGE)
    move_left_entry.grid(row = 1, column = 1)
    move_left_entry.insert(0, controls[1])

    # move left label
    move_left_label = Label(frame,
                          text = "M o v e  L e f t  ",
                          font = ("Impact", 20),
                          width = 15,
                          padx = 10,
                          bg = "#141314",
                          fg = "white",
                          anchor = W)
    move_left_label.grid(row = 1, column = 0)

    # move down control
    move_down_entry = Entry(frame,
                          font = ("Impact", 20),
                          width = 10,
                          bd = 5,
                          relief = RIDGE)
    move_down_entry.grid(row = 2, column = 1)
    move_down_entry.insert(0, controls[2])

    # move down label
    move_down_label = Label(frame,
                          text = "M o v e  D o w n  ",
                          font = ("Impact", 20),
                          width = 15,
                          padx = 10,
                          bg = "#141314",
                          fg = "white",
                          anchor = W)
    move_down_label.grid(row = 2, column = 0)

    # move right control
    move_right_entry = Entry(frame,
                          font = ("Impact", 20),
                          width = 10,
                          bd = 5,
                          relief = RIDGE)
    move_right_entry.grid(row = 3, column = 1)
    move_right_entry.insert(0, controls[3])

    # move right label
    move_right_label = Label(frame,
                          text = "M o v e  Right  ",
                          font = ("Impact", 20),
                          width = 15,
                          padx = 10,
                          bg = "#141314",
                          fg = "white",
                          anchor = W)
    move_right_label.grid(row = 3, column = 0)

    # boss key control 
    boss_key_entry = Entry(frame,
                          font = ("Impact", 20),
                          width = 10,
                          bd = 5,
                          relief = RIDGE)
    boss_key_entry.grid(row = 4, column = 1)
    boss_key_entry.insert(0, controls[4])

    # boss key label
    boss_key_label = Label(frame,
                          text = "B o s s  K e y  ",
                          font = ("Impact", 20),
                          width = 15,
                          padx = 10,
                          bg = "#141314",
                          fg = "white",
                          anchor = W)
    boss_key_label.grid(row = 4, column = 0)


    def cheat_code():
        ''' enables cheat mode if correct cheat code in entry box
            changes appearence of button to show it is enabled 
            if all ready activated it will deactivate'''
        
        global cheat_mode

        # disbable cheat mode
        if cheat_mode is True:
            cheat_mode = False

            # change button to show it is disabled
            enable_button.configure(text = "E n a b l e")
            enable_button.configure(bg = "white")
            return

        # check if code is correct
        if cheat_entry.get() == "lotsandlotsofbullets":
            cheat_mode = True

            # change button to show cheat code is enabled
            enable_button.configure(text = "E n a b l e d")
            enable_button.configure(bg = "grey")


    # frame containing elements related to cheat code
    cheat_frame = Frame(top,
                        width = int(screen_width * 0.50),
                        height = int(screen_height * 0.70),
                        bg = "#141314")
    cheat_frame.pack(side = BOTTOM, pady = 20)

    # label containing text "Enter Cheat Code"
    cheat_label = Label(cheat_frame,
                        font = ("Impact", 20),
                        bg = "#141314",
                        fg = "white",
                        text = "E n t e r  C h e a t  C o d e : ")
    cheat_label.grid(row = 0, column = 0)

    # entry box to type cheat code
    cheat_entry = Entry(cheat_frame,
                        font = ("Impact", 20),
                        bd = 5,
                        relief = RIDGE)
    cheat_entry.grid(row = 1, column = 0)

    # enable cheat code button
    enable_button = Button(cheat_frame,
                           font = ("Impact", 20),
                           text = "E n a b l e",
                           command = cheat_code)
    enable_button.grid(row = 1, column = 1)



    letters = [ 'a', 'b', 'c', 'd', 'e', 'f',
                'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x',
                'y', 'z']

    def save():
        ''' saves the settings in the entry boxes '''

        global controls 

        # create list of all entry boxes
        entry_boxes = [move_up_entry, move_left_entry, move_down_entry, move_right_entry, boss_key_entry]

        characters = []

        for entry_box in entry_boxes:
            # check if empty or not a letter
            if entry_box.get() not in letters:
                messagebox.showerror(title = "error",
                                     message = "ensure valid characters in entry boxes")
                return
            
            # check for duplictes
            if entry_box.get() in characters:
                messagebox.showerror(title = "error",
                                     message = "ensure there are no duplicates")
                return
            
            else:
                characters.append(entry_box.get()) 
        
        controls = characters
        
    # save button
    save_button = Button(frame,
                         text = "save",
                         font = ("Impact", 20),
                         command = save,
                         padx = 10)
    save_button.grid(row = 5, column = 1)



def configure_main_menu(current_user):
    ''' adds elements to the main menu screen '''
    
    window = Tk()


    # creates main menu screen window and gets the dimensions of the user's screen
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
    canvas.create_text(int(screen_width / 2), int(screen_height / 2.6), text = "B I G   S P I D E R ",
                       fill = "black", font = ("Impact", 100))


    # creating frame to store buttons for the main menu
    menu_frame = Frame(window,
                       bg = "#141314",
                       width = 20,
                       height = 40)
    menu_frame.place(relx = 0.35, rely = 0.45)
    

    # play game button
    play_button = Button(menu_frame,
                         text = "P l a y",
                         font = ("Impact", 20),
                         height = 2,
                         width = 40,
                         bd = 5,
                         relief = RIDGE,
                         command = lambda: play(window, screen_width, screen_height, current_user))
    play_button.pack(padx = 20, pady = 20)


    # leaderboard button 
    leaderboard_button = Button(menu_frame,
                         text = "L e a d e r b o a r d",
                         font = ("Impact", 20),
                         height = 2,
                         width = 40,
                         bd = 5,
                         relief = RIDGE,
                         command = lambda: leaderboard(window, screen_width, screen_height))
    leaderboard_button.pack(padx = 20, pady = 20)


    # settings button 
    settings_button = Button(menu_frame,
                         text = "S e t t i n g s",
                         font = ("Impact", 20),
                         height = 2,
                         width = 40,
                         bd = 5,
                         relief = RIDGE,
                         command = lambda: settings(window, screen_width, screen_height))
    settings_button.pack(padx = 20, pady = 20)


    # quit button 
    quit_button = Button(menu_frame,
                         text = "Q u i t",
                         font = ("Impact", 20),
                         height = 2,
                         width = 40,
                         bd = 5,
                         relief = RIDGE,
                         command = quit)
    quit_button.pack(padx = 20, pady = 20)


    window.mainloop()

