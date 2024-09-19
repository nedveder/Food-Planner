# Food-Planner

## Overview

This project implements a meal planning system using various optimization algorithms. It aims to create efficient meal plans based on different objectives such as minimizing food waste or maximizing nutritional value.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Components](#components)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Running the Project](#running-the-project)
6. [Extending the System](#extending-the-system)

## Project Structure

The project consists of several Python files organized into folders:

- `main.py`: The main entry point for running the meal planning system
- `Experiments/`
  - `experiment.py`: Contains the `Experiment` class for running meal planning experiments
- `Problems/`: A folder containing the core problem definition and utilities
  - `problem.py`: Defines the base `Problem` class for meal planning problems
  - `problem_types.py`: Implements specific problem types
  - `state.py`: Defines the `State` class to represent the current state of the meal planning problem
  - `utils.py`: Contains utility classes like `Piece` and `Action`
- `Solvers/`: A folder containing various optimization algorithms
  - `solver.py`: Defines the base `Solver` abstract class
  - `graph_algorithm.py`: Implements the `PlanningGraphSolver`
  - `greedy_algorithm.py`: Implements the `GreedySolver`
  - `reinforcement_learning_algorithm.py`: Implements the `RLSolver`
  - `simulated_annealing_algorithm.py`: Implements the `SimulatedAnnealingSolver`


## Components
### Experiment (experiment.py)

The `Experiment` class is responsible for setting up and running the meal planning experiments. It loads datasets, initializes problems and solvers, and executes the experiments.

### Problems Folder
#### Problem (problem.py)

The `Problem` class is an abstract base class that defines the structure for meal planning problems. It manages legal actions (recipes) based on available ingredients and handles date and meal scheduling logic. Key methods include:

- `create_legal_actions`: Generates a list of valid recipes
- `get_available_actions`: Determines available actions based on the current state
- `is_goal_state`: Checks if the goal state has been reached

#### Problem Types (problem_types.py)

This file defines specific problem types:

1. `MinimizeWasteProblem`: Aims to minimize food waste by prioritizing ingredients closer to expiration.
2. `MaximizeByParametersProblem`: Allows optimization based on specified parameters (e.g., nutritional values).

Both classes implement custom `get_action_score` methods to evaluate recipes based on their respective objectives.

#### State (state.py)

The `State` class represents the current state of the meal planning problem. It keeps track of available pieces (ingredients) and selected actions (recipes). Key methods include:

- `update_state`: Updates the state after selecting an action
- `is_available_piece`: Checks if a piece is available in the current state

#### Utils (utils.py)

This file contains utility classes:

- `Piece`: Represents an ingredient with properties like item_id, quantity, unit, and expiration_date
- `Action`: Represents a recipe with properties like action_id, name, and a list of required pieces


### Solvers Folder

#### Solver (solver.py)

The `Solver` class is an abstract base class that defines the interface for all solver implementations. It includes an abstract `solve` method that must be implemented by all concrete solver classes.

#### Graph Algorithm (graph_algorithm.py)

The `PlanningGraphSolver` class implements a graph-based algorithm for solving meal planning problems. It builds a planning graph and extracts an optimal solution. Key methods include:

- `build_planning_graph`: Constructs the planning graph
- `extract_solution`: Extracts the best meal plan from the graph

#### Greedy Algorithm (greedy_algorithm.py)

The `GreedySolver` class implements a greedy approach to solving meal planning problems. It iteratively selects the best available action based on the problem's scoring method.

#### Reinforcement Learning Algorithm (reinforcement_learning_algorithm.py)

The `RLSolver` class implements a Q-learning based approach to solve meal planning problems. It learns the optimal policy through repeated episodes of interaction with the problem environment. Key features include:

- Epsilon-greedy action selection
- Q-value updates based on rewards and future state values
- Ability to handle large state spaces through function approximation

#### Simulated Annealing Algorithm (simulated_annealing_algorithm.py)

The `SimulatedAnnealingSolver` class implements the simulated annealing optimization technique. It starts with a random solution and iteratively improves it by exploring neighboring solutions, with a decreasing probability of accepting worse solutions over time. Key features include:

- Temperature-based acceptance probability
- Cooling schedule to control the exploration-exploitation trade-off
- Ability to escape local optima through probabilistic acceptance of worse solutions


## Installation

To install the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/meal-planning-optimization.git
   ```
2. Navigate to the project directory:
   ```
   cd meal-planning-optimization
   ```


## Usage

To use the meal planning system, you can either run the `main.py` script (see [Running the Project](#running-the-project)) or use the components in your own Python script:

1. Import the necessary classes:

   ```python
   from MealOptimizer.Experiments import Experiment
   from MealOptimizer import Problems
   from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, PlanningGraphSolver, RLSolver
   from datetime import date
   ```

2. Set up the experiment parameters:

   ```python
   problem = Problems.MinimizeWasteProblem
   solvers = [GreedySolver(), SimulatedAnnealingSolver(), PlanningGraphSolver(), RLSolver()]
   products_data_path = "path/to/your/products_data.csv"
   recipes_data_path = "path/to/your/recipes_data.csv"
   start_date = date(2024, 9, 1)
   ```

3. Create and run the experiment:

   ```python
   experiment = Experiment(problem, solvers, start_date, products_data_path, recipes_data_path, number_of_days=5)
   results = experiment.run()
   ```

4. Analyze the results:

   ```python
   for solver, state in results.items():
       print(f"{solver} reached the goal state with solution:\n {state}")
   ```

## Running the Project

To run the meal planning system using the provided `main.py` script:

1. Ensure you're in the project root directory.

2. Update the `products_data_path` and `recipes_data_path` variables in `main.py` to point to your CSV files:

   ```python
   products_data_path = "path/to/your/products_data.csv"
   recipes_data_path = "path/to/your/recipes_data.csv"
   ```

3. Run the script:

   ```
   python main.py
   ```
