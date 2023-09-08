import tkinter as tk
import pickle
import datetime
from pynput import keyboard

class SupportTicketTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Mutiny Staff Sit Counter")
        self.root.configure(bg="#111111")  # Set the background color of the root window

        # Set the window to appear at the top
        self.root.attributes('-topmost', True)

        # Create a counter variable
        self.ticket_count = tk.IntVar()
        self.load_count()  # Load the count from a file

        # Create and configure labels
        self.label = tk.Label(root, text="Mutiny Staff Sit Counter", font=("Helvetica", 20), bg="#111111", fg="#ffffff")
        self.label.pack(pady=(20, 10))

        self.count_label = tk.Label(root, text=self.get_display_text(), font=("Helvetica", 36), bg="#111111", fg="#ffffff")
        self.count_label.pack(pady=10)

        self.subtext_label = tk.Label(root, text=self.get_subtext(), font=("Helvetica", 14), bg="#111111", fg="#ffffff")
        self.subtext_label.pack()

        # Create a decrease button
        self.decrease_button = tk.Button(root, text="-", font=("Helvetica", 24), bg="#111111", fg="#ffffff", command=self.decrement_count)
        self.decrease_button.pack()

        # Create a global keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

    def on_key_press(self, key):
        try:
            if key.char == "#":
                self.increment_count()  # Increment the count when the "#" key is pressed
        except AttributeError:
            pass

    def increment_count(self):
        current_count = self.ticket_count.get()
        if current_count < 90:
            self.ticket_count.set(current_count + 1)
            self.save_count()  # Save the count to a file
            self.update_count_label()

    def decrement_count(self):
        current_count = self.ticket_count.get()
        if current_count > 0:
            self.ticket_count.set(current_count - 1)
            self.save_count()  # Save the count to a file
            self.update_count_label()

    def save_count(self):
        with open("ticket_count.pkl", "wb") as f:
            pickle.dump(self.ticket_count.get(), f)

    def load_count(self):
        try:
            with open("ticket_count.pkl", "rb") as f:
                count = pickle.load(f)
                self.ticket_count.set(count)
        except FileNotFoundError:
            pass

    def get_display_text(self):
        return f"{self.ticket_count.get()} / 90"

    def get_subtext(self):
        current_day = datetime.datetime.now().weekday()
        current_count = self.ticket_count.get()
        days_remaining = 5 - current_day  # Assuming Monday is 0 and Friday is 4

        if days_remaining <= 0:
            return "You've exceeded the goal!"
        
        average_goal = round((90 - current_count) / days_remaining)
        return f"Aim for {average_goal} tickets/day to reach the goal."

    def update_count_label(self):
        self.count_label.config(text=self.get_display_text())
        self.subtext_label.config(text=self.get_subtext())

if __name__ == "__main__":
    root = tk.Tk()
    app = SupportTicketTracker(root)
    root.mainloop()
