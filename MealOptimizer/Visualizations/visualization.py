import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from typing import List, Dict, Tuple
from datetime import date, timedelta

from MealOptimizer.Experiments import Experiment
from MealOptimizer.Problems import MinimizeWasteProblem, CountExpiredItemsProblem, ParametersProblem
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver,  RLSolver


class MealOptimizationVisualizer:
    def __init__(self, output_dir: str = 'visualizations'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_comparison(self, results: Dict[str, Dict[str, Dict[str, List[Tuple[float, float]]]]], metric: str):
        problem_types = list(results.keys())
        param_sets = list(results[problem_types[0]].keys())
        solvers = list(results[problem_types[0]][param_sets[0]].keys())

        fig, axs = plt.subplots(len(problem_types), 1, figsize=(15, 6 * len(problem_types)), sharex=True)
        if len(problem_types) == 1:
            axs = [axs]

        x = np.arange(len(solvers))
        width = 0.8 / len(param_sets)

        for prob_idx, problem_type in enumerate(problem_types):
            for i, param_set in enumerate(param_sets):
                if metric == 'time':
                    values = [np.mean([r[0] for r in results[problem_type][param_set][solver]]) for solver in solvers]
                    ylabel = 'Average Execution Time (seconds)'
                elif metric == 'score':
                    values = [np.mean([r[1] for r in results[problem_type][param_set][solver]]) for solver in solvers]
                    ylabel = 'Average Score'
                else:
                    raise ValueError("Invalid metric. Choose 'time' or 'score'.")

                axs[prob_idx].bar(x + i * width, values, width, label=f'Param Set {i + 1}')

            axs[prob_idx].set_ylabel(ylabel)
            axs[prob_idx].set_title(f'{problem_type} - {metric.capitalize()} Performance')
            axs[prob_idx].set_xticks(x + width * (len(param_sets) - 1) / 2)
            axs[prob_idx].set_xticklabels(solvers, rotation=45, ha='right')
            axs[prob_idx].legend()

        plt.tight_layout()
        filename = f'{metric}_performance_comparison_by_problem.png'
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
        return filename

    def plot_overall_comparison(self, results: Dict[str, Dict[str, Dict[str, List[Tuple[float, float]]]]], metric: str):
        problem_types = list(results.keys())
        param_sets = list(results[problem_types[0]].keys())
        solvers = list(results[problem_types[0]][param_sets[0]].keys())

        fig, ax = plt.subplots(figsize=(15, 8))

        x = np.arange(len(solvers))
        width = 0.8 / (len(problem_types) * len(param_sets))

        for prob_idx, problem_type in enumerate(problem_types):
            for i, param_set in enumerate(param_sets):
                if metric == 'time':
                    values = [np.mean([r[0] for r in results[problem_type][param_set][solver]]) for solver in solvers]
                    ylabel = 'Average Execution Time (seconds)'
                elif metric == 'score':
                    values = [np.mean([r[1] for r in results[problem_type][param_set][solver]]) for solver in solvers]
                    ylabel = 'Average Score'
                else:
                    raise ValueError("Invalid metric. Choose 'time' or 'score'.")

                offset = prob_idx * len(param_sets) + i
                ax.bar(x + offset * width, values, width, label=f'{problem_type} - Param Set {i + 1}')

        ax.set_ylabel(ylabel)
        ax.set_title(f'Overall {metric.capitalize()} Performance Comparison')
        ax.set_xticks(x + width * (len(problem_types) * len(param_sets) - 1) / 2)
        ax.set_xticklabels(solvers, rotation=45, ha='right')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        filename = f'{metric}_overall_performance_comparison.png'
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
        return filename


def run_experiments(problem_classes, products_data_path: str, recipes_data_path: str,
                    parameter_sets: List[Dict], num_runs: int = 10):
    solvers = [GreedySolver(), SimulatedAnnealingSolver(),  RLSolver()]
    results = {problem.__name__: {} for problem in problem_classes}

    products_df = pd.read_csv(products_data_path)
    recipes_df = pd.read_csv(recipes_data_path)

    for problem_class in problem_classes:
        for i, params in enumerate(parameter_sets):
            results[problem_class.__name__][f'Set_{i + 1}'] = {solver.__class__.__name__: [] for solver in solvers}

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
                if problem_class.__name__ == "ParametersProblem":
                    problem_instance = problem_class(
                        recipes_df,
                        params['start_date'],
                        products_df[["Product Name", "Date"]],
                        number_of_days=params['num_days'],
                        meals_per_day=params['meals_per_day'],
                        parameters_to_maximize=params.get('parameters_to_maximize')
                    )
                elif problem_class.__name__ == "MinimizeWasteProblem":
                    problem_instance = problem_class(
                        recipes_df,
                        params['start_date'],
                        products_df[["Product Name", "Date"]],
                        number_of_days=params['num_days'],
                        meals_per_day=params['meals_per_day']
                    )
                else:
                    problem_instance = problem_class(
                        recipes_df,
                        params['start_date'],
                        products_df[["Product Name", "Date"]],
                        number_of_days=params['num_days'],
                        meals_per_day=params['meals_per_day']
                    )

                for solver, (final_state, time) in run_results.items():
                    score = problem_instance.get_score(final_state) if final_state else 0
                    results[problem_class.__name__][f'Set_{i + 1}'][solver.__class__.__name__].append((time, score))

    return results


def visualize_results(results: Dict[str, Dict[str, Dict[str, List[Tuple[float, float]]]]]):
    visualizer = MealOptimizationVisualizer()

    time_plot = visualizer.plot_comparison(results, 'time')
    score_plot = visualizer.plot_comparison(results, 'score')

    overall_time_plot = visualizer.plot_overall_comparison(results, 'time')
    overall_score_plot = visualizer.plot_overall_comparison(results, 'score')

    print(f"Time performance plot by problem: {time_plot}")
    print(f"Score performance plot by problem: {score_plot}")
    print(f"Overall time performance plot: {overall_time_plot}")
    print(f"Overall score performance plot: {overall_score_plot}")


# Example usage
if __name__ == "__main__":
    problem_classes = [MinimizeWasteProblem, CountExpiredItemsProblem, ParametersProblem]
    products_data_path = r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\non optimality of greedy\products.csv"
    recipes_data_path = r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\non optimality of greedy\recipes.csv"

    parameter_sets = [
        {
            'start_date': date(2024, 9, 1),
            'num_days': 12,
            'meals_per_day': 1,
            'parameters_to_maximize': ["Shelf Time"]
        },

        {
            'start_date': date(2024, 9, 1),
            'num_days': 5,
            'meals_per_day': 2,
            'parameters_to_maximize': ["Preparation Time (min)", "Taste Rating"]
        },
        {
            'start_date': date(2024, 9, 1),
            'num_days': 3,
            'meals_per_day': 3,
            'parameters_to_maximize': ["Preparation Time (min)"]
        },
        {
            'start_date': date(2024, 9, 1),
            'num_days': 1,
            'meals_per_day': 12,
            'parameters_to_maximize': ["Shelf Time", "Taste Rating"]
        },
        {
            'start_date': date(2024, 9, 1),
            'num_days': 11,
            'meals_per_day': 1,
            'parameters_to_maximize': ["Number of Steps", "Shelf Time"]
        }
    ]

    try:
        results = run_experiments(problem_classes, products_data_path, recipes_data_path, parameter_sets)
        visualize_results(results)
    except Exception as e:
        print(f"An error occurred: {e}")