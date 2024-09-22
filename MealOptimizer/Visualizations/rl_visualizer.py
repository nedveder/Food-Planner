from datetime import date

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from MealOptimizer.Solvers import RLSolver
from MealOptimizer.Problems import MinimizeWasteProblem, CountExpiredItemsProblem
from MealOptimizer.Experiments import Experiment
import os
from tqdm import tqdm


class RLSolverVisualization:
    def __init__(self, initial_state, piece_dataset, action_dataset, start_date, output_dir="rl_visualization_results2"):
        self.initial_state = initial_state
        self.piece_dataset = piece_dataset
        self.action_dataset = action_dataset
        self.start_date = start_date
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run_experiments(self, parameter_ranges: Dict[str, List[Any]], num_days: int = 7, meals_per_day: int = 3) -> pd.DataFrame:
        results = []
        total_experiments = (
                len(parameter_ranges['learning_rate']) *
                len(parameter_ranges['discount_factor']) *
                len(parameter_ranges['epsilon']) *
                len(parameter_ranges['episodes'])
        )

        with tqdm(total=total_experiments, desc="Running Experiments") as pbar:
            for learning_rate in parameter_ranges['learning_rate']:
                for discount_factor in parameter_ranges['discount_factor']:
                    for epsilon in parameter_ranges['epsilon']:
                        for episodes in parameter_ranges['episodes']:
                            solver = RLSolver(learning_rate=learning_rate,
                                              discount_factor=discount_factor,
                                              epsilon=epsilon,
                                              episodes=episodes)

                            # MinimizeWasteProblem
                            minimize_waste_problem = MinimizeWasteProblem(self.action_dataset, self.start_date, self.piece_dataset,
                                                                          number_of_days=num_days, meals_per_day=meals_per_day)
                            minimize_waste_state = solver.solve(minimize_waste_problem, self.initial_state)
                            minimize_waste_score = minimize_waste_problem.get_score(minimize_waste_state)

                            # CountExpiredItemsProblem
                            count_expired_problem = CountExpiredItemsProblem(self.action_dataset, self.start_date, self.piece_dataset,
                                                                             number_of_days=num_days, meals_per_day=meals_per_day)
                            count_expired_state = solver.solve(count_expired_problem, self.initial_state)
                            count_expired_score = count_expired_problem.get_score(count_expired_state)

                            results.append({
                                'learning_rate': learning_rate,
                                'discount_factor': discount_factor,
                                'epsilon': epsilon,
                                'episodes': episodes,
                                'minimize_waste_score': minimize_waste_score,
                                'count_expired_score': count_expired_score
                            })

                            pbar.update(1)

        return pd.DataFrame(results)

    def plot_parameter_vs_score(self, results: pd.DataFrame, parameter: str):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=results, x=parameter, y='minimize_waste_score', label='MinimizeWaste')
        sns.scatterplot(data=results, x=parameter, y='count_expired_score', label='CountExpired')
        plt.title(f'Score vs {parameter.replace("_", " ").title()}')
        plt.xlabel(parameter.replace("_", " ").title())
        plt.ylabel('Score')
        plt.legend()
        plt.savefig(os.path.join(self.output_dir, f'score_vs_{parameter}.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def plot_heatmap(self, results: pd.DataFrame, x_param: str, y_param: str):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        for ax, problem in zip([ax1, ax2], ['minimize_waste_score', 'count_expired_score']):
            pivot_table = results.pivot_table(values=problem, index=y_param, columns=x_param, aggfunc=np.mean)
            sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='.2f', ax=ax)
            ax.set_title(f'{problem.replace("_", " ").title()}\n{y_param.replace("_", " ").title()} vs {x_param.replace("_", " ").title()}')

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'heatmap_{x_param}_vs_{y_param}.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def plot_3d_surface(self, results: pd.DataFrame, x_param: str, y_param: str):
        fig = plt.figure(figsize=(20, 8))

        for idx, problem in enumerate(['minimize_waste_score', 'count_expired_score'], 1):
            pivot_table = results.pivot_table(values=problem, index=y_param, columns=x_param, aggfunc=np.mean)
            x = pivot_table.columns
            y = pivot_table.index
            X, Y = np.meshgrid(x, y)
            Z = pivot_table.values

            ax = fig.add_subplot(1, 2, idx, projection='3d')
            surf = ax.plot_surface(X, Y, Z, cmap='coolwarm')
            ax.set_xlabel(x_param.replace("_", " ").title())
            ax.set_ylabel(y_param.replace("_", " ").title())
            ax.set_zlabel('Score')
            ax.set_title(
                f'{problem.replace("_", " ").title()}\nScore vs {x_param.replace("_", " ").title()} and {y_param.replace("_", " ").title()}')
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'3d_surface_{x_param}_vs_{y_param}.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def plot_problem_transfer(self, results: pd.DataFrame):
        plt.figure(figsize=(10, 8))
        plt.scatter(results['minimize_waste_score'], results['count_expired_score'], alpha=0.6)
        plt.xlabel('MinimizeWasteProblem Score')
        plt.ylabel('CountExpiredItemsProblem Score')
        plt.title('Transfer Learning: MinimizeWasteProblem vs CountExpiredItemsProblem')

        min_score = min(results['minimize_waste_score'].min(), results['count_expired_score'].min())
        max_score = max(results['minimize_waste_score'].max(), results['count_expired_score'].max())
        plt.plot([min_score, max_score], [min_score, max_score], 'r--', label='Perfect Transfer')

        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'problem_transfer.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def generate_data_tables(self, results: pd.DataFrame):
        # Summary statistics
        summary_stats = results.describe()
        summary_stats.to_csv(os.path.join(self.output_dir, 'summary_statistics.csv'))

        # Top 10 parameter combinations for each problem
        top_minimize_waste = results.nlargest(10, 'minimize_waste_score')
        top_count_expired = results.nlargest(10, 'count_expired_score')

        top_minimize_waste.to_csv(os.path.join(self.output_dir, 'top_10_minimize_waste.csv'), index=False)
        top_count_expired.to_csv(os.path.join(self.output_dir, 'top_10_count_expired.csv'), index=False)

        # Correlation matrix
        correlation_matrix = results.corr()
        correlation_matrix.to_csv(os.path.join(self.output_dir, 'correlation_matrix.csv'))

    def run_all_visualizations(self, parameter_ranges: Dict[str, List[Any]], num_days: int = 7, meals_per_day: int = 3):
        print("Starting experiments...")
        results = self.run_experiments(parameter_ranges, num_days, meals_per_day)

        print("Generating visualizations...")
        with tqdm(total=len(parameter_ranges) +
                        len(parameter_ranges) * (len(parameter_ranges) - 1) +
                        1 + 1,
                  desc="Generating Visualizations") as pbar:

            for param in parameter_ranges.keys():
                self.plot_parameter_vs_score(results, param)
                pbar.update(1)

            # for x_param in parameter_ranges.keys():
            #     for y_param in parameter_ranges.keys():
            #         if x_param != y_param:
            #             self.plot_heatmap(results, x_param, y_param)
            #             self.plot_3d_surface(results, x_param, y_param)
            #             pbar.update(1)

            self.plot_problem_transfer(results)
            pbar.update(1)

            self.generate_data_tables(results)
            pbar.update(1)

        print(f"All visualizations and data tables have been saved to the '{self.output_dir}' directory.")


# Example usage in main.py
def main():
    # Setup your experiment parameters
    piece_dataset = pd.read_csv("../Datasets/non optimality of greedy/products.csv")
    action_dataset = pd.read_csv("../Datasets/non optimality of greedy/recipes.csv")
    start_date = date(2024, 9, 1)
    initial_state = Experiment.create_initial_state(piece_dataset)

    visualizer = RLSolverVisualization(initial_state, piece_dataset, action_dataset, start_date)

    parameter_ranges = {
        'learning_rate': [0.01]*5,
        'discount_factor': [0.99]*5,
        'epsilon': [0.2]*5,
        'episodes': [100]*5
    }

    visualizer.run_all_visualizations(parameter_ranges)


if __name__ == "__main__":
    main()