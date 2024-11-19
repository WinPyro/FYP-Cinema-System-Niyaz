import tkinter as tk
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
import os


class CCTVControlRoom:
    def __init__(self, parent):
        self.parent = parent

        # Frame for CCTV controls
        self.cctv_frame = tk.Frame(self.parent, bg="#1c1c1c")
        self.cctv_frame.pack(expand=True, fill="both")

        title = tk.Label(self.cctv_frame, text="CCTV Control Room", font=("Arial", 24, "bold"), fg="#e5c07b", bg="#1c1c1c")
        title.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.cctv_frame, bg="#1c1c1c")
        button_frame.pack(pady=20)

        # Camera Buttons
        self.camera_buttons = [
            {"name": "Camera 1", "image": "Hall1.png"},
            {"name": "Camera 2", "image": "Hall2.png"},
            {"name": "Camera 3", "image": "Hall3.png"},
            {"name": "Camera 4", "image": "Hall4.png"},
            {"name": "Camera 5", "image": "Hall5.png"},
            {"name": "Camera Toilet", "image": "Toilet.png"},
            {"name": "Camera Main Hall", "image": "MainHall.png"},
            {"name": "Camera Food Area", "image": "foodPlace.png"},
            {"name": "View All Cameras", "image": "Allzcctv.png"}
        ]

        # Create two columns of buttons
        column1 = tk.Frame(button_frame, bg="#1c1c1c")
        column1.pack(side="left", padx=20)

        column2 = tk.Frame(button_frame, bg="#1c1c1c")
        column2.pack(side="left", padx=20)

        # Assign buttons to respective columns
        for idx, camera in enumerate(self.camera_buttons):
            frame = column1 if idx < 5 else column2
            btn = Button(frame, text=camera["name"], font=("Arial", 14), width=20, height=2,
                         bg="#3e3e3e", fg="#e5c07b", activebackground="#4b4b4b", activeforeground="#e5c07b",
                         command=lambda c=camera: self.open_camera_window(c["name"], c["image"]))
            btn.pack(pady=5)

        # Back button
        back_button = Button(self.cctv_frame, text="Back to Main Menu", font=("Arial", 14), bg="#3e3e3e", fg="#e5c07b",
                             activebackground="#4b4b4b", activeforeground="#e5c07b", command=self.back_to_main_menu)
        back_button.pack(pady=20)

    def open_camera_window(self, camera_name, image_file):
        # Open a new window to display the camera view
        new_window = Toplevel(self.parent)
        new_window.title(camera_name)
        new_window.geometry("800x600")
        new_window.configure(bg="#1c1c1c")

        # Load and display the image
        try:
            img_path = os.path.join("Images", image_file)
            image = Image.open(img_path)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)  # Use LANCZOS for resampling
            photo = ImageTk.PhotoImage(image)
            img_label = Label(new_window, image=photo, bg="#1c1c1c")
            img_label.image = photo
            img_label.pack(pady=20)
        except Exception as e:
            error_label = Label(new_window, text=f"Error loading image: {e}", font=("Arial", 14),
                                fg="red", bg="#1c1c1c")
            error_label.pack(pady=20)

        # Back Button
        back_button = Button(new_window, text="Back", font=("Arial", 14), width=15, height=2,
                             bg="#3e3e3e", fg="#e5c07b", activebackground="#4b4b4b", activeforeground="#e5c07b",
                             command=new_window.destroy)
        back_button.pack(pady=20)

    def back_to_main_menu(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        CinemaApp(self.parent)  # Reinitialize the main menu
