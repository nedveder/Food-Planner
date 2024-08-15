from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any


class Problem(ABC):
    @abstractmethod
    def load_data(self, data_source: str) -> pd.DataFrame:
        """Load data from the given source into a pandas DataFrame."""
        pass

    @abstractmethod
    def apply_solution(self, solution: Any) -> None:
        """Apply the given solution to the problem."""
        pass

    @abstractmethod
    def evaluate_solution(self) -> Dict[str, float]:
        """Evaluate the applied solution based on defined KPIs."""
        pass

    @abstractmethod
    def generate_output(self) -> pd.DataFrame:
        """Generate a meaningful output for the user."""
        pass

    @abstractmethod
    def get_state(self) -> Any:
        """Get the current state of the problem."""
        pass

    @abstractmethod
    def is_goal_state(self, state: Any) -> bool:
        """Check if the given state is a goal state."""
        pass

    @abstractmethod
    def get_possible_actions(self, state: Any) -> List[Any]:
        """Get possible actions for the given state."""
        pass

    @abstractmethod
    def apply_action(self, state: Any, action: Any) -> Any:
        """Apply the given action to the state and return the new state."""
        pass

    @abstractmethod
    def get_kpis(self) -> List[str]:
        """Return a list of KPI names for this problem."""
        pass



