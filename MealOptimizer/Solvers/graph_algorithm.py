from typing import List, Dict, Set
from ..Problems.problem import Problem
from ..Problems.state import State
from ..Problems.utils import Action, Piece
from .solver import Solver


class PlanningGraphSolver(Solver):
    def solve(self, problem: Problem, initial_state: State) -> State:
        graph = self.build_planning_graph(problem, initial_state)
        plan = self.extract_solution(graph, problem, initial_state)

        final_state = initial_state
        for action in plan:
            final_state.update_state(action)

        return final_state

    def build_planning_graph(self, problem: Problem, initial_state: State) -> List[Dict]:
        graph = []
        current_pieces = set(initial_state.get_available_pieces)
        reached_goal = False

        while not reached_goal:
            action_layer = {}
            for action in problem.legal_actions:
                if all(piece in current_pieces for piece in action.pieces):
                    action_layer[action] = set(action.pieces)

            new_pieces = set(current_pieces)
            for action in action_layer:
                new_pieces.update(action.pieces)

            graph.append({"pieces": current_pieces, "actions": action_layer})

            if len(graph) >= problem.requested_amount:
                reached_goal = True

            if new_pieces == current_pieces:  # No new pieces added
                break

            current_pieces = new_pieces

        return graph

    def extract_solution(self, graph: List[Dict], problem: Problem, initial_state: State) -> List[Action]:
        goal_layer = len(graph) - 1
        plan = []
        current_state = initial_state

        while len(plan) < problem.requested_amount and goal_layer >= 0:
            layer = graph[goal_layer]
            best_action = max(
                layer["actions"].keys(),
                key=lambda act: problem.get_action_score(act, current_state),
                default=None
            )

            if best_action:
                plan.append(best_action)
                # Update the current state
                current_state = self.apply_action(current_state, best_action)
                # Remove the pieces used by this action from all previous layers
                for piece in best_action.pieces:
                    for prev_layer in graph[:goal_layer + 1]:
                        if piece in prev_layer["pieces"]:
                            prev_layer["pieces"].remove(piece)
                        for action in list(prev_layer["actions"].keys()):
                            if piece in prev_layer["actions"][action]:
                                del prev_layer["actions"][action]

            goal_layer -= 1

        return list(reversed(plan))

    @staticmethod
    def pieces_to_set(pieces: List[Piece]) -> Set[Piece]:
        return set(pieces)

    @staticmethod
    def apply_action(state: State, action: Action) -> State:
        new_state = State([Piece(p.item_id, p.quantity, p.expiration_date) for p in state.get_available_pieces])
        new_state.update_state(action)
        return new_state