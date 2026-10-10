from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from .base import ElementSide, TMMElement


@dataclass
class TMMResult:
    """Immutable result container holding state vectors and evaluation logic."""

    elements: list[TMMElement]
    states_at_nodes: np.ndarray

    def __post_init__(self):
        """Calculate state size dynamically based on the flattened unknowns vector."""
        number_of_sides = 2 * len(self.elements)
        self.state_size = self.states_at_nodes.size // number_of_sides

    def evaluate(
        self, element_i: int, s: float | np.ndarray | Sequence[float]
    ) -> np.ndarray:
        """Evaluate an element state at a certain local coordinate.

        Parameters
        ----------
        element_i
            Element index.
        s
            Local coordinate (from 0 to self.elements[element_i].length).
        """
        eval_s = np.atleast_1d(np.asarray(s, dtype=np.float64))
        states = np.empty(
            (eval_s.size, self.state_size), dtype=np.float64
        )

        for i, s in enumerate(eval_s):
            start_state = self.get_state_at_node(element_i, ElementSide.START)
            tm_A, tm_b = self.elements[element_i].get_transfer_eq(s)
            states[i] = tm_A @ start_state + tm_b

        if isinstance(s, Sequence):
            return states
        else:
            return states[0]

    def get_state_at_node(
        self,
        element_i: int | Sequence[int],
        element_side: ElementSide | None = None,
    ) -> np.ndarray:
        """Get state vectors from the array of all element states.

        Parameters
        ----------
        element_i
            Element index or an array of them.
        element_side
            The side at which the state is retrieved.
            If None, retrieve at both sides.
        """
        scalar_element = isinstance(element_i, (int, np.integer))
        element_indices = np.atleast_1d(np.asarray(element_i, dtype=np.int64))
        states = self.states_at_nodes.reshape(-1, self.state_size)

        if element_side is None:
            state_indices = np.stack(
                (2 * element_indices, 2 * element_indices + 1),
                axis=1,
            ).reshape(-1)
            return states[state_indices]

        side_offset = int(element_side == ElementSide.END)
        state_indices = 2 * element_indices + side_offset
        selected_states = states[state_indices]

        if scalar_element:
            return selected_states[0]
        return selected_states
