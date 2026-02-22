
import tkinter as tk
import random

# Helper to center and resize window to half the screen
def set_half_screen(root):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

# Main app
class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guesser")
        set_half_screen(self.root)
        self.players = []
        self.turn = 0
        self.min_val = 1
        self.max_val = 100
        self.num = random.randint(self.min_val, self.max_val)
        self.setup_player_count_entry()

    def setup_player_count_entry(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.player_count_var = tk.StringVar()
        tk.Label(self.root, text="Enter number of players (minimum 2):").pack(pady=10)
        self.player_count_entry = tk.Entry(self.root, textvariable=self.player_count_var)
        self.player_count_entry.pack()
        self.player_count_entry.focus_set()
        self.player_count_entry.bind('<Return>', lambda e: self.setup_name_entry())
        self.count_button = tk.Button(self.root, text="Next", command=self.setup_name_entry)
        self.count_button.pack(pady=20)

    def setup_name_entry(self):
        try:
            count = int(self.player_count_var.get())
            if count < 2:
                raise ValueError
        except ValueError:
            self.player_count_var.set("")
            self.player_count_entry.focus_set()
            return
        self.player_count = count
        for widget in self.root.winfo_children():
            widget.destroy()
        self.name_vars = [tk.StringVar() for _ in range(self.player_count)]
        self.name_entries = []
        for i in range(self.player_count):
            tk.Label(self.root, text=f"Enter Player {i+1} Name:").pack(pady=5)
            entry = tk.Entry(self.root, textvariable=self.name_vars[i])
            entry.pack()
            self.name_entries.append(entry)

        # Range selection UI
        range_frame = tk.Frame(self.root)
        range_frame.pack(pady=10)
        tk.Label(range_frame, text="Min:").grid(row=0, column=0)
        self.min_entry = tk.Entry(range_frame, width=8)
        self.min_entry.insert(0, str(self.min_val))
        self.min_entry.grid(row=0, column=1, padx=4)
        tk.Label(range_frame, text="Max:").grid(row=0, column=2)
        self.max_entry = tk.Entry(range_frame, width=8)
        self.max_entry.insert(0, str(self.max_val))
        self.max_entry.grid(row=0, column=3, padx=4)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)
        self.name_entries[0].focus_set()
        self.name_entries[-1].bind('<Return>', lambda e: self.start_game())

    def start_game(self):
        names = [var.get().strip().title() for var in self.name_vars]
        if any(not name for name in names):
            return
        # Validate and set range
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            if min_val >= max_val:
                raise ValueError
        except Exception:
            # simple inline feedback using window title flash
            self.root.bell()
            return
        self.min_val, self.max_val = min_val, max_val
        self.players = names
        self.turn = 0
        self.num = random.randint(self.min_val, self.max_val)
        self.setup_game_ui()

    def setup_game_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.turn_label = tk.Label(self.root, text=f"{self.players[self.turn]}'s turn", font=("Arial", 16))
        self.turn_label.pack(pady=10)
        self.prompt_label = tk.Label(self.root, text=f"Guess a number between {self.min_val} and {self.max_val}:")
        self.prompt_label.pack()
        self.entry = tk.Entry(self.root, width=30, font=("Arial", 18))
        self.entry.pack(pady=10, ipady=8)
        self.entry.bind('<Return>', self.check_guess)
        self.guess_button = tk.Button(self.root, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=10)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        self.entry.focus_set()

    def check_guess(self, event=None):
        if self.guess_button['state'] == tk.DISABLED:
            return
        try:
            guess = int(self.entry.get())
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")
            return
        player = self.players[self.turn]
        if guess == self.num:
            self.result_label.config(text=f"{player} Congratulations you won!!")
            self.guess_button.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)
        elif guess < self.num:
            self.result_label.config(text=f"{player}, that's too low. {self.players[(self.turn+1)%len(self.players)]}'s turn.")
            self.turn = (self.turn + 1) % len(self.players)
            self.turn_label.config(text=f"{self.players[self.turn]}'s turn")
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
        elif guess > self.num:
            self.result_label.config(text=f"{player}, that's too high. {self.players[(self.turn+1)%len(self.players)]}'s turn.")
            self.turn = (self.turn + 1) % len(self.players)
            self.turn_label.config(text=f"{self.players[self.turn]}'s turn")
            self.entry.delete(0, tk.END)
            self.entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGame(root)
    root.mainloop()
