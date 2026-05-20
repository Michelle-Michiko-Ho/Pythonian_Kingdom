# ```python id="v6n2rq"
from turtle import Turtle, Screen
import random
import tkinter as tk
import tkinter.messagebox
import pygame

# =========================================================
# INITIALIZE PYGAME AUDIO
# =========================================================
pygame.mixer.init()

# ---------------------------------------------------------
# ASSUMED AUDIO FILES (place these in same folder)
#
# background_music.mp3
# win.wav
# lose.wav
# countdown.wav
# start.wav
# ---------------------------------------------------------

# =========================================================
# CONFIGURATION
# =========================================================
colors = ["red", "blue", "green", "orange"]
y_position = [-90, -30, 30, 90]

is_race_on = False
user_bet = ""
all_turtles = []

# =========================================================
# SCREEN SETUP
# =========================================================
screen = Screen()
screen.setup(width=700, height=500)
screen.bgcolor("lightyellow")
screen.title("🐢 Ultimate Turtle Race")

# Smooth animation
screen.tracer(0)

# =========================================================
# TKINTER ROOT
# =========================================================
canvas = screen.getcanvas()
root = canvas.master

# =========================================================
# TITLE TURTLE
# =========================================================
title_turtle = Turtle()
title_turtle.hideturtle()
title_turtle.penup()
title_turtle.goto(0, 200)
title_turtle.color("darkblue")
title_turtle.write(
    "ULTIMATE TURTLE RACE",
    align="center",
    font=("Arial", 24, "bold")
)

# =========================================================
# FINISH LINE
# =========================================================
finish_line = Turtle()
finish_line.hideturtle()
finish_line.penup()
finish_line.goto(250, -200)
finish_line.pendown()
finish_line.left(90)

for _ in range(20):
    finish_line.forward(10)
    finish_line.penup()
    finish_line.forward(10)
    finish_line.pendown()

# =========================================================
# TURTLE CREATION
# =========================================================
for turtle_index in range(len(colors)):

    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()

    new_turtle.color(colors[turtle_index])

    new_turtle.goto(x=-300, y=y_position[turtle_index])

    # Fastest speed
    new_turtle.speed(0)

    all_turtles.append(new_turtle)

screen.update()

# =========================================================
# DROPDOWN MENU
# =========================================================
user_bet_var = tk.StringVar(root)
user_bet_var.set("Select a turtle color")

option_menu = tk.OptionMenu(root, user_bet_var, *colors)

option_menu.config(
    width=18,
    font=("Helvetica", 14),
    bg="lightgreen",
    fg="darkred"
)

option_menu.place(x=120, y=420)

# =========================================================
# STATUS LABEL
# =========================================================
status_label = tk.Label(
    root,
    text="Choose a turtle and press Start",
    font=("Arial", 17, "bold"),
    fg="white"
)

status_label.place(x=200, y=380)

# =========================================================
# COUNTDOWN DISPLAY TURTLE
# =========================================================
countdown_turtle = Turtle()
countdown_turtle.hideturtle()
countdown_turtle.penup()
countdown_turtle.goto(0, 0)

# =========================================================
# RESET FUNCTION
# =========================================================
def reset_race():

    global is_race_on

    is_race_on = False

    # Stop all music
    pygame.mixer.music.stop()

    # Reset turtles
    for index, turtle in enumerate(all_turtles):
        turtle.goto(-300, y_position[index])

    # Re-enable controls
    start_button.config(state=tk.NORMAL)
    option_menu.config(state=tk.NORMAL)

    status_label.config(
        text="Choose a turtle and press Start"
    )

    screen.update()

# =========================================================
# COUNTDOWN FUNCTION
# =========================================================
countdown_numbers = ["3", "2", "1", "GO!"]
count_index = 0

def show_countdown():

    global count_index

    countdown_turtle.clear()

    if count_index < len(countdown_numbers):

        #pygame.mixer.Sound("race_countdown.wav").play()

        countdown_turtle.write(
            countdown_numbers[count_index],
            align="center",
            font=("Arial", 40, "bold")
        )

        count_index += 1

        screen.update()

        screen.ontimer(show_countdown, 1000)

    else:

        countdown_turtle.clear()

        #pygame.mixer.Sound("race_countdown.wav").play()

        # Start background music
        #pygame.mixer.music.load("race_countdown.wav")

        #pygame.mixer.music.set_volume(0.5)

        #pygame.mixer.music.play(-1)

        screen.ontimer(start_game_loop, 50)

# =========================================================
# START BUTTON CALLBACK
# =========================================================
def start_race_callback():

    global is_race_on
    global user_bet
    global count_index

    selected_bet = user_bet_var.get()

    if selected_bet not in colors:

        tk.messagebox.showwarning(
            title="No Selection",
            message="Please select a turtle color first!"
        )

        return

    user_bet = selected_bet

    if not is_race_on:

        is_race_on = True

        count_index = 0

        # Disable controls
        start_button.config(state=tk.DISABLED)
        option_menu.config(state=tk.DISABLED)

        status_label.config(
            text=f"You bet on the {user_bet} turtle!"
        )

        # Start countdown
        show_countdown()

# =========================================================
# MAIN GAME LOOP
# =========================================================
def start_game_loop():

    global is_race_on

    if is_race_on:

        for turtle in all_turtles:

            rand_distance = random.randint(1, 12)

            turtle.forward(rand_distance)

            # Winner detected
            if turtle.xcor() > 250:

                is_race_on = False

                pygame.mixer.music.stop()

                winning_color = turtle.pencolor()

                # -------------------------------------------------
                # WIN / LOSS LOGIC
                # -------------------------------------------------
                if winning_color == user_bet:

                    #pygame.mixer.Sound("race_countdown.wav").play()

                    result_message = (
                        f"🎉 YOU WON!\n\n"
                        f"The {winning_color} turtle won the race!"
                    )

                else:

                    #pygame.mixer.Sound("race_countdown.wav").play()

                    result_message = (
                        f"😢 YOU LOST!\n\n"
                        f"The {winning_color} turtle won the race!"
                    )

                status_label.config(
                    text=f"Winner: {winning_color.upper()}"
                )

                # Popup
                tk.messagebox.showinfo(
                    title="Race Over",
                    message=result_message,
                    parent=root
                )

                # Ask user to play again
                play_again = tk.messagebox.askyesno(
                    title="Play Again?",
                    message="Would you like to race again?"
                )

                if play_again:
                    reset_race()
                else:
                    root.destroy()

                screen.update()

                return

        screen.update()

        # ~60 FPS smooth animation
        screen.ontimer(start_game_loop, 16)

# =========================================================
# START BUTTON
# =========================================================
start_button = tk.Button(
    root,
    text="START RACE",
    command=start_race_callback,
    font=("Arial", 14, "bold"),
    bg="orange",
    fg="black",
    padx=10,
    pady=5
)

start_button.place(x=500, y=415)

# =========================================================
# EXIT ON CLICK
# =========================================================
screen.exitonclick()
#```
