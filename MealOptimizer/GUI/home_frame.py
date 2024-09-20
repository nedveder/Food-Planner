import customtkinter as ctk
from PIL import Image, ImageTk  # Required to handle images

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Ensuring the row will expand to fill the frame

        # Load the image
        self.original_image = Image.open("MealOptimizer/welcome_pic.png")  # Replace with your image file
        self.bg_image_tk = None  # This will hold the resized image

        # Create a canvas to hold the image
        self.canvas = ctk.CTkCanvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")  # Span the entire frame

        # Bind the resize event to resize the image dynamically
        self.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        # Get the current size of the frame
        frame_width = self.winfo_width()
        frame_height = self.winfo_height()

        # Resize the image to fit the frame
        resized_image = self.original_image.resize((frame_width, frame_height), Image.ANTIALIAS)
        self.bg_image_tk = ImageTk.PhotoImage(resized_image)

        # Update the canvas with the resized image
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")