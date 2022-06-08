from tkinter import *
import tkinter as tk
from data import Words


BACKGROUND = "#EFFFFD"
BUTTON_COLOR = "#42C2FF"



class Ui(tk.Tk):
    """Application class handles display, calculation and operation
    inherits the tkinter module

    Args:
        tk (_module_): gui module
    """
    def __init__(self):
        super().__init__()
        self.title("Type Speed App")
        self.config(bg=BACKGROUND, padx=15, pady=20)
        self.timer_count = 60
        self.time = None

        ## instance of word class, generates random words
        self.word = Words()
        self.current_word = ""

        self.title_label = Label(text="Test your typing speed")
        self.title_label.config(font=(50))
        self.title_label.grid(row=0,column=2)

        self.canvas = tk.Canvas(width=900, height=600, highlightthickness=0)
        self.test_text = self.canvas.create_text(450, 300, text="", width=800, font="10", justify="center")
        self.canvas.grid(row=1,column=1, columnspan=3)

        self.score_board = tk.Label(text=f"CWPM: 0     WPM: 0")
        self.score_board.grid(row=2, column=1)

        self.timer_text = tk.Label(text=f"timer: {self.timer_count}")
        self.timer_text.grid(row=2, column=3)

        self.text_area = tk.Entry(width=50)
        self.text_area.focus()
        self.text_area.grid(row=3, column=2)

        self.start_button = tk.Button(text="START", bg=BUTTON_COLOR, command=self.start_count)
        self.start_button.grid(row=4, column=2)


        self.restart_button = tk.Button(text="RESET", bg=BUTTON_COLOR, command=self.restart)
        self.restart_button.grid(row=4, column=3)
        
        
        self.mainloop()
        
    def start_count(self):
        """ method binded to start button
        generates words and starts countdown
        """
        self.start_button['state'] = "disabled"
        self.clear()
        self.current_word = self.word.generate_words(200)
        self.canvas.itemconfig(self.test_text, text=self.current_word)
        self.count_down()
        
        

    def count_down(self):
        """method to handle timer loop using tkinter after function
        initiates calculation method on completion
        """
        if self.timer_count != 0:
            # TODO 1 DISABLE START BUTTON ONCE COUNTDOWN STARTS
            self.timer_count -= 1
            self.timer_text.config(text=f"timer: {self.timer_count}")
            self.time = self.after(1000, self.count_down)
        else:
            self.calculate_score()
            self.start_button['state'] = "normal"
        
    def restart(self):
        """resets user interface
        """
        self.after_cancel(self.time)
        self.clear()
        self.timer_text.config(text=f"timer: {self.timer_count}")
        self.start_button['state'] = "normal"
        
        

    def calculate_score(self):
        """calculates words typed 
        calculates number of correct words typed
        """
        current_word = self.canvas.itemcget(self.test_text, option="text")
        user_entry = self.text_area.get()

        
        self.canvas.itemconfig(self.test_text, text="")

        wpm = (len(user_entry) // 5) / 1
        ln = 0
        for char in user_entry:
            if char == " ":
                ln += 1

        compare_words = current_word.split()[:ln+1]
        user_compare_words = user_entry.split()
        wrong_words = 0
        for word1, word2 in zip(compare_words, user_compare_words):
            if word1.lower() != word2.lower():
                wrong_words += 1

        cwpm = wpm - (wrong_words/1)


        self.display_result(wpm=wpm, cwpm=cwpm)
        self.text_area.delete(0, 'end')


    def display_result(self, wpm, cwpm):
        """displays result to user

        Args:
            wpm (int): words per minute
            cwpm (int): correct words per minute
        """
        self.score_board.config(text=f"CWPM: {cwpm}     WPM: {wpm}")


    def clear(self):
        """clears labels and resets timer
        """
        self.canvas.itemconfig(self.test_text, text="")
        self.display_result(0,0)
        self.timer_count = 60