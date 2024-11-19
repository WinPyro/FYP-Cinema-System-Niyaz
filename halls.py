import tkinter as tk

class Halls:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#1c1c1c")
        self.show_all_halls()

    def show_all_halls(self):
        # Clear the frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Title for the hall selection menu
        title = tk.Label(self.parent, text="Select Hall", font=("Arial", 24, "bold"), fg="#e5c07b", bg="#1c1c1c")
        title.pack(pady=10)

        # Create buttons for each hall
        for i in range(1, 6):
            hall_button = tk.Button(self.parent, text=f"Hall {i}", font=("Arial", 18), width=15, height=2,
                                    bg="#3e3e3e", fg="#e5c07b", activebackground="#4b4b4b", activeforeground="#e5c07b",
                                    command=lambda i=i: self.open_hall(i))
            hall_button.pack(pady=10)

    def open_hall(self, hall_number):
        # Clear the frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Title for the selected hall
        hall_title = tk.Label(self.parent, text=f"Hall {hall_number}", font=("Arial", 24, "bold"), fg="#e5c07b", bg="#1c1c1c")
        hall_title.pack(pady=10)

        # Screen Label
        screen_label = tk.Label(self.parent, text="SCREEN", font=("Arial", 16), bg="#3e3e3e", fg="#e5c07b", width=40)
        screen_label.pack(pady=10)

        # Seats layout
        seats_frame = tk.Frame(self.parent, bg="#1c1c1c")
        seats_frame.pack()

        rows = ["A", "B", "C", "D", "E"]
        seats_per_row = 10

        for row in rows:
            row_frame = tk.Frame(seats_frame, bg="#1c1c1c")
            row_frame.pack()
            for seat_num in range(1, seats_per_row + 1):
                seat_id = f"{row}{seat_num}"
                seat_button = tk.Button(row_frame, text=seat_id, width=4, height=2, bg="#3e3e3e", fg="#e5c07b",
                                        activebackground="#4b4b4b", activeforeground="#e5c07b")
                seat_button.pack(side="left", padx=2, pady=2)

        # Back Button to return to all halls menu
        back_button = tk.Button(self.parent, text="Back to Halls", font=("Arial", 16), width=15, height=2,
                                 bg="#3e3e3e", fg="#e5c07b", activebackground="#4b4b4b", activeforeground="#e5c07b",
                                 command=self.show_all_halls)
        back_button.pack(pady=20)
