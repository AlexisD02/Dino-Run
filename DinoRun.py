# DinoRun.py

# Author: Alexis Demetriou (G20970098)

# Email: ADemetriou5@uclan.ac.uk

# Description: The Dinosaur Game (also known as the Chrome Dino) is a browser game developed by Google and built into the
# Google Chrome web browser. The player guides a pixelated Tyrannosaurus rex across a side-scrolling landscape,
# avoiding obstacles to achieve a higher score.
# The DinoRun.py program demonstrates the Dino Runner game with additional features and original graphics.

# The definition of the dino and bird is reused from the interactive_flappy_wings.py code provided under Week06, step0604.
# The definition of the ground, cacti, cloud and background is reused from the adding_obstacles.py code provided under Week07, step0704.
# The definition of the random width is reused from the Exercise0705.py code provided under Week07, xtras.
# The text that display the score (points) in the bottom right corner of the window, in the middle and in the bottom left of the windows canvas is
# reused from the ShowingTextOnCanvas.py code provided under Week03, step0303.
# A new list containing a sequence of colors (as strings) to be used to fill background color is reused from the
# MoreMouseInputWithLists.py code provided under Week02, step0204.
# A function that is executed to change the background color is reused from the traffic_lights.py code provided under Week06, step0602.
# The nested-if structure is adapted from the lecture slides week 1, slide 61.
# A high score feature for reading/writing the high scores in a file were adopted from
# the source code https://stackoverflow.com/questions/39746641/retrieving-a-single-integer-from-a-text-file-and-assigning-it-to-a-variable.

from tkinter import *
from random import randint

TITLE = "Dino Run"
WIDTH, HEIGHT = 800, 600  # the width and height for the resolution
"""
WARNING! 
Changing the window resolution can damage the game!
"""
in_a_jump = False  # this boolean values tells us when already in a jump as to not start another one
jump_offsets = [0, -70, -40, -25, -15, -10, -5, -2, -1, 0, 1, 2, 5, 10, 15, 25, 40, 55, 35, -20]  # movements of a jump over time
jump_index = 0  # used to keep track of the phase of the jump, it completes after len(jump_offsets) steps
DELAY, DELAY_JUMP, DELAY_GIF, DELAY_SCORE, DELAY_BACKGROUND = 35, 50, 120, 100, 50 * 1000  # delay for animation, gif, score and background between animations, in milliseconds
frame_index_dino, frame_index_bird = 0, 0  # the index of the current dino and bird frame - used to drive the animation
FRAME_COUNT_DINO, FRAME_COUNT_BIRD = 6, 2  # total frames of dino and bird in the animation
scored_points = 0  # initial score of the game
COLORS = ['tan', 'sky blue', 'light sky blue', 'navajo white', 'midnight blue', 'black']  # define a new List to hold the colors for the background.
color_index = randint(0, len(COLORS) - 1)  # random index for the background color
start_game = False  # the game only starts when the player presses the enter key
game_over = False  # the player will be able to play the game until the dino object collides with moving objects
pause = False  # the player will be able to pause the game by pressing the small or capital "P" key
pause_text = []
game_over_text = []

win = Tk()  # creates a GUI window (using the tkinter library)
win.title(TITLE)  # sets window's title to 'Dino Run' (shown in the top area)

canvas = Canvas(win, width=WIDTH, height=HEIGHT)  # link the canvas to the 'win' and set its size (in this case the full window).
canvas.config(bg=COLORS[color_index])  # sets the background color of the canvas using the 'bg' property.
canvas.pack()  # the following command ('pack') packs the widget within the host window.

# load the background images
cloud_img = PhotoImage(file='resources/cloud.png')
ground_img = PhotoImage(file='resources/ground.png')
cactus_small = PhotoImage(file='resources/cactus-small.png')
two_cacti_small = PhotoImage(file='resources/two-cacti-small.png')
cactus_big = PhotoImage(file='resources/cactus-big.png')
many_cacti = PhotoImage(file='resources/many-cacti.png')

