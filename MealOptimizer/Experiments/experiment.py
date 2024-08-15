from abc import ABC, abstractmethod
from typing import List
import time
from ..Problems.problem import Problem
from ..Solvers.solver import Solver
from ..Metrics.visualization import VisualizationComparison, PerformanceMetrics


class Experiment(ABC):
    def __init__(self, datasets: List[str], problem: Problem, solvers: List[Solver]):
        self.problem = problem
        self.solvers = solvers
        self.visualization = VisualizationComparison()
        self.datasets = datasets

    @abstractmethod
    def run(self):
        pass

    def visualize_results(self):
        self.visualization.plot_runtime_comparison()
        self.visualization.plot_iterations_comparison()
        for kpi in self.problem.get_kpis():
            self.visualization.plot_kpi_comparison(kpi)

        comparison_table = self.visualization.generate_comparison_table()
        print("Comparison Table:")
        print(comparison_table)


class MealPlanningExperiment(Experiment):
    def run(self):
        for solver in self.solvers:
            for dataset in self.datasets:
                self.problem.load_data(dataset)
                dataset_size = len(self.problem.get_state())
                start_time = time.time()
                solution = solver.solve(self.problem)
                end_time = time.time()

                runtime = end_time - start_time
                iterations = solver.get_iterations()
                self.problem.apply_solution(solution)
                kpis = self.problem.evaluate_solution()

                metrics = PerformanceMetrics(dataset_size, runtime, iterations, kpis)
                self.visualization.add_solver_performance(solver.__class__.__name__, metrics)
