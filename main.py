from MealOptimizer.Experiments import Experiment
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver
from datetime import date
from MealOptimizer.GUI.main_gui import MealPlannerGUI


def main_cmd():
    problem = Problems.MinimizeWasteProblem
    solvers = [GreedySolver(), SimulatedAnnealingSolver(), PlanningGraphSolver(), RLSolver()]
    products_data_path = "/Users/nadavlederman/Desktop/Projects/Food-Planner/Datasets/smaller_products_data.csv"
    recipes_data_path = "/Users/nadavlederman/Desktop/Projects/Food-Planner/Datasets/new_recipes.csv"
    start_date = date(2024, 9, 1)
    experiment = Experiment(problem, solvers, start_date, products_data_path, recipes_data_path, number_of_days=5)
    results = experiment.run()
    for solver, state in results.items():
        print(f"{solver} reached the goal state with solution:\n {state}")

def main():
    gui = MealPlannerGUI()
    gui.mainloop()

if __name__ == "__main__":
    main()
