from MealOptimizer.Experiments import Experiment
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver


def main():
    problem = Problems.MinimizeWasteProblem
    solvers = [GreedySolver]
    products_data_path = "/Users/nadavlederman/Desktop/Projects/Food-Planner/Datasets/products_data.csv"
    recipes_data_path = "/Users/nadavlederman/Desktop/Projects/Food-Planner/Datasets/recipes_with_product_tuples.csv"
    start_date = "2021-01-01"
    experiment = Experiment(problem, solvers, start_date, products_data_path, recipes_data_path)
    experiment.run()
    experiment.visualize_results()


if __name__ == "__main__":
    main()
