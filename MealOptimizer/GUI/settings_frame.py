import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import date, timedelta

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.create_planning_options()
        self.create_problem_selection()
        self.create_algorithm_options()
        self.create_recipes_options()

        self.run_button = ctk.CTkButton(self, text="Run Optimization", command=self.run_optimization)
        self.run_button.grid(row=9, column=0, padx=20, pady=20)

    def create_planning_options(self):
        planning_label = ctk.CTkLabel(self, text="Meal Planning Options", font=ctk.CTkFont(size=16, weight="bold"))
        planning_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        planning_frame = ctk.CTkFrame(self)
        planning_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        planning_frame.grid_columnconfigure((0, 1), weight=1)

        # Start Date
        start_date_label = ctk.CTkLabel(planning_frame, text="Start Date (YYYY-MM-DD):")
        start_date_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_date_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.start_date_entry = ctk.CTkEntry(planning_frame, textvariable=self.start_date_var, width=100)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Number of days
        days_label = ctk.CTkLabel(planning_frame, text="Number of Days:")
        days_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.days_var = ctk.StringVar(value="7")
        self.days_entry = ctk.CTkEntry(planning_frame, textvariable=self.days_var, width=50)
        self.days_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Meals per day
        meals_label = ctk.CTkLabel(planning_frame, text="Meals per Day:")
        meals_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.meals_var = ctk.StringVar(value="3")
        self.meals_entry = ctk.CTkEntry(planning_frame, textvariable=self.meals_var, width=50)
        self.meals_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    def create_problem_selection(self):
        problem_label = ctk.CTkLabel(self, text="Optimization Problem", font=ctk.CTkFont(size=16, weight="bold"))
        problem_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")

        self.problem_var = ctk.StringVar(value="Minimize Waste")
        self.problem_dropdown = ctk.CTkOptionMenu(
            self,
            values=["Minimize Waste", "Maximize Parameters"],
            variable=self.problem_var,
            command=self.toggle_parameter_options
        )
        self.problem_dropdown.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.parameter_frame = ctk.CTkFrame(self)
        self.parameter_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.parameter_frame.grid_columnconfigure((0, 1), weight=1)

        self.prep_time_var = ctk.BooleanVar(value=False)
        self.taste_rating_var = ctk.BooleanVar(value=False)
        self.shelf_time_var = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(self.parameter_frame, text="Preparation Time", variable=self.prep_time_var).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(self.parameter_frame, text="Taste Rating", variable=self.taste_rating_var).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(self.parameter_frame, text="Shelf Time", variable=self.shelf_time_var).grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.parameter_frame.grid_remove()  # Hide initially

    def toggle_parameter_options(self, _):
        if self.problem_var.get() == "Maximize Parameters":
            self.parameter_frame.grid()
        else:
            self.parameter_frame.grid_remove()

    def create_algorithm_options(self):
        algorithm_label = ctk.CTkLabel(self, text="Optimization Algorithms", font=ctk.CTkFont(size=16, weight="bold"))
        algorithm_label.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="w")

        self.algorithm_frame = ctk.CTkFrame(self)
        self.algorithm_frame.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        self.algorithm_frame.grid_columnconfigure((0, 1), weight=1)

        self.greedy_var = ctk.BooleanVar(value=True)
        self.sa_var = ctk.BooleanVar(value=True)
        self.graph_var = ctk.BooleanVar(value=True)
        self.rl_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.algorithm_frame, text="Greedy", variable=self.greedy_var).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkCheckBox(self.algorithm_frame, text="Simulated Annealing", variable=self.sa_var).grid(row=0, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkCheckBox(self.algorithm_frame, text="Planning Graph", variable=self.graph_var).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkCheckBox(self.algorithm_frame, text="Reinforcement Learning", variable=self.rl_var).grid(row=1, column=1, padx=20, pady=10, sticky="w")

    def create_recipes_options(self):
        recipes_label = ctk.CTkLabel(self, text="Recipes Data", font=ctk.CTkFont(size=16, weight="bold"))
        recipes_label.grid(row=7, column=0, padx=20, pady=(20, 10), sticky="w")

        self.recipes_frame = ctk.CTkFrame(self)
        self.recipes_frame.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
        self.recipes_frame.grid_columnconfigure(0, weight=1)

        self.recipes_path_var = ctk.StringVar()
        self.recipes_path_entry = ctk.CTkEntry(self.recipes_frame, textvariable=self.recipes_path_var)
        self.recipes_path_entry.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.recipes_browse_button = ctk.CTkButton(self.recipes_frame, text="Browse", command=self.browse_recipes_csv)
        self.recipes_browse_button.grid(row=0, column=1, padx=(0, 20), pady=10)

    def browse_recipes_csv(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.recipes_path_var.set(file_path)

    def run_optimization(self):
        self.master.run_optimization()