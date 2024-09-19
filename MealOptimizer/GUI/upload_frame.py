import customtkinter as ctk
import os
from PIL import Image
import pandas as pd
from datetime import date
from tkinter import filedialog, messagebox
from scrollable_frame import ScrollableProductFrame
import random
import string


def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class UploadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)  # Make the product list expandable

        self.create_manual_input()
        self.create_csv_upload()
        self.create_product_list()

    def create_manual_input(self):
        manual_label = ctk.CTkLabel(self, text="Add Products Manually", font=ctk.CTkFont(size=16, weight="bold"))
        manual_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.product_var = ctk.StringVar()
        self.quantity_var = ctk.StringVar()
        self.unit_var = ctk.StringVar()
        self.date_var = ctk.StringVar()

        ctk.CTkLabel(input_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        self.product_entry = ctk.CTkEntry(input_frame, textvariable=self.product_var)
        self.product_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Quantity:").grid(row=0, column=1, padx=5, pady=5)
        self.quantity_entry = ctk.CTkEntry(input_frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Unit:").grid(row=0, column=2, padx=5, pady=5)
        self.unit_entry = ctk.CTkEntry(input_frame, textvariable=self.unit_var)
        self.unit_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=3, padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(input_frame, textvariable=self.date_var)
        self.date_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        self.add_product_button = ctk.CTkButton(input_frame, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=2, column=0, columnspan=4, padx=20, pady=10)

    def create_csv_upload(self):
        csv_label = ctk.CTkLabel(self, text="Upload Products from CSV", font=ctk.CTkFont(size=16, weight="bold"))
        csv_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")

        csv_description = ctk.CTkLabel(self, text="Upload a CSV file with columns: ID, Product Name, Quantity, Unit, Date", wraplength=400)
        csv_description.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        csv_frame = ctk.CTkFrame(self)
        csv_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        csv_frame.grid_columnconfigure(0, weight=1)

        self.csv_path_var = ctk.StringVar()
        self.csv_path_entry = ctk.CTkEntry(csv_frame, textvariable=self.csv_path_var)
        self.csv_path_entry.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.csv_browse_button = ctk.CTkButton(csv_frame, text="Browse", command=self.browse_csv)
        self.csv_browse_button.grid(row=0, column=1, padx=(0, 20), pady=10)

        self.csv_upload_button = ctk.CTkButton(csv_frame, text="Upload CSV", command=self.upload_csv)
        self.csv_upload_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

    def create_product_list(self):
        list_label = ctk.CTkLabel(self, text="Added Products", font=ctk.CTkFont(size=16, weight="bold"))
        list_label.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="w")

        self.product_list = ScrollableProductFrame(self, width=500, height=200)
        self.product_list.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")

    def add_product(self):
        product = self.product_var.get()
        quantity = self.quantity_var.get()
        unit = self.unit_var.get()
        date = self.date_var.get()

        if product and quantity and unit and date:
            try:
                # Convert quantity to float to ensure it's a number
                float(quantity)
                id = generate_random_id()
                self.product_list.add_product(id, product, quantity, unit, date)
                self.product_var.set("")
                self.quantity_var.set("")
                self.unit_var.set("")
                self.date_var.set("")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_path_var.set(file_path)

    def upload_csv(self):
        csv_path = self.csv_path_var.get()
        if not csv_path:
            messagebox.showerror("Error", "Please select a CSV file")
            return

        try:
            df = pd.read_csv(csv_path)
            required_columns = ["ID", "Product Name", "Quantity", "Unit", "Date"]
            if not all(col in df.columns for col in required_columns):
                raise ValueError("CSV file must contain columns: ID, Product Name, Quantity, Unit, Date")

            for _, row in df.iterrows():
                self.product_list.add_product(row["ID"], row["Product Name"], row["Quantity"], row["Unit"], row["Date"])

            messagebox.showinfo("Success", f"Added {len(df)} products from CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload CSV: {str(e)}")