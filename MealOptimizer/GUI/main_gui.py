from datetime import datetime
import customtkinter as ctk
import os
from PIL import Image
import pandas as pd
from datetime import date
from tkinter import filedialog, messagebox
from MealOptimizer.Experiments import Experiment
from MealOptimizer.Problems import MinimizeWasteProblem, ParametersProblem
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver
import traceback


from MealOptimizer.GUI.results_frame import ResultsFrame
from MealOptimizer.GUI.home_frame import HomeFrame
from MealOptimizer.GUI.upload_frame import UploadFrame
from MealOptimizer.GUI.settings_frame import SettingsFrame


class MealPlannerGUI(ctk.CTk):
    def __init__(self, recipes_path=None):
        super().__init__()
        self.recipes_path = recipes_path

        self.title("Meal Planner Optimization System")
        self.geometry("1100x700")  # Increased window size

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_navigation_frame()
        self.home_frame = HomeFrame(self)
        self.upload_frame = UploadFrame(self)
        self.settings_frame = SettingsFrame(self)
        self.results_frame = ResultsFrame(self)

        self.select_frame_by_name("home")

    def create_navigation_frame(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Meal Planner",
                                                   compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.upload_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Upload Products",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           anchor="w", command=self.upload_button_event)
        self.upload_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.results_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Results",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.results_button_event)
        self.results_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.upload_button.configure(fg_color=("gray75", "gray25") if name == "upload" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        self.results_button.configure(fg_color=("gray75", "gray25") if name == "results" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "upload":
            self.upload_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.upload_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
        if name == "results":
            self.results_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.results_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def upload_button_event(self):
        self.select_frame_by_name("upload")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def results_button_event(self):
        self.select_frame_by_name("results")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def run_optimization(self):
        selected_solvers = []
        if self.settings_frame.greedy_var.get():
            selected_solvers.append(GreedySolver())
        if self.settings_frame.sa_var.get():
            selected_solvers.append(SimulatedAnnealingSolver())
        if self.settings_frame.graph_var.get():
            selected_solvers.append(PlanningGraphSolver())
        if self.settings_frame.rl_var.get():
            selected_solvers.append(RLSolver())

        if not selected_solvers:
            messagebox.showerror("Error", "Please select at least one algorithm")
            return

        try:
            start_date = datetime.strptime(self.settings_frame.start_date_var.get(), "%Y-%m-%d").date()
            number_of_days = int(self.settings_frame.days_var.get())
            meals_per_day = int(self.settings_frame.meals_var.get())
            requested_amount = number_of_days * meals_per_day
            parameters_to_maximize = []

            # Determine which problem to use
            if self.settings_frame.problem_var.get() == "Minimize Waste":
                problem = MinimizeWasteProblem
            else:  # Maximize Parameters
                if self.settings_frame.num_steps_var.get():
                    parameters_to_maximize.append("Number of Steps")
                if self.settings_frame.prep_time_var.get():
                    parameters_to_maximize.append("Preparation Time (min)")
                if self.settings_frame.num_products_var.get():
                    parameters_to_maximize.append("Number of Products")

                problem = ParametersProblem


            products_pd =  pd.DataFrame(self.upload_frame.product_list.products,
                         columns=["ID", "Product Name", "Quantity", "Date"])
            recipes_path = self.settings_frame.recipes_path_var.get()
            recipes_df = pd.read_csv(recipes_path)


            # Create Experiment instance
            experiment = Experiment(
                problem,
                selected_solvers,
                start_date,
                products_pd,  # piece_dataset
                recipes_df,  # action_dataset
                number_of_days=number_of_days,
                meals_per_day=meals_per_day,
                parameters_to_maximize=parameters_to_maximize
            )

            results = experiment.run()
            self.results_frame.display_results(results, number_of_days, experiment.problem)
            self.select_frame_by_name("results")
        except Exception as e:
            error_message = f"An error occurred during optimization:\n{str(e)}\n\nStacktrace:\n{traceback.format_exc()}"
            print(error_message)  # Print to console for debugging
            messagebox.showerror("Error", error_message)

    def create_temp_csv_files(self):
        # Create temporary products CSV
        products_df = pd.DataFrame(self.upload_frame.product_list.products,
                                   columns=["ID", "Product Name", "Quantity", "Date"])
        products_df.to_csv("temp_products.csv", index=False)

        # Use the selected recipes CSV
        recipes_path = self.settings_frame.recipes_path_var.get()
        if not recipes_path:
            messagebox.showerror("Error", "No recipes CSV selected. Please select a recipes CSV file.")
            return False

        try:
            recipes_df = pd.read_csv(recipes_path)
            recipes_df.to_csv("temp_recipes.csv", index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read recipes CSV: {str(e)}")
            return False

        return True

    def download_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.results_frame.results_text.get("1.0", ctk.END))
            messagebox.showinfo("Information", f"Results saved to {file_path}")


if __name__ == "__main__":
    app = MealPlannerGUI()
    app.mainloop()
