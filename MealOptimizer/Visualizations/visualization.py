import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from MealOptimizer.Experiments import Experiment
from MealOptimizer import Problems
from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver
from datetime import date, timedelta
from itertools import combinations
from MealOptimizer.Problems.state import State
from collections import Counter
import os


class AlgorithmComparisonVisualizer:
    def __init__(self, products_data: pd.DataFrame, recipes_data: pd.DataFrame, output_dir: str = 'visualization_output'):
        self.products_data = products_data
        self.recipes_data = recipes_data
        self.solvers = [
            GreedySolver(),
            SimulatedAnnealingSolver(),
            PlanningGraphSolver(),
            RLSolver()
        ]
        self.problem_types = [
            Problems.MinimizeWasteProblem,
            Problems.ParametersProblem
        ]
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_unique_filename(self, base_name: str) -> str:
        """Generate a unique filename for saving plots."""
        counter = 1
        while True:
            filename = f"{base_name}_{counter}.png"
            if not os.path.exists(os.path.join(self.output_dir, filename)):
                return filename
            counter += 1

    def save_plot(self, base_name: str):
        """Save the current plot with a unique filename."""
        filename = self.get_unique_filename(base_name)
        plt.savefig(os.path.join(self.output_dir, filename), bbox_inches='tight')
        plt.close()
        print(f"Saved plot: {filename}")

    def run_experiments(self, start_date: date, num_days: int, meals_per_day: int,
                        parameters_to_maximize: List[str] = None) -> Dict[str, Dict[str, Tuple[State, float]]]:
        results = {}
        for problem_type in self.problem_types:
            experiment = Experiment(
                problem_type,
                self.solvers,
                start_date,
                self.products_data,
                self.recipes_data,
                number_of_days=num_days,
                meals_per_day=meals_per_day,
                parameters=parameters_to_maximize
            )
            results[problem_type.__name__] = experiment.run()
        return results

    def plot_time_differences(self, results: Dict[str, Dict[str, Tuple[State, float]]]):
        plt.figure(figsize=(12, 6))
        for problem_type, problem_results in results.items():
            times = [result[1] for result in problem_results.values()]
            solver_names = [solver.__class__.__name__ for solver in problem_results.keys()]
            plt.bar(solver_names, times, alpha=0.8, label=problem_type)

        plt.title("Execution Time Comparison")
        plt.xlabel("Solvers")
        plt.ylabel("Time (seconds)")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot("time_differences")

    def compare_results(self, results: Dict[str, Dict[str, Tuple[State, float]]]):
        plt.figure(figsize=(12, 6))
        for problem_type, problem_results in results.items():
            scores = [self.get_score(state) for state, _ in problem_results.values() if state is not None]
            solver_names = [solver.__class__.__name__ for solver in problem_results.keys()]
            plt.bar(solver_names, scores, alpha=0.8, label=problem_type)

        plt.title("Score Comparison")
        plt.xlabel("Solvers")
        plt.ylabel("Score")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot("time_differences")

    def get_score(self, state: State) -> float:
        # Implement this method based on how you calculate the score for a state
        # This is a placeholder implementation
        return sum(action.score for action in state.selected_actions)

    def compare_with_different_inputs(self, start_date: date, num_days_list: List[int], meals_per_day_list: List[int]):
        """
        Creates a scatter plot to visualize how algorithms perform with different inputs
        (number of days and meals per day).
        This plot shows the relationship between execution time and score,
         with additional dimensions represented by point size and style.
        :param start_date:
        :param num_days_list:
        :param meals_per_day_list:
        :return:
        """
        data = []
        for num_days in num_days_list:
            for meals_per_day in meals_per_day_list:
                results = self.run_experiments(start_date, num_days, meals_per_day)
                for problem_type, problem_results in results.items():
                    for solver, result in problem_results.items():
                        data.append({
                            'Problem Type': problem_type,
                            'Solver': solver.__class__.__name__,
                            'Num Days': num_days,
                            'Meals per Day': meals_per_day,
                            'Score': result[0].score if result[0] is not None else np.nan,
                            'Time': result[1]
                        })

        df = pd.DataFrame(data)

        plt.figure(figsize=(15, 10))
        sns.scatterplot(data=df, x='Time', y='Score', hue='Solver', style='Problem Type',
                        size='Num Days', size_norm=(20, 200))
        plt.title("Algorithm Performance with Different Inputs")
        plt.xlabel("Execution Time (seconds)")
        plt.ylabel("Score")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        self.save_plot("performance_different_inputs")

    def compare_with_different_products(self, start_date: date, num_days: int, meals_per_day: int,
                                        product_data_list: List[pd.DataFrame]):
        """
        This method runs experiments with different sets of product data while keeping other inputs constant.
        It creates a scatter plot showing how algorithms perform with different product sets.
        :param start_date:
        :param num_days:
        :param meals_per_day:
        :param product_data_list:
        :return:
        """
        data = []
        for i, products in enumerate(product_data_list):
            self.products_data = products  # Update the products data
            results = self.run_experiments(start_date, num_days, meals_per_day)
            for problem_type, problem_results in results.items():
                for solver, result in problem_results.items():
                    data.append({
                        'Problem Type': problem_type,
                        'Solver': solver.__class__.__name__,
                        'Product Set': f'Set {i + 1}',
                        'Score': result[0].score if result[0] is not None else np.nan,
                        'Time': result[0]
                    })

        df = pd.DataFrame(data)

        plt.figure(figsize=(15, 10))
        sns.scatterplot(data=df, x='Time', y='Score', hue='Solver', style='Problem Type',
                        size='Product Set', size_norm=(50, 200))
        plt.title("Algorithm Performance with Different Product Sets")
        plt.xlabel("Execution Time (seconds)")
        plt.ylabel("Score")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        self.save_plot("performance_different_products")

    def plot_performance_heatmap(self, data: pd.DataFrame, x: str, y: str, value: str, title: str):
        """
        A helper method to create heatmaps for visualizing performance across different input parameters.
        :param data:
        :param x:
        :param y:
        :param value:
        :param title:
        :return:
        """
        pivot = data.pivot(index=y, columns=x, values=value)
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot, annot=True, cmap="YlGnBu", fmt=".2f")
        plt.title(title)
        plt.tight_layout()
        self.save_plot("plot_performance_heatmap")

    def visualize_input_sensitivity(self, start_date: date, num_days_list: List[int], meals_per_day_list: List[int]):
        """
        This method creates heatmaps to show how each solver's performance (both score and time) changes with different
        numbers of days and meals per day.
        :param start_date:
        :param num_days_list:
        :param meals_per_day_list:
        :return:
        """
        data = []
        for num_days in num_days_list:
            for meals_per_day in meals_per_day_list:
                results = self.run_experiments(start_date, num_days, meals_per_day)
                for problem_type, problem_results in results.items():
                    for solver, result in problem_results.items():
                        data.append({
                            'Problem Type': problem_type,
                            'Solver': solver.__class__.__name__,
                            'Num Days': num_days,
                            'Meals per Day': meals_per_day,
                            'Score': result[0].score if result[0] is not None else np.nan,
                            'Time': result[1]
                        })

        df = pd.DataFrame(data)

        for solver in df['Solver'].unique():
            solver_data = df[df['Solver'] == solver]
            self.plot_performance_heatmap(solver_data, 'Num Days', 'Meals per Day', 'Score',
                                          f'{solver} - Score Heatmap')
            self.plot_performance_heatmap(solver_data, 'Num Days', 'Meals per Day', 'Time',
                                          f'{solver} - Time Heatmap')

    def visualize_ingredient_distribution(self, results: Dict):
        """
        Creates a heatmap showing how frequently each ingredient is used across different problem types and solvers.
        This helps identify if certain algorithms tend to favor particular ingredients.
        :param results:
        :return:
        """
        ingredient_counts = {}
        for problem_type, problem_results in results.items():
            for solver, result in problem_results.items():
                ingredients = [piece.item_id for action in result.selected_actions for piece in action.pieces]
                ingredient_counts[(problem_type, solver.__class__.__name__)] = Counter(ingredients)

        df = pd.DataFrame(ingredient_counts).fillna(0)
        plt.figure(figsize=(15, 10))
        sns.heatmap(df, annot=True, fmt='d', cmap='YlGnBu')
        plt.title('Ingredient Usage Distribution')
        plt.xlabel('Problem Type - Solver')
        plt.ylabel('Ingredient ID')
        plt.tight_layout()
        self.save_plot("visualize_ingredient_distribution")

    def visualize_meal_variety(self, results: Dict):
        """Generates a bar plot comparing the variety of meals produced by each solver and problem type. It
        calculates a "variety score" as the ratio of unique meals to total meals planned. """
        variety_scores = {}
        for problem_type, problem_results in results.items():
            for solver, result in problem_results.items():
                unique_meals = len(set(action.action_id for action in result.selected_actions))
                total_meals = len(result.selected_actions)
                variety_scores[(problem_type, solver.__class__.__name__)] = unique_meals / total_meals

        df = pd.DataFrame.from_dict(variety_scores, orient='index', columns=['Variety Score'])
        df.plot(kind='bar', figsize=(12, 6))
        plt.title('Meal Variety Comparison')
        plt.xlabel('Problem Type - Solver')
        plt.ylabel('Variety Score (Unique Meals / Total Meals)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        self.save_plot("visualize_meal_variety")

    def visualize_waste_reduction(self, results: Dict):
        waste_reduction = {}
        for problem_type, problem_results in results.items():
            for solver, result in problem_results.items():
                used_ingredients = set(piece.item_id for action in result.selected_actions for piece in action.pieces)
                total_ingredients = set(self.products_data['Item ID'])
                waste_reduction[(problem_type, solver.__class__.__name__)] = len(used_ingredients) / len(
                    total_ingredients)

        df = pd.DataFrame.from_dict(waste_reduction, orient='index', columns=['Waste Reduction Score'])
        df.plot(kind='bar', figsize=(12, 6))
        plt.title('Waste Reduction Comparison')
        plt.xlabel('Problem Type - Solver')
        plt.ylabel('Waste Reduction Score (Used Ingredients / Total Ingredients)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        self.save_plot("visualize_waste_reduction")

    def visualize_solver_convergence(self, start_date: date, num_days: int, meals_per_day: int):
        """lots the convergence of solver scores over iterations for algorithms that support this feature (like
        SimulatedAnnealingSolver or RLSolver). This helps visualize how quickly different solvers reach their final
        solutions. """
        convergence_data = {}
        for problem_type in self.problem_types:
            for solver in self.solvers:
                if hasattr(solver, 'get_convergence_data'):
                    experiment = Experiment(
                        problem_type,
                        [solver],
                        start_date,
                        self.products_data,
                        self.recipes_data,
                        number_of_days=num_days,
                        meals_per_day=meals_per_day
                    )
                    results = experiment.run()
                    convergence_data[(problem_type.__name__, solver.__class__.__name__)] = solver.get_convergence_data()

        plt.figure(figsize=(15, 10))
        for key, data in convergence_data.items():
            plt.plot(data, label=f"{key[0]} - {key[1]}")
        plt.title('Solver Convergence Comparison')
        plt.xlabel('Iterations')
        plt.ylabel('Score')
        plt.legend()
        plt.tight_layout()
        self.save_plot("visualize_solver_convergence")

    def visualize_parameter_combinations(self, start_date: date, num_days: int, meals_per_day: int):
        parameters = ["Shelf Time", "Taste Rating", "Number of Steps", "Preparation Time (min)", "Number of Products"]
        max_parameters = {"Shelf Time", "Taste Rating"}
        min_parameters = {"Number of Steps", "Preparation Time (min)", "Number of Products"}

        results = []

        # MinimizeWaste problem
        experiment = Experiment(
            Problems.MinimizeWasteProblem,
            self.solvers,
            start_date,
            self.products_data,
            self.recipes_data,
            number_of_days=num_days,
            meals_per_day=meals_per_day
        )
        minimize_waste_results = experiment.run()

        for solver, result in minimize_waste_results.items():
            results.append({
                'Problem Type': 'MinimizeWaste',
                'Parameters': 'N/A',
                'Solver': solver.__class__.__name__,
                'Score': result[0].score if result[0] is not None else np.nan,
                'Time': result[1]
            })

        # ParametersProblem with different parameter combinations
        for r in range(1, len(parameters) + 1):
            for combo in combinations(parameters, r):
                parameters_to_maximize = [p for p in combo if p in max_parameters]
                parameters_to_minimize = [p for p in combo if p in min_parameters]

                experiment = Experiment(
                    Problems.ParametersProblem,
                    self.solvers,
                    start_date,
                    self.products_data,
                    self.recipes_data,
                    number_of_days=num_days,
                    meals_per_day=meals_per_day,
                    parameters=parameters_to_maximize + parameters_to_minimize
                )
                param_results = experiment.run()

                for solver, result in param_results.items():
                    results.append({
                        'Problem Type': 'ParametersProblem',
                        'Parameters': ', '.join(combo),
                        'Solver': solver.__class__.__name__,
                        'Score': result[0].score if result[0] is not None else np.nan,
                        'Time': result[1]
                    })

        df = pd.DataFrame(results)

        # Plotting
        plt.figure(figsize=(20, 12))

        # Score comparison
        plt.subplot(2, 1, 1)
        sns.barplot(x='Parameters', y='Score', hue='Solver', data=df, ci=None)
        plt.title('Score Comparison for Different Problem Types and Parameters')
        plt.xlabel('Problem Type - Parameters')
        plt.ylabel('Score')
        plt.xticks(rotation=90)
        plt.legend(title='Solver', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Time comparison
        plt.subplot(2, 1, 2)
        sns.barplot(x='Parameters', y='Time', hue='Solver', data=df, ci=None)
        plt.title('Execution Time Comparison for Different Problem Types and Parameters')
        plt.xlabel('Problem Type - Parameters')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=90)
        plt.legend(title='Solver', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        self.save_plot("visualize_parameter_combinations_1")

        # Heatmap for average score across solvers
        plt.figure(figsize=(15, 10))
        pivot_score = df.pivot_table(values='Score', index='Parameters', columns='Solver', aggfunc='mean')
        sns.heatmap(pivot_score, annot=True, fmt='.2f', cmap='YlGnBu')
        plt.title('Average Score Heatmap for Different Problem Types and Parameters')
        plt.tight_layout()
        plt.show()

        # Heatmap for average time across solvers
        plt.figure(figsize=(15, 10))
        pivot_time = df.pivot_table(values='Time', index='Parameters', columns='Solver', aggfunc='mean')
        sns.heatmap(pivot_time, annot=True, fmt='.2f', cmap='YlOrRd')
        plt.title('Average Execution Time Heatmap for Different Problem Types and Parameters')
        plt.tight_layout()
        self.save_plot("visualize_parameter_combinations_2")

    def visualize_all(self, start_date: date, num_days: int, meals_per_day: int,
                      num_days_list: List[int], meals_per_day_list: List[int],
                      product_data_list: List[pd.DataFrame]):
        # Store the original products_data
        original_products_data = self.products_data

        for i, products_data in enumerate(product_data_list):
            print(f"\nAnalyzing Product Dataset {i + 1}")
            self.products_data = products_data  # Update the products data

            results = self.run_experiments(start_date, num_days, meals_per_day)
            self.plot_time_differences(results)
            self.compare_results(results)
            self.compare_with_different_inputs(start_date, num_days_list, meals_per_day_list)
            self.visualize_input_sensitivity(start_date, num_days_list, meals_per_day_list)
            self.visualize_ingredient_distribution(results)
            self.visualize_meal_variety(results)
            self.visualize_waste_reduction(results)
            self.visualize_solver_convergence(start_date, num_days, meals_per_day)
            self.visualize_parameter_combinations(start_date, num_days, meals_per_day)

        # Restore the original products_data
        self.products_data = original_products_data

        # Compare across different product datasets
        self.compare_with_different_products(start_date, num_days, meals_per_day, product_data_list)


if __name__ == "__main__":
    products_data1 = pd.read_csv(r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\products_dataset\known_100.csv")
    products_data2 = pd.read_csv(r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\products_dataset\known_200.csv")
    products_data3 = pd.read_csv(r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\products_dataset\known_300.csv")
    recipes_data = pd.read_csv(r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\recipes.csv")

    visualizer = AlgorithmComparisonVisualizer(products_data1, recipes_data, output_dir='visualization_output')
    visualizer.visualize_all(
        start_date=date(2024, 9, 1),
        num_days=5,
        meals_per_day=3,
        num_days_list=[3, 5, 7],
        meals_per_day_list=[2, 3, 4],
        product_data_list=[products_data1, products_data2, products_data3]
    )