# display the background images
clouds_obj = (canvas.create_image(WIDTH // 3, HEIGHT // 3, image=cloud_img),
              canvas.create_image(WIDTH * 2 // 3, HEIGHT // 3 - 50, image=cloud_img))  # initial coordinates of two clouds
list_clouds_height = (HEIGHT // 3 - 50, HEIGHT // 3 - 30, HEIGHT // 3 - 10, HEIGHT // 3 + 10, HEIGHT // 3 + 30, HEIGHT // 3 + 50)

ground_obj = canvas.create_image(WIDTH // 2, HEIGHT - ground_img.height() // 2, image=ground_img)  # initial coordinates of the ground
cactus_small_obj = canvas.create_image(-cactus_small.width(), HEIGHT - cactus_small.height() // 2 - ground_img.height() + 15,
                                       image=cactus_small)  # initial coordinates of the small cactus
two_cacti_small_obj = canvas.create_image(-two_cacti_small.width(), HEIGHT - two_cacti_small.height() // 2 - ground_img.height() + 15,
                                          image=two_cacti_small)  # initial coordinates of the two small cacti
cactus_big_obj = canvas.create_image(-cactus_big.width(), HEIGHT - cactus_big.height() // 2 - ground_img.height() + 15,
                                     image=cactus_big)  # initial coordinates of the big cactus
many_cacti_obj = canvas.create_image(-many_cacti.width(), HEIGHT - many_cacti.height() // 2 - ground_img.height() + 15,
                                     image=many_cacti)  # initial coordinates of the many cacti
random_obj = randint(0, 4)  # the game will initially select a random object
dino_frames = [PhotoImage(file='resources/dino%i.png' % i) for i in range(FRAME_COUNT_DINO)]  # the 'dino_frames' array contains the 6 image frames
bird_frames = [PhotoImage(file='resources/bird%i.png' % i) for i in range(FRAME_COUNT_BIRD)]  # the 'bird_frames' array contains the 2 image frames
dino = canvas.create_image(WIDTH // 4 + 10, HEIGHT - dino_frames[0].height() / 2 - ground_img.height() + 15, image=dino_frames[0])  # initial coordinates of the dino
bird = canvas.create_image(-bird_frames[0].width(), HEIGHT - bird_frames[0].height() / 2 - ground_img.height(), image=bird_frames[0])  # initial coordinates of the bird
start_text = canvas.create_text(WIDTH // 2, HEIGHT - 55, text='Press Enter to start the game', font=("Georgia", 16), fill='black')
score = canvas.create_text(WIDTH - 40, HEIGHT - 15, text=f"{scored_points:08d}", font=("Georgia", 12))  # text score coordinates of the game
file_r = open("High Score.txt", "r")   # opens the file for "read" operations
high_score = int(file_r.read())  # read high score of the game from a .txt file
high_score_text = canvas.create_text(WIDTH - 175, HEIGHT - 15, text="High Score: " + str(high_score), font=("Georgia", 12))  # display the high score of the game
canvas.create_text(175, HEIGHT - 15, text='CO1417 Dino Run | Q: Quit, P: Pause, R: Restart', font=("Georgia", 12))  # display the instructions of the game
# Print the instructions in the terminal.
print("Press Enter to start the game")
print("Press Q to Quit.")
print("Press P to Pause/Play.")
print("Press R to Restart.")


def update():
    """
    This function is called periodically to update the coordinates of ground, cacti and bird image. It resets them when they fall off the screen.
    """
    global list_clouds_height, random_obj, game_over  # use global variables (defined outside the function)
    # handle the 'clouds' part of the background - it moves at a slower pace to create a parallax phenomenon
    for i in range(len(clouds_obj)):
        (x, y) = canvas.coords(clouds_obj[i])  # this extracts the coordinates of the cloud object
        if x >= -cloud_img.width():  # if the cloud image has not gone off the screen,
            canvas.move(clouds_obj[i], -1, 0)  # then move the cloud to the left by changing the x by -1
        else:
            random_cloud = list_clouds_height[randint(0, len(list_clouds_height) - 1)]
            canvas.coords(clouds_obj[i], WIDTH + cloud_img.width() // 2, random_cloud)
            # reset the cloud, moving it back to the starting point and changing randomly the height of the cloud

    # handle the 'ground' part of the background
    (x, y) = canvas.coords(ground_obj)  # this extracts the coordinates of the ground object
    if x >= 0:  # if the ground image has not gone off the screen,
        canvas.move(ground_obj, -10, 0)  # move the ground to the left by changing the x by -10
    else:
        canvas.move(ground_obj, WIDTH, 0)  # reset the ground, moving it back to the starting point

    (x_dino, y_dino) = canvas.coords(dino)  # this extracts the coordinates of the dino
    if random_obj == 0:  # if the random object is a small cactus,
        # then handle the 'small cactus' part of the background
        (x, y) = canvas.coords(cactus_small_obj)  # this extracts the coordinates of the small cactus
        if x >= -cactus_small.width():  # if the small cactus image has not gone off the screen,
            canvas.move(cactus_small_obj, -10, 0)  # move the small cactus to the left by changing the x by -10
            if x - cactus_small.width() / 2 <= x_dino + dino_frames[0].width() / 2 and x + cactus_small.width() / 2 >= x_dino - \
                    dino_frames[0].width() / 2 and y - cactus_small.height() / 2 <= y_dino + dino_frames[0].height() / 2:
                # if the dino collided with a small cactus
                game_over = True  # then the game is over
                return game_over
        else:
            random_object()  # when the object goes off the screen, the program itself selects the next random object
    if random_obj == 1:  # if the random object is two small cacti,
        # then handle the 'two small cacti' part of the background
        (x, y) = canvas.coords(two_cacti_small_obj)  # this extracts the coordinates of two small cacti
        if x >= -two_cacti_small.width():  # if the two small cacti image has not gone off the screen,
            canvas.move(two_cacti_small_obj, -10, 0)  # move two small cacti to the left by changing the x by -10
            if x - two_cacti_small.width() / 2 <= x_dino + dino_frames[0].width() / 2 and x + two_cacti_small.width() / 2 >= x_dino - \
                    dino_frames[0].width() / 2 and y - two_cacti_small.height() / 2 <= y_dino + dino_frames[0].height() / 2:
                # if the dino collided with two small cacti
                game_over = True  # then the game is over
                return game_over
        else:
            random_object()  # when the object goes off the screen, the program itself selects the next random object
    if random_obj == 2:  # if the random object is a big cactus,
        # then handle the 'big cactus' part of the background
        (x, y) = canvas.coords(cactus_big_obj)  # this extracts the coordinates of the big cactus
        if x >= -cactus_big.width():  # if the big cactus image has not gone off the screen,
            canvas.move(cactus_big_obj, -10, 0)  # then move the big cactus to the left by changing the x by -10
            if x - cactus_big.width() / 2 <= x_dino + dino_frames[0].width() / 2 and x + cactus_big.width() / 2 >= x_dino - \
                    dino_frames[0].width() / 2 and y - cactus_big.height() / 2 <= y_dino + dino_frames[0].height() / 2:
                # if the dino collided with big cactus
                game_over = True  # then the game is over
                return game_over
        else:
            random_object()  # when the object goes off the screen, the program itself selects the next random object
    if random_obj == 3:  # if the random object are many cacti,
        # then handle the 'many cacti' part of the background
        (x, y) = canvas.coords(many_cacti_obj)  # this extracts the coordinates of many cacti
        if x >= -many_cacti.width():  # if many cacti image has not gone off the screen,
            canvas.move(many_cacti_obj, -10, 0)  # then move many cacti to the left by changing the x by -15
            if x - many_cacti.width() / 2 <= x_dino + dino_frames[0].width() / 2 and x + many_cacti.width() / 2 >= x_dino - \
                    dino_frames[0].width() / 2 and y - many_cacti.height() / 2 <= y_dino + dino_frames[0].height() / 2:
                # if the dino collided with a many cacti (obj)
                game_over = True  # then the game is over
                return game_over
        else:
            random_object()  # when the object goes off the screen, the program itself selects the next random object
    if random_obj == 4:  # if the random object is a bird,
        # then handle the 'bird' part of the background
        (x, y) = canvas.coords(bird)  # this extracts the coordinates of the bird
        if x >= -bird_frames[0].width():  # if the bird image has not gone off the screen,
            canvas.move(bird, -16, 0)  # then move the bird to the left by changing the x by -16
            if x - bird_frames[0].width() / 2 <= x_dino + dino_frames[0].width() / 2 and x + bird_frames[0].width() / 2 >= x_dino - \
                    bird_frames[0].width() / 2 and y - bird_frames[0].height() / 2 <= y_dino + dino_frames[0].height() / 2:
                # if the dino collided with a bird
                game_over = True  # then the game is over
                return game_over
        else:
            random_object()  # when the object goes off the screen, the program itself selects the next random object

    if not pause:  # if there is no pause,
        win.after(DELAY, update)  # then repeat the loop


def random_object():
    """
    This function was created for the game to independently select a random object and shuffle it to certain coordinates.
    Also, the function will randomly choose the distance between cacti.
    The spacing between them will be between 900 and 1100 pixels wide.
    """
    global random_obj  # use global variable (defined outside the function)
    random_obj = randint(0, 4)  # function randomly selects a number
    random_width = (WIDTH + randint(100, 300))  # the function randomly selects the width
    if random_obj == 0:
        canvas.move(cactus_small_obj, random_width, 0)  # move the small cactus to a random position x
    if random_obj == 1:
        canvas.move(two_cacti_small_obj, random_width, 0)  # move the two small cacti to a random position x
    if random_obj == 2:
        canvas.move(cactus_big_obj, random_width, 0)  # move the big cactus to a random position x
    if random_obj == 3:
        canvas.move(many_cacti_obj, random_width, 0)  # move many cacti to a random position x
    if random_obj == 4:
        canvas.move(bird, random_width, 0)  # move the bird to a random position x


def update_jump_animation():
    """
    In this function, the dino will jump to a certain height using the jump offsets, only when the player presses the "space" key.
    """
    global in_a_jump, jump_index  # use global variables (defined outside the function)
    if not game_over and not pause:  # if the object has not crashed and there is no pause
        if in_a_jump:  # if in a jump, move the character by jump_offset
            jump_offset = jump_offsets[jump_index]  # pick the current offset
            canvas.move(dino, 0, jump_offset)  # the 'canvas.move' function moves the specified object by the given X,Y pixels
            jump_index = jump_index + 1  # prepare for the next phase of the jump
            if jump_index > len(jump_offsets) - 1:  # when the jump ends...
                jump_index = 0  # ...reset the jump_index...
                in_a_jump = False  # ...and set in_a_jump back to False
        win.after(DELAY_JUMP, update_jump_animation)  # repeat the loop


def update_animation():
    """
    Dino animation and also bird animation will be updated in this function. When a dino jumps, the animation will not be updated.
    """
    global frame_index_dino, frame_index_bird, in_a_jump  # use global variables (defined outside the function)
    # update the frame picture
    canvas.itemconfig(dino, image=dino_frames[frame_index_dino])  # set the next frame to the 'dino' image
    canvas.itemconfig(bird, image=bird_frames[frame_index_bird])  # set the next frame to the 'bird' image
    frame_index_bird += 1  # updates the bird index
    if not in_a_jump:  # if the dino is not in a jump,
        frame_index_dino += 1  # then the dino index updates.
    else:  # if the dino is in a jump,
        frame_index_dino = 0  # then the animation will not update.
    if frame_index_dino == FRAME_COUNT_DINO - 1:  # if the dino index is out of bounds,
        frame_index_dino = 1  # then the animation starts over.
    if frame_index_bird == FRAME_COUNT_BIRD:  # if the bird index is out of bounds,
        frame_index_bird = 0  # then the animation starts over.
    if not game_over and not pause:  # if the object has not crashed and there is no pause,
        win.after(DELAY_GIF, update_animation)  # then repeat the loop.
    elif game_over:  # if the dino object crashed,
        canvas.itemconfig(dino, image=dino_frames[5])  # then a dead dino will be drawn.


def update_background():
    """
    This function will drastically update the background color every 500 points earned.
    """
    global COLORS, color_index  # use global variables (defined outside the function)
    if color_index == len(COLORS) - 1:  # if the color index is out of range,
        color_index = -1  # if the color index is out of bounds, then the color will be the first array of the COLORS List
    color_index += 1  # updates the color index
    canvas.config(bg=COLORS[color_index])  # updates the background color


def update_score():
    """
    This function will add and update earned points every 100ms (0.1sec). Earned points will be displayed on Windows canvas in the bottom right corner.
    """
    global scored_points, DELAY  # use global variables (defined outside the function)
    canvas.itemconfig(score, text=str(f"{scored_points:08d}"))  # the code updates the text, which shows the score
    scored_points += 1  # plus one point every 100ms (0.1 sec)
    # Every accrual of 20 points the game will speed up. The game update chapel will be 15 ms (0.015 sec).
    if scored_points % 20 == 0 and scored_points != 0 and DELAY >= 15:
        DELAY -= 1
    if scored_points % 500 == 0 and scored_points != 0:
        update_background()
    if not game_over and not pause:  # if the object has not crashed and there is no pause,
        win.after(DELAY_SCORE, update_score)  # then repeat the loop


def jump(__self__):
    """
    This function is called when a jump is initiated.
    """
    global in_a_jump  # use global variable (defined outside the function)
    # Only process the jump event if no other jump is in progress, the game is not paused and when the player pressed the enter key to start the game
    if not in_a_jump and not pause and start_game:
        in_a_jump = True


def on_key_press(event):
    """
    This function is called to handle arbitrary key presses.
    """
    global pause, pause_text, scored_points, game_over, game_over_text, random_obj, DELAY, in_a_jump, jump_index, start_game
    # Use global variables (defined outside the function).
    if event.char == 'Q' or event.char == 'q':  # handle small or capital Q
        quit()  # quit the game (windows closes)
    if (event.char == 'P' or event.char == 'p') and not game_over and start_game:  # handle small or capital P
        pause = not pause  # pause/unpause the game when player presses "P" key
        pause_text.append(canvas.create_text(WIDTH // 2, HEIGHT // 2, text='PAUSE', fill='white', font=("Berlin Sans FB", 40)))
        # The pause text will be displayed in the center of the Windows canvas.
        if not pause:  # if there is no pause,
            for i in pause_text:
                canvas.delete(i)  # then the displayed text will be deleted.
            game()  # all functions will work again as there is no pause
        return pause
    if (event.char == 'R' or event.char == 'r') and start_game:  # handle small or capital R
        scored_points = 0   # renew earned points in the game
        DELAY = 35  # reload the DELAY (speed) in the game
        canvas.coords(dino, WIDTH // 4 + 10, HEIGHT - dino_frames[0].height() / 2 - ground_img.height() + 15)  # assign old initial dino coordinates
        in_a_jump = False
        jump_index = 0
        if random_obj == 0:  # if the small cactus object is within windows canvas
            canvas.coords(cactus_small_obj, - cactus_small.width(), HEIGHT - cactus_small.height() / 2 - ground_img.height() + 15)
            # assign old initial small cactus coordinates
        if random_obj == 1:  # if two small cacti object is within windows canvas
            canvas.coords(two_cacti_small_obj, - two_cacti_small.width(), HEIGHT - two_cacti_small.height() / 2 - ground_img.height() + 15)
            # assign old initial two small cacti coordinates
        if random_obj == 2:  # if the big cactus object is within windows canvas
            canvas.coords(cactus_big_obj, - cactus_big.width(), HEIGHT - cactus_big.height() / 2 - ground_img.height() + 15)
            # assign old initial big cactus coordinates
        if random_obj == 3:  # if many cacti object is within windows canvas
            canvas.coords(many_cacti_obj, - many_cacti.width(), HEIGHT - many_cacti.height() / 2 - ground_img.height() + 15)
            # assign old initial many cacti coordinates
        if random_obj == 4:  # if bird object is within windows canvas
            canvas.coords(bird, - bird_frames[0].width(), HEIGHT - bird_frames[0].height() / 2 - ground_img.height())
            # assign old initial bird coordinates
        random_obj = randint(0, 4)
        canvas.itemconfig(dino, image=dino_frames[0])
        if game_over:  # if the object crashed and the game is over, then restart the game by starting all the functions again
            game_over = False
            canvas.delete(game_over_text.pop(0))  # at restart, game over text will be deleted
            game_lost_function()
            game()
        if pause:  # if the game is paused,
            pause = not pause  # then unpause the game
            for i in pause_text:  # delete the pause text
                canvas.delete(i)
            game()
            return pause


def game_lost_function():
    """
    This function will print the text in the middle of windows canvas when the game is over.
    Also, if the player has broken a new record in the game, then it will be written to the text file "High Score.txt"
    """
    global scored_points, high_score, game_over_text, high_score_text  # use global variables (defined outside the function)
    if game_over:  # if the object crashed
        game_over_text.append(canvas.create_text(WIDTH // 2, HEIGHT // 2, text='GAME OVER', fill='white', font=("Berlin Sans FB", 40)))
        print("Game Over!")
        if scored_points > high_score:  # if the point earned in the current game is greater than in previous games
            print("New High Score!")
            canvas.itemconfig(high_score_text, text="High Score: " + str(scored_points))
            file_w = open("High Score.txt", "w")  # opens the file for "write" operations
            file_w.write(repr(scored_points))  # write or rewrite the game points
            file_w.close()  # close the file
    else:  # if the dino object has not crashed,
        win.after(DELAY, game_lost_function)  # then repeat the loop


def game():
    global start_game, high_score, file_r  # use global variables (defined outside the function)
    win.unbind('<Return>')
    start_game = True
    canvas.delete(start_text)  # delete the start text
    file_r = open("High Score.txt", "r")   # opens the file for "read" operations
    high_score = int(file_r.read())  # read high score of the game from a .txt file
    win.after(0, update)
    win.after(0, update_animation)
    win.after(0, update_jump_animation)
    win.after(0, update_score)


game_lost_function()
win.bind('<space>', jump)
win.bind('<KeyPress>', on_key_press)  # '<KeyPress>' is used to handle small or capital Q, P and R.
win.bind('<Return>', lambda _: game())  # the game will not start until the player presses the "Enter" key.
win.mainloop()  # To keep the window around, the 'win.mainloop()' call activates the window.
