from MealOptimizer.Experiments import Experiment
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver
from datetime import date
from MealOptimizer.GUI.main_gui import MealPlannerGUI
import pandas as pd


def main_cmd():
    problem = Problems.CountExpiredItemsProblem
    solvers = [GreedySolver(), SimulatedAnnealingSolver(), PlanningGraphSolver(), RLSolver()]
    products_data_path = "MealOptimizer/Datasets/products_dataset/known_400.csv"  # insert path
    recipes_data_path = "MealOptimizer/Datasets/recipes_smaller.csv"  # insert path
    start_date = date(2024, 9, 1)
    experiment = Experiment(problem, solvers, start_date, pd.read_csv(products_data_path), pd.read_csv(recipes_data_path),
                            number_of_days=12,
                            meals_per_day=1)
    results = experiment.run()
    for solver, state in results.items():
        print(f"{solver} reached the end state with solution:\n {state}")


def main():
    recipe_data_path = "recipes.csv"
    gui = MealPlannerGUI(recipe_data_path)
    gui.mainloop()


if __name__ == "__main__":
    main_cmd()
