from tkinter import *
from PIL import Image, ImageTk
from end_game import end_game
from configure_window import configure_window
import math
import time
import json
import webbrowser

# initialising global variables
paused = False
character_movement_override = False
counter = 0
counter_since_shot = 0
character_health_bar = None
character_health_bar_background = None
character_health = 100
spider_health_bar = None
spider_health_bar_background = None
spider_health = 1000
user_level = None



def game_loop(window, level, username, controls, cheat_mode):
    ''' the main game loop all contained within this function '''

    global user_level
    global paused
    global counter

    user_level = level

    def pause_menu():
        ''' allows the user to quit and save the game
            or to simply take a break since the game will stop '''

        # changing global variable paused
        global paused
        paused = True

        def close():
            ''' closes the menu allowing the game to unpause '''
            global paused
            paused = False
            top.destroy()

        def save():
            ''' saves current level to json file, able to then load to that level '''
    
            # reads json file
            with open("userdetails.json", "r", encoding = "utf-8") as f:
                user_details = json.load(f)

                # get the correct user
                for user in user_details["players"]:
                    if user["username"] == username:

                        user["level"] = user_level

                        # write the level to json file
                        with open("userdetails.json", "w", encoding = "utf-8") as f:
                            json.dump(user_details, f, indent = 4)



        # creating the pause menu pop up 
        top = Toplevel()
        top.geometry(f"{int(screen_width * 0.2)}x{int(screen_height * 0.3)}")
        top.title("Paused")
        top.configure(bg = "black") 


        #create the frame to hold the buttons
        frame = Frame(top,
                      bg = "#141314")
        frame.pack()

        # creating the close button 
        close_menu_button = Button(frame,
                              font = ("Impact", 20),
                              text = "C l o s e   M e n u",
                              height = 2,
                              width = 20,
                              bg = "#141314",
                              fg = "white",
                              bd = 5,
                              relief = RIDGE,
                              command = close)
        close_menu_button.grid(row = 0, column = 0)

        save_game_button = Button(frame,
                             text = "S a v e   G a m e",
                             font = ("Impact", 20),
                             height = 2,
                             width = 20,
                             bg = "#141314",
                             fg = "white",
                             bd = 5,
                             relief = RIDGE,
                            command = save)
        save_game_button.grid(row = 1, column = 0)


        quit_game_button = Button(frame,
                             text = "Q u i t   G a m e",
                             font = ("Impact", 20),
                             height = 2,
                             width = 20,
                             bg = "#141314",
                             fg = "white",
                             bd = 5,
                             relief = RIDGE,
                            command = lambda: end_game(window, "Y o u   Q u i t"))
        quit_game_button.grid(row = 2, column = 0)

        # handles closing the window with the x button 
        top.protocol("WM_DELETE_WINDOW", close)  

    # destroy previous window and create new window 
    window.destroy()
    window = Tk()

    # configures window for the game and gets the user's screen dimensions
    screen_dimensions = configure_window(window)
    screen_height = screen_dimensions[0]
    screen_width = screen_dimensions[1]
    window.focus_force()

    # add canvas 
    canvas = Canvas(window,
                    width = screen_width,
                    height = screen_height)
    canvas.pack()


    # loading file for background 
    with Image.open("5025.png") as img:
        
        # resizing the background
        img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

        # convert image into appropriate type 
        background = ImageTk.PhotoImage(img)

    # add background to canvas
    canvas.create_image(int(screen_width / 2), int(screen_height / 2), image = background)


    # creates window for the game and gets the user's screen dimensions
    screen_dimensions = configure_window(window)
    screen_height = screen_dimensions[0]
    screen_width = screen_dimensions[1]
    window.focus_force()

    # creating the round label 
    round_label = Label(window, 
                        font = ("Impact", 60),
                        text = user_level,
                        width = 2,
                        bg = "#141314",
                        fg = "#9c2a2a")
    round_label.place(relx = 0.49)

    # creating pause button
    pause_button = Button(canvas,
                          font = ("Impact", 20),
                          text = "=",
                          height = 1,
                          bg = "#141314",
                          fg = "white",
                          width = 5,
                          command = pause_menu)
    pause_button.place(x = 20, y = 20)

    # loading the character file
    with Image.open("survivor-move_shotgun_4.png") as char:
        
        # resizing the character
        char = char.resize((100, 100), Image.Resampling.LANCZOS)

        # convert image into appropriate type 
        character = ImageTk.PhotoImage(char)

    # add character to canvas
    character_image = canvas.create_image(200, 200, image = character)


    # loading the file containing spider
    with Image.open("spider.png") as spi:
        
        # resizing the character
        spi = spi.resize((300, 300), Image.Resampling.LANCZOS)

        # convert image into appropriate type 
        spider = ImageTk.PhotoImage(spi)

    # add spider to canvas
    spider_image = canvas.create_image(700, 700, image = spider)


    # stores bullets and their velocities
    # list of dictionaries each containing bullet id, x velocity, y, velocity

    bullets_velocities = []


    def update():
        ''' contains functions that constantly update the game every 1ms '''

        # increment counter
        global counter_since_shot
        global counter

        counter += 1

        # if counter since shot active increment counter
        if counter_since_shot > 0:
            counter_since_shot += 1

        # counter resets after attack takes place
        if counter == 55:
            counter = 1

        def rotation(angle_diff, img):
            ''' rotates the the img by the angle diff, img is either the spider or the character '''

            # if game is paused do nothing if rotating spider
            if paused is True and img == spi:
                return

            # if game is paused and player override not enabled do nothing is rotating character
            if paused is True and character_movement_override is False and img == char:
                return

            # if couunter above 50 spider attacks 
            # attack is animated by a slight rotation
            if counter > 50 and img == spi:
                angle_diff += 30


            # rotate image and convert back to compatible form 
            rotated = img.rotate(angle_diff, resample = Image.Resampling.BICUBIC, expand = True)
            rotated_image = ImageTk.PhotoImage(rotated)

            # Update the label with the rotated image
            if img == spi:
                canvas.itemconfig(spider_image, image = rotated_image)
                canvas.image_1 = rotated_image
            elif img == char:
                canvas.itemconfig(character_image, image = rotated_image)
                canvas.image_2 = rotated_image

            

        def character_movement(event, move_up, move_down, move_left, move_right, boss_key, health, character_x, character_y):
            ''' characters movement is carried out, key pressed is compared to the users character movement settings '''

            global character_health_bar
            global character_health_bar_background
            global paused

            # if game is paused do nothing
            if paused is True and character_movement_override is False:
                return

            # set local variables 
            mov_x = 0
            mov_y = 0

            # get the key that was pressed
            key_pressed = event.keysym

            # boss key pressed
            if key_pressed == boss_key:
                # pause game
                pause_menu()
                # take to video
                url = "https://www.youtube.com/watch?v=rfscVS0vtbw"
                webbrowser.open(url)

            # changes to coordinates are calculated
            if key_pressed == move_up:
                mov_y = -30

            elif key_pressed == move_down:
                mov_y = 30

            elif key_pressed == move_left:
                mov_x = -30
    
            elif key_pressed == move_right:
                mov_x = 30


            # setting screen boundaries

            # setting right boundary
            if character_x > screen_width - 60 and mov_x > 0:
                mov_x = 0

            # setting left boundary
            elif character_x < 80 and mov_x < 0:
                mov_x = 0

            # setting bottom boundary
            if character_y > screen_height - 60 and mov_y > 0:
                mov_y = 0

            # setting top boundary
            elif character_y < 100 and mov_y < 0:
                mov_y = 0

            # image of character moves
            canvas.move(character_image, mov_x, mov_y)
            

            # creating the initial character health bar 
            if character_health_bar is None:
                character_health_bar_background = canvas.create_rectangle(200, 200, 300, 200, fill = "grey", width = 5)
                character_health_bar = canvas.create_rectangle(200, 200, 300, 200, fill = "red")

            # updates position of character health bar 
            canvas.delete(character_health_bar_background)
            character_health_bar_background = canvas.create_rectangle(character_x - 100, character_y - 120, character_x, character_y - 100, fill = "grey", width = 5)

            # scale bar to size to health remaining
            canvas.delete(character_health_bar)
            character_health_bar = canvas.create_rectangle(character_x - 97.5, character_y - 117.5, character_x - 97.5 + health, character_y - 102.5, fill = "red")



        def shoot(character_x, character_y, char_angle):
            ''' creates bullets fired from the charactes '''
            
            global counter_since_shot

            # reset counter, able to shoot again 
            if counter_since_shot > 30:
                counter_since_shot = 0 
            
            # unable to shoot aslong as cheat mode is off
            if counter_since_shot > 0 and cheat_mode is False:
                return

            # if game is paused do nothing
            if paused is True:
                return

            bullet_x = 0
            bullet_y = 0

            def calc_velocities(speed, angle):
                ''' calculate the vertical and horizontal velocities of each bullet '''

                vertical_velocity = 0
                horizontal_velocity = 0

                match angle:
                    # moving down and right
                    case angle if  0 < angle <= 90:

                        # convert to radians
                        angle = (angle / 180) * math.pi

                        vertical_velocity = speed * math.sin(angle)
                        horizontal_velocity = speed * math.cos(angle)

                    # moving down and left 
                    case angle if 90 < angle <= 180:

                        # convert to radians
                        angle = (angle / 180) * math.pi

                        vertical_velocity = speed * math.cos(angle - (math.pi / 2))
                        horizontal_velocity = -(speed * math.sin(angle - (math.pi / 2)))

                    # moving up and right
                    case angle if -90 < angle <= 0:

                        # convert to radians
                        angle = (angle / 180) * math.pi

                        vertical_velocity = -(speed * math.sin(-angle))
                        horizontal_velocity = speed * math.cos(-angle)

                    # moving up and left
                    case angle if -180 < angle <= -90:
                        # convert to radians
                        angle = (angle / 180) * math.pi

                        vertical_velocity = -(speed * math.cos((-angle) - (math.pi / 2)))
                        horizontal_velocity = -(speed * math.sin((-angle) - (math.pi / 2)))

                    case _:
                        vertical_velocity = 0
                        horizontal_velocity = 0

                return horizontal_velocity, vertical_velocity

            # adjust position of where balls spawn based on char_angle
            # so they spawn closer to gun

            if  0 < char_angle <= 90:
                bullet_x = character_x
                bullet_y = character_y + 15

            elif 90 < char_angle <= 180:
                bullet_x = character_x - 60
                bullet_y = character_y

            elif -90 < char_angle <= 0:
                bullet_x = character_x + 30
                bullet_y = character_y - 30

            elif -180 <= char_angle <= -90:
                bullet_x = character_x
                bullet_y = character_y - 45

            bullets = []

            # creating all 5 bullets 
            for _ in range(5):

                # create bullet
                bullet = canvas.create_oval(bullet_x, bullet_y, bullet_x + 10, bullet_y + 10, fill = "black")

                # add bullet to list 
                bullets.append(bullet)
            
            # angle increment adjusts the spread of the bullet, bullet 1 -30 from bullet 3 (center) 
            angle_increment = -30
            speed = 10
            
            for bullet in bullets:


                # add the angle increment to the angle between character and mouse, then increase the increment
                angle = char_angle + angle_increment
                angle_increment += 15

                # ensures that angles are within the range of -180 and 180
                if angle >= 180: 
                    angle -= 360
                elif angle <= -180:
                    angle += 360


                # calculate the velocities
                horizontal_velocity, vertical_velocity = calc_velocities(speed, angle)

                # add dictionary to the list of dictionaries
                bullets_velocities.append({"bullet_id": bullet, "x_velocity": horizontal_velocity, "y_velocity": vertical_velocity})

            # beginning counter since shot 
            counter_since_shot = 1


        def bullet_move():
            ''' every time the window updates the bullet locations are updates and they move 
                according to their velocities stored in bullet_velocities'''
            
            # if game is paused do nothing
            if paused is True:
                return

            for info in bullets_velocities:

                # retrieving variables from dictionary
                bullet = info["bullet_id"]
                horizontal_velocity = info["x_velocity"]
                vertical_velocity = info["y_velocity"]

                # move the bullet 
                canvas.move(bullet, horizontal_velocity, vertical_velocity)


        def spider_movement(x_diff, y_diff, spider_x, spider_y, max_health):
            ''' movement of spider follows the user at all times '''

            global spider_health_bar
            global spider_health_bar_background

            # if game is paused do nothing
            if paused is True:
                return

            # defining initial variables 
            mov_x = 0
            mov_y = 0

            # if spider to right of character spider moves left 
            if x_diff > 100: 
                mov_x = -5

            # if spider to left of character spider moves right 
            elif x_diff < -100:
                mov_x = 5

            # if spider below character spider moves up
            if y_diff > 100:
                mov_y = -5
            
            # if spider above character spider moves down
            elif y_diff < -100:
                mov_y = 5


            if mov_x > 0 and mov_y > 0:
                # ratio between x and y (if y is far greater the spider will travel less x for smoother motion)
                x_y_ratio = x_diff / y_diff

                # convert ratio to positive
                if x_y_ratio < 0:
                    x_y_ratio = x_y_ratio * -1

                # if x_diff greater than y_diff, mov_y decreases
                if x_y_ratio > 1:
                    mov_y = mov_y / x_y_ratio
                
                # if y_diff greater than x_diff, mov_x decreases
                if x_y_ratio < 1:
                    mov_x = mov_x * x_y_ratio

            # move the spider image
            canvas.move(spider_image, mov_x, mov_y)

            # new position of the spider
            spider_x = spider_x + mov_x
            spider_y = spider_y + mov_y

            # creates initial spider health bar
            if spider_health_bar is None:
                spider_health_bar_background = canvas.create_rectangle(700, 700, 1000, 700, fill = "grey", width = 5)
                spider_health_bar = canvas.create_rectangle(700, 700, 1000, 700, fill = "red")

            # update position of spider health bar
            canvas.delete(spider_health_bar_background)
            spider_health_bar_background = canvas.create_rectangle(spider_x - 250, spider_y - 300, spider_x + 50, spider_y - 280, fill = "grey", width = 5)


            # scale bar to size to health remaining
            increment = (spider_health / max_health) * 300
            canvas.delete(spider_health_bar)
            spider_health_bar = canvas.create_rectangle(spider_x - 247.5, spider_y - 297.5, spider_x - 247.5 + increment, spider_y - 282.5, fill = "red")


        def check_spider_hit():
            ''' checks if a bullet is within the spiders hitbox or outside window
                if bullet in hitbox bullet disappears and spider loses health '''
            
            global spider_health

            # damage is dependant on round
            damage = 50 - user_level + 1

            # minimum damage is 1
            if damage < 1:
                damage = 1

            # setting boundaries of hitbox
            left_hitbox = spider_x - 75
            right_hitbox = spider_x + 75
            top_hitbox = spider_y - 75
            bottom_hitbox = spider_y + 75
            
            for info in bullets_velocities:
                
                # get coordinates of bullet
                bullet_coordinates = canvas.coords(info["bullet_id"])

                # get the coordinates of the centre of the bullet
                bullet_x = (bullet_coordinates[0] + bullet_coordinates[2]) / 2
                bullet_y = (bullet_coordinates[1] + bullet_coordinates[3]) / 2

                # if bullet within hitbox
                if left_hitbox < bullet_x < right_hitbox and top_hitbox < bullet_y < bottom_hitbox:

                    # spider takes damage
                    spider_health = spider_health - damage 

                    # bullet removed 
                    # get bullet
                    bullet = info["bullet_id"]

                    # remove from bullet_velocities
                    bullets_velocities.remove(info)

                    # remove from canvas
                    canvas.delete(bullet)

                # if bullet outside window
                if screen_width < bullet_x < 0 and screen_height < bullet_y < 0: 

                    # bullet removed 
                    # get bullet
                    bullet = info["bullet_id"]

                    # remove from bullet_velocities
                    bullets_velocities.remove(info)

                    # remove from canvas
                    canvas.delete(bullet)


        def spider_dead(max_health):
            ''' checks if the spider has over 0 health left 
                if health below 0 game pauses, health increases and user_level increases '''
            
            global paused
            global spider_health_bar
            global spider_health
            global character_movement_override
            global user_level


            # if spider has health remaining do nothing
            if spider_health > 0:
                return
            
            paused = True

            # allows the chaarcter to move and rotate despite everthing else being paused
            character_movement_override = True

            increment = 5

            while spider_health != max_health:
                spider_health += 10
                canvas.delete(spider_health_bar)

                # when bar fully fills spider is at max health
                if increment > 300:
                    increment = 300
                    spider_health = max_health

                # update the health bar with added health
                spider_health_bar = canvas.create_rectangle(spider_x - 247.5, spider_y - 297.5, spider_x - 247.5 + increment, spider_y - 282.5, fill = "red")
                window.update()
                increment += 5

                # add delay when health bar being filled
                time.sleep(0.1)

            # user_level increase
            user_level += 1

            # increase round counter
            round_label.configure(text = user_level)


            # check if update high score required 
            # reads json file
            with open("userdetails.json", "r", encoding = "utf-8") as f:
                user_details = json.load(f)

                # get the correct user
                for user in user_details["players"]:
                    if user["username"] == username:

                        # get highscore and compare to current level
                        high_score = user["high-score"]
                        if user_level > high_score:

                            user["high-score"] = user_level
                        
                            # add the new high score to json file
                            with open("userdetails.json", 'w', encoding = "utf-8") as f:
                                json.dump(user_details, f, indent=4)

            # game unpauses
            paused = False
            character_movement_override = False

        def check_character_hit(character_x, character_y):
            ''' when spider attacks checks if character within spiders range
                if in range character takes damage
                if health below zero end game '''
            
            global character_health
            global character_health_bar
            global character_health_bar_background

            # if not on spider attack do nothing
            if counter != 54:
                return

            # damage is dependant on round
            damage = 10 + user_level - 1

            # maximum damage is 100
            if damage > 100:
                damage = 100

            # setting range of spider's attack
            left_range = spider_x - 200
            right_range = spider_x + 200
            top_range = spider_y - 200
            bottom_range = spider_y + 200

            # character in range of spider's attack
            if left_range < character_x < right_range and top_range < character_y < bottom_range:

                # character takes damage
                character_health -= damage

                # updates position of character health bar 
                canvas.delete(character_health_bar_background)
                character_health_bar_background = canvas.create_rectangle(character_x - 100, character_y - 120, character_x, character_y - 100, fill = "grey", width = 5)

                # updates health bar filling
                canvas.delete(character_health_bar)
                character_health_bar = canvas.create_rectangle(character_x - 97.5, character_y - 117.5, character_x - 97.5 + character_health, character_y - 102.5, fill = "red")
            if character_health <= 0:
                time.sleep(1)
                end_game(window, "Y o u   D i e d") 


        # position of character
        character_coordinates = canvas.coords(character_image)
        character_x = character_coordinates[0]
        character_y = character_coordinates[1]

        # position of spider
        spider_coordinates = canvas.coords(spider_image)
        spider_x = spider_coordinates[0]
        spider_y = spider_coordinates[1]

        # location of mouse
        mouse_x = window.winfo_pointerx() - window.winfo_rootx()
        mouse_y = window.winfo_pointery() - window.winfo_rooty()

        # calculate vertical and horizontal diff between character and mouse
        initial_char_angle = 0
        diff_x = mouse_x - character_x
        diff_y = mouse_y - character_y

        # incase of division by zero 
        if diff_x == 0:
            diff_x = 1
        
        # get angle between character and mouse
        char_angle = math.atan((diff_y/diff_x))

        # convert to degrees
        char_angle = (char_angle * 180) /  math.pi

        if diff_x < 0 and diff_y < 0:
            char_angle = char_angle - 180

        elif diff_x < 0:
            char_angle = 180 + char_angle 

        # apply the angle
        char_angle_diff = initial_char_angle - char_angle
        rotation(char_angle_diff, char)


        # calculate difference in position between spider and character
        initial_spider_angle = 0 
        x_diff = spider_x - character_x
        y_diff = spider_y - character_y

        # incase of division by zero 
        if x_diff == 0:
            x_diff = 1
        
        # get angle between spider and character
        spider_angle = math.atan((y_diff / x_diff))

        # convert to degrees
        spider_angle = (spider_angle * 180) /  math.pi

        if x_diff < 0 and y_diff < 0:
            spider_angle = spider_angle - 180

        elif x_diff < 0:
            spider_angle = 180 + spider_angle 

        # apply the angle
        spider_angle_diff = initial_spider_angle - spider_angle
        spider_angle_diff = spider_angle_diff + 190
        rotation(spider_angle_diff, spi)
            
        # binding controls
        move_up = controls[0]
        move_left = controls[1]
        move_down = controls[2]
        move_right = controls[3]
        boss_key = controls[4]

        spider_max_health = 1000

        # on key press character movement function is called
        window.bind("<Key>", lambda event: character_movement(event, move_up, move_down, move_left, move_right, boss_key,
                                                             character_health, character_x, character_y))
        
        
        # on left mouse click character shoots
        window.bind("<Button-1>", lambda event: shoot(character_x, character_y, char_angle))

        # bullets move
        bullet_move()

        # check if spider hit by bullet
        check_spider_hit()
        
        # check if spider is dead (no health)
        spider_dead(spider_max_health)

        # check if character hit by spider
        check_character_hit(character_x, character_y)

        # spider follows the user
        spider_movement(x_diff, y_diff, spider_x, spider_y, spider_max_health)


        # updates every ms
        window.after(1, update)

    update()
    
    # setting window to fullscreen
    window.wm_attributes("-fullscreen", True)
    window.mainloop()