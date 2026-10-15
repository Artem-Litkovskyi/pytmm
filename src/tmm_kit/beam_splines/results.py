from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from tmm_kit.tmm.base import ElementEdge
from tmm_kit.tmm.result import TMMResult


@dataclass
class StatisticalBeamSplineResult:
    """Immutable result container holding state vectors and evaluation logic."""

    t: np.ndarray | Sequence[float]
    tmm_result: TMMResult

    def evaluate(
        self, t: np.typing.ArrayLike
    ) -> np.ndarray:
        """Evaluate a beam spline state at a certain coordinate.

        Parameters
        ----------
        t
            Global coordinate or array of them
            (from self.t[0] to self.t[-1]).
        """
        eval_ts = np.atleast_1d(np.asarray(t, dtype=np.float64))
        states = np.empty((eval_ts.size, self.tmm_result.state_size), dtype=np.float64)

        for i, eval_t in enumerate(eval_ts):
            element_i = np.searchsorted(self.t, eval_t, side="right") - 1
            element_i = int(min(max(element_i, 0), len(self.t) - 2))

            s = float(eval_t - self.t[element_i])
            A, b = self.tmm_result.elements[element_i].get_transfer_eq(s)

            start_state = self.tmm_result.get_edge_state(
                element_i, ElementEdge.START
            )

            states[i] = A @ start_state + b

        if np.isscalar(t):
            return states[0]
        return states

    def get_state_at_node(
        self,
        element_i: np.typing.ArrayLike,
        element_edge: ElementEdge | None = None,
    ) -> np.ndarray:
        """Get state vectors from the array of all element states.

        Parameters
        ----------
        element_i
            Element index (indices).
        element_edge
            The edge at which the state is retrieved.
            If None, retrieve at both edges.
        """
        return self.tmm_result.get_edge_state(element_i, element_edge)

    def get_all_edge_states(
        self,
        element_edge: ElementEdge | None = None,
    ) -> np.ndarray:
        """Get all state vectors from the array of all element states.

        Parameters
        ----------
        element_edge
            The edge at which the state is retrieved.
            If None, retrieve at both edges.
        """
        return self.tmm_result.get_all_edge_states(element_edge)
