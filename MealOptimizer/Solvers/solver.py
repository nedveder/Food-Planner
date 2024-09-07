from abc import ABC, abstractmethod
from ..Problems.problem import Problem
from ..Problems.state import State


class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem, state: State) -> State:
        """Solve the given problem and return the solution."""
        raise NotImplementedError
