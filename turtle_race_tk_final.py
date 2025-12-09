from turtle import Turtle, Screen
import random
import tkinter as tk
import tkinter.messagebox # Add this line near your other imports


# --- Configuration Variables ---
colors = ["red", "blue", "orange", "green", "purple", "dodgerblue"]
y_position = [-20, 20, 60, 100, 140, 190]
is_race_on = False
user_bet = ""
all_turtles = []

# --- Tkinter Integration Functions ---

def start_race_callback():
    """
    Called when the 'Start Race' button is clicked.
    Sets the global user_bet and initiates the first game loop timer event.
    """
    global is_race_on, user_bet
    
    selected_bet = user_bet_var.get()
    if selected_bet == "Select a color for betting" or selected_bet not in colors:
        print("Please select a valid color before starting the race.")
        return
        
    user_bet = selected_bet
    if not is_race_on: # Prevent starting the loop multiple times if button is hammered
        is_race_on = True
        # Disable controls
        start_button.config(state=tk.DISABLED)
        option_menu.config(state=tk.DISABLED)
        print(f"Race started! You bet on the {user_bet} turtle.")
        # Start the *actual* game loop timer sequence here
        screen.ontimer(start_game_loop, 50) 


# --- Turtle Setup ---
screen = Screen()
screen.setup(width=500, height=500)
screen.title("Turtle Race")
# Optional: Speed up turtle animations by turning off automatic tracing for performance
screen.tracer(0) 


# --- Tkinter Widget Setup ---
canvas = screen.getcanvas()
root = canvas.master

user_bet_var = tk.StringVar(root)
user_bet_var.set("Select a color for betting")

option_menu = tk.OptionMenu(root, user_bet_var, *colors)
option_menu.config(
    width=17, 
    font=('Helvetica', 15),
    bg='lightgreen',
    fg='darkred'
)
option_menu.place(x=130, y=350) 

start_button = tk.Button(root, text="Start Race", command=start_race_callback)
start_button.place(x=350, y=350)


# --- Turtle Initialization ---
for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])
    new_turtle.goto(x=-230, y=y_position[turtle_index])
    all_turtles.append(new_turtle)

# Manually update the screen once after initial placement since tracer is off
screen.update()

# --- Main Race Loop Function ---

def start_game_loop():
    """
    This function updates turtle positions and checks for the winner.
    It reschedules itself using ontimer as long as the race is on.
    """
    global is_race_on, user_bet, root

    if is_race_on:
        for turtle in all_turtles:
            rand_distance = random.randint(0, 10)
            turtle.forward(rand_distance)
            
            # Check for winner *inside* the movement loop
            if turtle.xcor() > 230:
                is_race_on = False
                winning_color = turtle.pencolor()
                if winning_color == user_bet:
                    result_message = f"You've won! The {winning_color} turtle is the winner!"
                else:
                    result_message = f"You've lost! The {winning_color} turtle is the winner!"
                
                print(result_message)

                # --- FIX IS HERE: Use Tkinter Messagebox instead of screen.textinput ---
                tk.messagebox.showinfo(title="Race Over", message=result_message, parent=root)
                # ---------------------------------------------------------------------

                # Re-enable controls after the race finishes
                start_button.config(state=tk.NORMAL)
                option_menu.config(state=tk.NORMAL)
                screen.update() # Final update to show finished positions
                return # Stop the ontimer sequence
        
        # If the race is still on, schedule the next frame update
        screen.update() # Update the display after all turtles move
        screen.ontimer(start_game_loop, 30) # Reschedule the function call (30ms delay)



# The main execution starts here. The game loop begins only when the button is pressed.
screen.exitonclick()

