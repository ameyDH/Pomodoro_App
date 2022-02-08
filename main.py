from tkinter import *
import math
import pygame    # we are using pygame to add sound
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
TIMER = None

# ---------------------------- Starting pygame and adding sound playing function------------------------------- #

pygame.mixer.init()

def play_sound():
    pygame.mixer.music.load("nudge.wav")
    pygame.mixer.music.play()

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(TIMER)
    canvas.itemconfig(timer_text, text="00:00")
    title_label_text.config(text="Timer", fg=GREEN)
    check_marks_text.config(text="")
    global REPS
    REPS = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global REPS
    REPS += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS % 2 != 0:
        title_label_text.config(text="Work", fg=GREEN)
        count_down(work_sec)

    elif REPS % 8 == 0:
        title_label_text.config(text="BREAK", fg=RED)
        count_down(long_break_sec)  # we are taking long break after 4 session of work

    elif REPS % 2 == 0:
        title_label_text.config(text="break", fg=PINK)
        count_down(short_break_sec)  # short break after each session of work


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    global REPS

    count_min = math.floor(count / 60)   # math.floor() Return the floor of x as an Integral.
    count_sec = count % 60               # we will get the remaining seconds
    if count_sec == 0:
        count_sec = "00"
    elif count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global TIMER
        TIMER = window.after(1000, count_down, count-1)    # Execute a command after a time delay (takes time parameter in millisecond)

    elif count == 0:
        start_timer()
        mark = ""
        work_sessions = math.floor(REPS / 2)
        for _ in range(work_sessions):
            mark += "✔"
        check_marks_text.config(text=mark)
        play_sound()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# label
title_label_text = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
title_label_text.grid(row=0, column=1)

# canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)       # *args (100 is X coordinate and 112 is Y coordinate)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(row=1, column=1)

# label
check_marks_text = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
check_marks_text.grid(row=3, column=1)

# button
start_button = Button(text="Start", command=start_timer)
start_button.grid(row=2, column=0)

# button
reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(row=2, column=2)


window.mainloop()

