from tkinter import *
import pandas
import random
from pathlib import Path

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn = []

# Tries to open the file words_to_learn and set you up for receiving flashcards from that list. If the file does not
# exist, you will get flashcards from the file french_words.
try:
    existing_df = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    df = pandas.read_csv('./data/french_words.csv')
    dict = df.to_dict(orient="records")
else:
    new_dict = existing_df.to_dict(orient="records")
    dict = new_dict


def another_card():
    """keeps the current card, with the word in French, onscreen for three seconds and after which it prompts the
    english translation. Additionally, upon clicking the "wrong_button" it prompts another flashcard"""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(dict)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(title, text='French', fill="black")
    canvas.itemconfig(word, text=current_card['French'], fill="black")
    flip_timer = window.after(3000, func=back_of_card)


def known_card():
    """If you know the word, its particular dictionary will be taken out of the list and another list will be created
    containing exclusively words you do not know. This second list will be saved in a data frame and, ultimately, in a
    csv file"""
    global dict, words_to_learn
    another_card()
    dict.remove(current_card)
    words_to_learn = [n for n in dict]
    new_df = pandas.DataFrame(words_to_learn)
    new_df.to_csv("data/words_to_learn.csv", index=False)


def back_of_card():
    """Configuring the back of the flashcard"""
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(title, text='English', fill="white")
    canvas.itemconfig(word, text=current_card['English'], fill="white")


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(3000, func=back_of_card)


# Creating and configuring the canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(410, 275, image=card_front_image)
title = canvas.create_text(370, 150, text="Title", font=("Arial", 40, "italic"))
word = canvas.create_text(370, 263, text="word", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Creating the buttons
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, fg=BACKGROUND_COLOR, highlightthickness=0,  command=known_card)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, fg=BACKGROUND_COLOR, highlightthickness=0, command=another_card)
wrong_button.grid(column=0, row=1)

# Calls the function in order to get a flashcard onscreen straight from the beginning
another_card()


window.mainloop()
