from abc import ABC, abstractmethod
import random
import math
from typing import List, Dict, Any, Tuple

from ..Problems.problem import Problem


class Solver(ABC):
    @abstractmethod
    def solve(self, problem: 'Problem') -> Any:
        """Solve the given problem and return the solution."""
        pass

    @abstractmethod
    def get_iterations(self) -> int:
        """Return the number of iterations performed by the solver."""
        pass