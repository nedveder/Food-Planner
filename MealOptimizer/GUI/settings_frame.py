import customtkinter as ctk
from tkinter import filedialog, messagebox

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.create_planning_options()
        self.create_algorithm_options()
        self.create_recipes_options()

        self.run_button = ctk.CTkButton(self, text="Run Optimization", command=self.run_optimization)
        self.run_button.grid(row=8, column=0, padx=20, pady=20)

    def create_planning_options(self):
        planning_label = ctk.CTkLabel(self, text="Meal Planning Options", font=ctk.CTkFont(size=16, weight="bold"))
        planning_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        planning_frame = ctk.CTkFrame(self)
        planning_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        planning_frame.grid_columnconfigure((0, 1), weight=1)

        # Number of days
        days_label = ctk.CTkLabel(planning_frame, text="Number of Days:")
        days_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.days_var = ctk.StringVar(value="7")  # Change to StringVar
        self.days_entry = ctk.CTkEntry(planning_frame, textvariable=self.days_var, width=50)
        self.days_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Meals per day
        meals_label = ctk.CTkLabel(planning_frame, text="Meals per Day:")
        meals_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.meals_var = ctk.StringVar(value="3")  # Change to StringVar
        self.meals_entry = ctk.CTkEntry(planning_frame, textvariable=self.meals_var, width=50)
        self.meals_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    def create_algorithm_options(self):
        algorithm_label = ctk.CTkLabel(self, text="Optimization Algorithms", font=ctk.CTkFont(size=16, weight="bold"))
        algorithm_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")

        algorithm_description = ctk.CTkLabel(self, text="Select one or more algorithms to use for meal plan optimization:", wraplength=400)
        algorithm_description.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        self.algorithm_frame = ctk.CTkFrame(self)
        self.algorithm_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.algorithm_frame.grid_columnconfigure((0, 1), weight=1)

        self.greedy_var = ctk.BooleanVar(value=True)
        self.sa_var = ctk.BooleanVar(value=True)
        self.graph_var = ctk.BooleanVar(value=True)
        self.rl_var = ctk.BooleanVar(value=True)

        self.greedy_check = ctk.CTkCheckBox(self.algorithm_frame, text="Greedy", variable=self.greedy_var)
        self.greedy_check.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.sa_check = ctk.CTkCheckBox(self.algorithm_frame, text="Simulated Annealing", variable=self.sa_var)
        self.sa_check.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.graph_check = ctk.CTkCheckBox(self.algorithm_frame, text="Planning Graph", variable=self.graph_var)
        self.graph_check.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.rl_check = ctk.CTkCheckBox(self.algorithm_frame, text="Reinforcement Learning", variable=self.rl_var)
        self.rl_check.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    def create_recipes_options(self):
        recipes_label = ctk.CTkLabel(self, text="Recipes Data", font=ctk.CTkFont(size=16, weight="bold"))
        recipes_label.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="w")

        recipes_description = ctk.CTkLabel(self, text="Select a CSV file containing the recipes data:", wraplength=400)
        recipes_description.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="w")

        self.recipes_frame = ctk.CTkFrame(self)
        self.recipes_frame.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        self.recipes_frame.grid_columnconfigure(1, weight=1)

        self.recipes_path_var = ctk.StringVar()
        self.recipes_path_entry = ctk.CTkEntry(self.recipes_frame, textvariable=self.recipes_path_var)
        self.recipes_path_entry.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.recipes_browse_button = ctk.CTkButton(self.recipes_frame, text="Browse", command=self.browse_recipes_csv)
        self.recipes_browse_button.grid(row=0, column=1, padx=20, pady=10)

    def browse_recipes_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.recipes_path_var.set(file_path)

    def run_optimization(self):
        self.master.run_optimization()