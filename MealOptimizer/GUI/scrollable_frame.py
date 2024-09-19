import customtkinter as ctk


class ScrollableProductFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.products = []
        self.entries = []

    def add_product(self, id, product, quantity, unit, date):
        label = ctk.CTkLabel(self, text=f"ID: {id} - {product} - {quantity} {unit} - Date: {date}", anchor="w")
        label.grid(row=len(self.products), column=0, pady=(0, 5), sticky="w")
        self.products.append((id, product, quantity, unit, date))
        self.entries.append(label)

    def clear_products(self):
        for entry in self.entries:
            entry.destroy()
        self.products = []
        self.entries = []