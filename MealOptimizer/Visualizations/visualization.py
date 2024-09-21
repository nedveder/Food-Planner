import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from typing import List, Dict, Tuple
from datetime import date

from MealOptimizer.Experiments import Experiment
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver
from MealOptimizer.Problems.problem import Problem
from MealOptimizer.Problems.state import State


class MealOptimizationVisualizer:
    def __init__(self, output_dir: str = 'visualizations'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_comparison(self, results: Dict[str, Dict[str, List[Tuple[float, float, float]]]], metric: str):
        plt.figure(figsize=(15, 8))

        solvers = list(next(iter(results.values())).keys())
        param_sets = list(results.keys())
        x = np.arange(len(solvers))
        width = 0.8 / len(param_sets)

        for i, param_set in enumerate(param_sets):
            if metric == 'time':
                values = [np.mean([r[0] for r in results[param_set][solver]]) for solver in solvers]
                ylabel = 'Average Execution Time (seconds)'
            elif metric == 'score':
                values = [np.mean([r[1] for r in results[param_set][solver]]) for solver in solvers]
                ylabel = 'Average Score'
            elif metric == 'success':
                values = [np.mean([r[2] for r in results[param_set][solver]]) for solver in solvers]
                ylabel = 'Success Rate'
            else:
                raise ValueError("Invalid metric. Choose 'time', 'score', or 'success'.")

            plt.bar(x + i * width, values, width, label=f'Param Set {i + 1}')

        plt.xlabel('Solvers')
        plt.ylabel(ylabel)
        plt.title(f'{metric.capitalize()} Performance Comparison')
        plt.xticks(x + width * (len(param_sets) - 1) / 2, solvers, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()

        filename = f'{metric}_performance_comparison.png'
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
        return filename


def run_experiments(problem_class, products_data_path: str, recipes_data_path: str,
                    parameter_sets: List[Dict], num_runs: int = 2):
    solvers = [GreedySolver(), SimulatedAnnealingSolver(), PlanningGraphSolver(), RLSolver()]
    results = {}

    products_df = pd.read_csv(products_data_path)
    recipes_df = pd.read_csv(recipes_data_path)

    for i, params in enumerate(parameter_sets):
        results[f'Set_{i + 1}'] = {solver.__class__.__name__: [] for solver in solvers}

        for _ in range(num_runs):
            experiment = Experiment(
                problem_class,
                solvers,
                params['start_date'],
                products_df,
                recipes_df,
                number_of_days=params['num_days'],
                meals_per_day=params['meals_per_day'],
                parameters=params.get('parameters_to_maximize')
            )
            run_results = experiment.run()

            problem_instance = problem_class(
                recipes_df,
                params['start_date'],
                products_df[["Product Name", "Date"]],
                number_of_days=params['num_days'],
                meals_per_day=params['meals_per_day']
            )

            for solver, (final_state, time) in run_results.items():
                score = problem_instance.get_score(final_state) if final_state else 0
                success = problem_instance.is_goal_state(final_state) if final_state else False
                results[f'Set_{i + 1}'][solver.__class__.__name__].append((time, score, int(success)))

    return results


def visualize_results(results: Dict[str, Dict[str, List[Tuple[float, float, float]]]]):
    visualizer = MealOptimizationVisualizer()

    time_plot = visualizer.plot_comparison(results, 'time')
    score_plot = visualizer.plot_comparison(results, 'score')
    success_plot = visualizer.plot_comparison(results, 'success')

    print(f"Time performance plot: {time_plot}")
    print(f"Score performance plot: {score_plot}")
    print(f"Success rate plot: {success_plot}")


# Example usage
if __name__ == "__main__":
    problem_class = Problems.MinimizeWasteProblem
    products_data_path = r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\non optimality of greedy\products.csv"
    recipes_data_path = r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\non optimality of greedy\recipes.csv"

    parameter_sets = [
        {
            'start_date': date(2024, 9, 1),
            'num_days': 12,
            'meals_per_day': 1,
            'parameters_to_maximize': []
        },

        {
            'start_date': date(2024, 9, 1),
            'num_days': 5,
            'meals_per_day': 2,
            'parameters_to_maximize': []
        },
        {
            'start_date': date(2024, 9, 1),
            'num_days': 1,
            'meals_per_day': 12,
            'parameters_to_maximize': []
        },
        {
            'start_date': date(2024, 9, 1),
            'num_days': 11,
            'meals_per_day': 1,
            'parameters_to_maximize': []
        }
    ]

    try:
        results = run_experiments(problem_class, products_data_path, recipes_data_path, parameter_sets)
        visualize_results(results)
    except Exception as e:
        print(f"An error occurred: {e}")