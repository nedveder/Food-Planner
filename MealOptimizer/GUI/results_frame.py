import customtkinter as ctk
import os
from PIL import Image
import pandas as pd
from datetime import date
from tkinter import filedialog, messagebox


class ResultsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.results_text = ctk.CTkTextbox(self, width=600, height=400)
        self.results_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.download_button = ctk.CTkButton(self, text="Download Results", command=self.download_results)
        self.download_button.grid(row=1, column=0, padx=20, pady=20)

    def display_results(self, results, number_of_days, meals_per_day, problem):
        self.results_text.delete("1.0", ctk.END)
        for solver, (state, solve_time, score) in results.items():
            self.results_text.insert(ctk.END, f"{solver.__class__.__name__} Results:\n")
            self.results_text.insert(ctk.END, f"Time taken: {solve_time:.2f} seconds\n\n")

            if state is None:
                self.results_text.insert(ctk.END, "No solution found.\n\n")
                continue

            for day in range(number_of_days):
                self.results_text.insert(ctk.END, f"Day {day + 1}:\n")
                day_actions = state.selected_actions[day * meals_per_day:(day + 1) * meals_per_day]
                if not day_actions:
                    self.results_text.insert(ctk.END, "  No meals planned for this day.\n")
                for meal, action in enumerate(day_actions, 1):
                    self.results_text.insert(ctk.END, f"  Meal {meal}: {action.name}\n")
                    self.results_text.insert(ctk.END, f"  Ingredients:\n")
                    for piece in action.pieces:
                        self.results_text.insert(ctk.END, f"    - {piece.item_id}: {piece.quantity}\n")
                    self.results_text.insert(ctk.END, "\n")
                self.results_text.insert(ctk.END, "\n")

            self.results_text.insert(ctk.END, f"Total Score: {score:.2f}\n\n")

    def download_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.results_text.get("1.0", ctk.END))
            messagebox.showinfo("Success", f"Results saved to {file_path}")