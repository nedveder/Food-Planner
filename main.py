from MealOptimizer import Problems
from MealOptimizer.Experiments import MealPlanningExperiment
from MealOptimizer.Solvers import RandomizedSolver, RLSolver, PlanningGraphSolver


def main():
    problem = Problems.MealPlanningProblem()
    solvers = [RandomizedSolver(), RLSolver(), PlanningGraphSolver()]
    datasets = ["Datasets/dataset1.csv", "Datasets/dataset2.csv"]
    experiment = MealPlanningExperiment(datasets,problem, solvers)
    experiment.run()
    experiment.visualize_results()


if __name__ == "__main__":
    main()
