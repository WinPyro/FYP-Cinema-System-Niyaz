import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
from cctv import CCTVControlRoom
from halls import Halls
from financial import FinancialReport
import sqlite3
import os
from PIL import Image, ImageTk


class CinemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Niyaz Cinemark Theater")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1c1c1c")

        # Database initialization
        self.conn = sqlite3.connect("cinema.db")
        self.cursor = self.conn.cursor()
        self.setup_database()

        try:
            self.original_logo = PhotoImage(file="logo.png")
            self.logo_image = self.original_logo.subsample(10, 10)
        except Exception as e:
            messagebox.showerror("Image Load Error", f"Could not load logo image: {e}")
            self.logo_image = None

        self.main_menu()

    def setup_database(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TEXT,
                halls INTEGER,
                screen_time INTEGER,
                image_path TEXT
            )
            """
        )
        self.conn.commit()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        navbar = tk.Frame(self.root, bg="#2c2c2c", height=60)
        navbar.pack(fill="x", side="top")

        if self.logo_image:
            logo_canvas = tk.Canvas(navbar, width=50, height=50, bg="#2c2c2c", highlightthickness=0)
            logo_canvas.create_oval(5, 5, 45, 45, fill="#2c2c2c", outline="")
            logo_canvas.create_image(25, 25, image=self.logo_image)
            logo_canvas.bind("<Button-1>", lambda e: self.main_menu())
            logo_canvas.pack(side="left", padx=10, pady=10)

        options = [
            ("Create a new movie entry", self.create_movie),
            ("See existing list of movies", self.show_movies),
            ("See halls", self.show_halls),
            ("See financial reports", self.show_reports),
            ("CCTV", self.show_cctv),
            ("Exit", self.exit_app),
        ]

        for text, command in options:
            button = tk.Button(
                navbar,
                text=text,
                font=("Arial", 14),
                bg="#2c2c2c",
                fg="#e5c07b",
                activebackground="#3a3a3a",
                activeforeground="#e5c07b",
                bd=0,
                command=lambda cmd=command: self.animate_button(cmd),
            )
            button.pack(side="left", padx=15, pady=10)
            button.bind("<Enter>", lambda e, btn=button: btn.config(bg="#3e3e3e"))
            button.bind("<Leave>", lambda e, btn=button: btn.config(bg="#2c2c2c"))

        self.content_frame = tk.Frame(self.root, bg="#1c1c1c")
        self.content_frame.pack(expand=True, fill="both")

        welcome_label = tk.Label(
            self.content_frame,
            text="Welcome to Niyaz Cinemark Theater Management System",
            font=("Arial", 24, "bold"),
            fg="#e5c07b",
            bg="#1c1c1c",
        )
        welcome_label.pack(pady=20)

        description = tk.Label(
            self.content_frame,
            text=(
                "This platform is designed to streamline operations within the cinema theater industry. "
                "It integrates various services like movie management, hall scheduling, CCTV monitoring, and "
                "financial reporting into one unified platform.\n\n"
                "Whether you're managing a small theater or a multi-branch cinema chain, this system offers "
                "the tools you need to enhance efficiency and ensure customer satisfaction."
            ),
            font=("Arial", 14),
            fg="#e5c07b",
            bg="#1c1c1c",
            wraplength=800,
            justify="center",
        )
        description.pack(pady=20)

    def animate_button(self, command):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        animation_label = tk.Label(self.content_frame, text="Loading...", font=("Arial", 20), fg="#e5c07b", bg="#1c1c1c")
        animation_label.pack(pady=20)

        def finish_animation():
            animation_label.destroy()
            command()

        animation_label.after(500, finish_animation)

    def create_movie(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.content_frame, text="Create New Movie Entry", font=("Arial", 24, "bold"), fg="#e5c07b", bg="#1c1c1c")
        title.pack(pady=10)

        movie_label = tk.Label(self.content_frame, text="Movie Name:", font=("Arial", 16), fg="#e5c07b", bg="#1c1c1c")
        movie_label.pack(pady=5)
        self.movie_entry = tk.Entry(self.content_frame, font=("Arial", 16), bg="#3e3e3e", fg="#e5c07b", insertbackground="#e5c07b")
        self.movie_entry.pack(pady=5)

        date_label = tk.Label(self.content_frame, text="Date of Creation (YYYY-MM-DD):", font=("Arial", 16), fg="#e5c07b", bg="#1c1c1c")
        date_label.pack(pady=5)
        self.date_entry = tk.Entry(self.content_frame, font=("Arial", 16), bg="#3e3e3e", fg="#e5c07b", insertbackground="#e5c07b")
        self.date_entry.pack(pady=5)

        halls_label = tk.Label(self.content_frame, text="Number of Halls (1-5):", font=("Arial", 16), fg="#e5c07b", bg="#1c1c1c")
        halls_label.pack(pady=5)
        self.halls_entry = tk.Entry(self.content_frame, font=("Arial", 16), bg="#3e3e3e", fg="#e5c07b", insertbackground="#e5c07b")
        self.halls_entry.pack(pady=5)

        screen_time_label = tk.Label(self.content_frame, text="Total Screen Time per Day (hours):", font=("Arial", 16), fg="#e5c07b", bg="#1c1c1c")
        screen_time_label.pack(pady=5)
        self.screen_time_entry = tk.Entry(self.content_frame, font=("Arial", 16), bg="#3e3e3e", fg="#e5c07b", insertbackground="#e5c07b")
        self.screen_time_entry.pack(pady=5)

        image_label = tk.Label(self.content_frame, text="Movie Poster Image:", font=("Arial", 16), fg="#e5c07b", bg="#1c1c1c")
        image_label.pack(pady=5)
        self.image_path = None
        upload_button = tk.Button(
            self.content_frame,
            text="Upload Image",
            font=("Arial", 16),
            bg="#3e3e3e",
            fg="#e5c07b",
            activebackground="#4b4b4b",
            activeforeground="#e5c07b",
            command=self.upload_image,
        )
        upload_button.pack(pady=10)

        save_button = tk.Button(
            self.content_frame,
            text="Save Movie",
            font=("Arial", 16),
            bg="#3e3e3e",
            fg="#e5c07b",
            activebackground="#4b4b4b",
            activeforeground="#e5c07b",
            command=self.save_movie,
        )
        save_button.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", f"Selected Image: {os.path.basename(file_path)}")

    def save_movie(self):
        movie_name = self.movie_entry.get().strip()
        date = self.date_entry.get().strip()
        halls = self.halls_entry.get().strip()
        screen_time = self.screen_time_entry.get().strip()
        image_path = self.image_path

        if not movie_name or not date or not halls or not screen_time or not image_path:
            messagebox.showwarning("Input Error", "Please fill in all fields and upload an image.")
            return

        try:
            halls = int(halls)
            if halls < 1 or halls > 5:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Number of halls must be an integer between 1 and 5.")
            return

        try:
            screen_time = int(screen_time)
            if screen_time <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Screen time must be a positive integer.")
            return

        images_dir = "movie_images"
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        image_filename = f"{movie_name}_{os.path.basename(image_path)}"
        image_destination = os.path.join(images_dir, image_filename)
        try:
            from shutil import copyfile

            copyfile(image_path, image_destination)
        except Exception as e:
            messagebox.showerror("Image Save Error", f"Could not save image: {e}")
            return

        self.cursor.execute(
            """
            INSERT INTO movies (name, date, halls, screen_time, image_path)
            VALUES (?, ?, ?, ?, ?)
            """,
            (movie_name, date, halls, screen_time, image_destination),
        )
        self.conn.commit()

        messagebox.showinfo("Success", "Movie saved successfully!")
        self.main_menu()

    def show_movies(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.content_frame,
            text="Existing Movies",
            font=("Arial", 24, "bold"),
            fg="#e5c07b",
            bg="#1c1c1c",
        )
        title.pack(pady=10)

             # Scrollable Frame
        scroll_canvas = tk.Canvas(self.content_frame, bg="#1c1c1c", highlightthickness=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scroll_frame = tk.Frame(scroll_canvas, bg="#1c1c1c")
        scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="n")

        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        def update_scroll_region(event):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        scroll_frame.bind("<Configure>", update_scroll_region)

        # Fetch and Display Movies
        self.cursor.execute("SELECT id, name, date, halls, screen_time, image_path FROM movies")
        movies = self.cursor.fetchall()
        if movies:
            for movie in movies:
                movie_container = tk.Frame(scroll_frame, bg="#1c1c1c")
                movie_container.pack(pady=10)

                try:
                    image = Image.open(movie[5])
                    image = image.resize((250, 200), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    image_label = tk.Label(movie_container, image=photo, bg="#1c1c1c")
                    image_label.image = photo
                    image_label.pack()

                except Exception as e:
                    error_label = tk.Label(
                        movie_container,
                        text=f"Image not available for {movie[1]}",
                        font=("Arial", 12),
                        fg="red",
                        bg="#1c1c1c",
                    )
                    error_label.pack()

                details = (
                    f"Name: {movie[1]}\nDate: {movie[2]}\nHalls: {movie[3]}\nScreen Time: {movie[4]} hours"
                )
                details_label = tk.Label(movie_container, text=details, font=("Arial", 14), fg="#e5c07b", bg="#1c1c1c")
                details_label.pack(pady=5)

                delete_button = tk.Button(
                    movie_container,
                    text="Delete",
                    font=("Arial", 12),
                    bg="#ff4d4d",
                    fg="white",
                    activebackground="#ff6666",
                    activeforeground="white",
                    command=lambda movie_id=movie[0]: self.delete_movie(movie_id),
                )
                delete_button.pack(pady=5)

                separator = tk.Frame(movie_container, bg="white", height=1, width=500)
                separator.pack(pady=10)

        
        else:
            no_movies_label = tk.Label(
                scroll_frame,
                text="No movies available.",
                font=("Arial", 16),
                fg="#e5c07b",
                bg="#1c1c1c",
            )
            no_movies_label.pack(pady=10)

    def delete_movie(self, movie_id):
        confirmation = messagebox.askyesno("Delete Movie", "Are you sure you want to delete this movie?")
        if confirmation:
            self.cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Movie deleted successfully!")
            self.show_movies()

    def show_halls(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Halls(self.content_frame)

    def show_reports(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        FinancialReport(self.content_frame)

    def show_cctv(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        CCTVControlRoom(self.content_frame)

    def exit_app(self):
        self.conn.close()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = CinemaApp(root)
    root.mainloop()
