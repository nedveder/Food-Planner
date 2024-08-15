import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict


class PerformanceMetrics:
    def __init__(self, dataset_size: int, runtime: float, iterations: int, kpis: Dict[str, float]):
        self.dataset_size = dataset_size
        self.runtime = runtime
        self.iterations = iterations
        self.kpis = kpis


class SolverPerformance:
    def __init__(self, solver_name: str):
        self.solver_name = solver_name
        self.metrics: List[PerformanceMetrics] = []

    def add_metrics(self, metrics: PerformanceMetrics):
        self.metrics.append(metrics)


class VisualizationComparison:
    def __init__(self):
        self.performances: Dict[str, SolverPerformance] = {}

    def add_solver_performance(self, solver_name: str, metrics: PerformanceMetrics):
        if solver_name not in self.performances:
            self.performances[solver_name] = SolverPerformance(solver_name)
        self.performances[solver_name].add_metrics(metrics)

    def _create_dataframe(self) -> pd.DataFrame:
        data = []
        for solver_name, performance in self.performances.items():
            for metrics in performance.metrics:
                row = {
                    'Solver': solver_name,
                    'Dataset Size': metrics.dataset_size,
                    'Runtime': metrics.runtime,
                    'Iterations': metrics.iterations,
                    **metrics.kpis
                }
                data.append(row)
        return pd.DataFrame(data)

    def plot_runtime_comparison(self):
        df = self._create_dataframe()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Dataset Size', y='Runtime', hue='Solver')
        plt.title('Runtime Comparison')
        plt.xlabel('Dataset Size')
        plt.ylabel('Runtime (seconds)')
        plt.show()

    def plot_iterations_comparison(self):
        df = self._create_dataframe()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Dataset Size', y='Iterations', hue='Solver')
        plt.title('Iterations Comparison')
        plt.xlabel('Dataset Size')
        plt.ylabel('Number of Iterations')
        plt.show()

    def plot_kpi_comparison(self, kpi_name: str):
        df = self._create_dataframe()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Dataset Size', y=kpi_name, hue='Solver')
        plt.title(f'{kpi_name} Comparison')
        plt.xlabel('Dataset Size')
        plt.ylabel(kpi_name)
        plt.show()

    def generate_comparison_table(self) -> pd.DataFrame:
        df = self._create_dataframe()
        return df.groupby('Solver').agg({
            'Runtime': ['mean', 'std'],
            'Iterations': ['mean', 'std'],
            **{kpi: ['mean', 'std'] for kpi in df.columns if kpi not in ['Solver', 'Dataset Size', 'Runtime', 'Iterations']}
        }).round(2)