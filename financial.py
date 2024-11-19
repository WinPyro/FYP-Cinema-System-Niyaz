import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class FinancialReport:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#1c1c1c")
        self.display_report()

    def display_report(self):
        # Clear the frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(self.parent, text="Financial Report", font=("Arial", 24, "bold"), fg="black", bg="#e5c07b")
        title.pack(pady=10)

        # Expenses data
        data = {
            "Cashier Salary": 5000,
            "Security Salary": 4000,
            "Cleaning Services": 2000,
            "Electric Bill": 1500,
            "Miscellaneous": 1000
        }

        # Create a dynamic bar chart
        self.canvas_frame = tk.Frame(self.parent, bg="#1c1c1c")
        self.canvas_frame.pack(fill="both", expand=True)

        def draw_chart(event=None):
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            # Get dynamic size for the figure
            width = self.canvas_frame.winfo_width() / 100  # Convert to inches for matplotlib
            height = self.canvas_frame.winfo_height() / 200

            fig, ax = plt.subplots(figsize=(width, height))
            categories = list(data.keys())
            values = list(data.values())
            ax.bar(categories, values, color="#e5c07b")

            # Update text styling for the chart
            ax.set_title("Monthly Expenses", fontsize=14, fontweight="bold", color="black")
            ax.set_ylabel("Amount (USD)", fontsize=12, fontweight="bold", color="black")
            ax.set_facecolor("#1c1c1c")
            ax.tick_params(colors="black", labelsize=10)

            # Display chart in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            canvas.draw()

        self.canvas_frame.bind("<Configure>", draw_chart)  # Redraw chart on window resize

        # Back Button
        back_button = tk.Button(self.parent, text="Back to Main Menu", font=("Arial", 16, "bold"), bg="#3e3e3e", fg="#e5c07b",
                                 activebackground="#4b4b4b", activeforeground="#e5c07b",
                                 command=self.go_back_to_menu)
        back_button.pack(pady=20)

    def go_back_to_menu(self):
        # Clear the frame to return to the main menu
        for widget in self.parent.winfo_children():
            widget.destroy()







            
