import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Meal Planner Optimization System",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.description = ctk.CTkLabel(self, text="Welcome to the Meal Planner Optimization System!\n\n"
                                                   "This application helps you create efficient meal plans based on "
                                                   "your available ingredients "
                                                   "and preferred optimization criteria. You can choose from various "
                                                   "algorithms to find the "
                                                   "best meal plans that minimize waste or maximize nutritional "
                                                   "value.\n\n "
                                                   "To get started, please proceed to the 'Upload Products' tab to "
                                                   "input your available ingredients.",
                                        wraplength=500, justify="left")
        self.description.grid(row=1, column=0, padx=20, pady=10)
