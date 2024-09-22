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
  - `greedy_algorithm.py`: Implements the `GreedySolver`
  - `reinforcement_learning_algorithm.py`: Implements the `RLSolver`
  - `simulated_annealing_algorithm.py`: Implements the `SimulatedAnnealingSolver`
- `GUI/`: A folder containing the graphical user interface components
  - `main_gui.py`: The main GUI application file containing the MealPlannerGUI class
  - `results_frame.py`: Implements the ResultsFrame for displaying optimization results
  - `home_frame.py`: Implements the HomeFrame for the main page of the GUI
  - `upload_frame.py`: Implements the UploadFrame for uploading product data
  - `settings_frame.py`: Implements the SettingsFrame for configuring optimization settings
  - `scrollable_frame.py`: Implements a ScrollableProductFrame for displaying products


## Components

### GUI Folder

#### MealPlannerGUI (main_gui.py)

The `MealPlannerGUI` class is the main application class that integrates all GUI components and handles the overall flow of the application. It creates the main window and manages navigation between different frames. This class is responsible for:

- Creating the navigation frame
- Initializing all other frames (HomeFrame, UploadFrame, SettingsFrame, ResultsFrame)
- Handling navigation between frames
- Running the optimization process
- Managing temporary CSV file creation
- Handling result downloads

#### ResultsFrame (results_frame.py)

The `ResultsFrame` class is responsible for displaying the optimization results. It shows the results for each solver, including the time taken, meals planned for each day, and the total score.

#### HomeFrame (home_frame.py)

The `HomeFrame` class implements the main page of the GUI, providing an overview of the application and instructions for use.

#### UploadFrame (upload_frame.py)

The `UploadFrame` class allows users to upload and manage product data. It includes functionality for adding products manually or via CSV file.

#### SettingsFrame (settings_frame.py)

The `SettingsFrame` class provides options for configuring the optimization process, including selecting the problem type, optimization parameters, and solvers to use.

#### ScrollableProductFrame (scrollable_frame.py)

The `ScrollableProductFrame` class implements a scrollable frame for displaying and managing a list of products.


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
2. `ParametersProblem`: Allows optimization based on specified parameters (e.g., nutritional values).
3. `CountExpiredItemsProblem`:  Aims to minimize the number of items that would expire if not used.

All the classes implement custom `get_action_score` methods to evaluate recipes based on their respective objectives.

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
   from MealOptimizer.Solvers import GreedySolver, SimulatedAnnealingSolver, RLSolver
   from datetime import date
   ```

2. Set up the experiment parameters:

   ```python
   problem = Problems.MinimizeWasteProblem
   solvers = [GreedySolver(), SimulatedAnnealingSolver(), RLSolver()]
   products_data_path = "path/to/your/products_data.csv"
   recipes_data_path = "path/to/your/recipes_data.csv"
   start_date = date(2024, 9, 1)
   ```

3. Create and run the experiment:

   ```python
   experiment = Experiment(problem, solvers, start_date, products_data_path, recipes_data_path, umber_of_days=1,
                 meals_per_day=3, parameters_to_maximize=None)
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

2. Run the script:

   ```
   python main.py
   ```
This will launch the graphical user interface, allowing you to interact with the meal planning system.

