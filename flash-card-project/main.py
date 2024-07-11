from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    og_data = pandas.read_csv("data/french_words.csv")
    to_learn = og_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- NEXT CARD ------------------------------- #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_title, text="French", fill="black")
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    en_word = current_card["English"]
    canvas.itemconfig(card_img, image=front_img)
    flip_timer = window.after(5000, func=flip_card)

# ---------------------------- REMOVE CARD ------------------------------- #
def remove_card():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    canvas.itemconfig(card_img, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR)
window.config(padx=50, pady=50)

flip_timer = window.after(5000 , func=flip_card)

canvas = Canvas(width=900, height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(450, 300, image=front_img)
card_title = canvas.create_text(450, 150, text="", font=("Arial", 45, "italic"))
card_word = canvas.create_text(450, 300, text="", font=("Arial", 65, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightbackground=BACKGROUND_COLOR, command=remove_card)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
