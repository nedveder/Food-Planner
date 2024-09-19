import customtkinter as ctk
import os
from PIL import Image
import pandas as pd
from datetime import date
from tkinter import filedialog, messagebox
from MealOptimizer.Experiments import Experiment
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver


class ResultsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.results_text = ctk.CTkTextbox(self, width=600, height=400)
        self.results_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.download_button = ctk.CTkButton(self, text="Download Results", command=self.download_results)
        self.download_button.grid(row=1, column=0, padx=20, pady=20)

    def display_results(self, results):
        self.results_text.delete("1.0", ctk.END)
        for solver, state in results.items():
            self.results_text.insert(ctk.END, f"{solver.__class__.__name__} Results:\n")
            self.results_text.insert(ctk.END, f"{state}\n\n")

    def download_results(self):
        self.master.download_results()
