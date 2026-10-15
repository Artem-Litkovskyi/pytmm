from collections.abc import Sequence

import numpy as np

from tmm_kit.beam_splines.constants import BEAM_STATE_SIZE
from tmm_kit.beam_splines.nodes import BeamSplineNode
from tmm_kit.beam_splines.results import StatisticalBeamSplineResult
from tmm_kit.tmm.base import TMMElement, TMMEquation
from tmm_kit.tmm.solver import TMMSolver


class StatisticalBeamSplineSolver:
    """Solve a statistical beam spline boundary-value problem."""

    def __init__(
        self,
        t: Sequence[float] | np.ndarray,
        element_class: type[TMMElement],
        element_data: dict[str, Sequence],
        node_class: type[BeamSplineNode],
        node_data: dict[str, Sequence],
        boundary_conditions: list[TMMEquation],
    ):
        """Initialize and assemble a statistical beam spline solver.

        Parameters
        ----------
        t
            Coordinates of the spline segment ends.
        element_class
            TMM element class used for every spline segment.
        element_data
            Struct of Arrays for element instances.
            Key - argument name.
            Value - array of argument values per element.
        node_class
            Beam spline node class used at every spline junction.
        node_data
            Struct of Arrays for node instances.
            Key - argument name.
            Value - array of argument values per node.
        boundary_conditions
            Equations imposed at the beam boundaries.
        """
        if len(t) < 2:
            raise ValueError("The number of t points must be greater or equal to 2")

        self.t = np.asarray(t, dtype=np.float64)

        element_lengths = np.diff(t)
        elements = _create_elements(element_class, element_lengths, element_data)

        nodes_n = len(t) - 2  # Exclude boundary nodes
        nodes = _create_nodes(node_class, nodes_n, node_data)

        self.solver = TMMSolver(
            BEAM_STATE_SIZE,
            elements,
            nodes,
            boundary_conditions,
        )

    def solve(self) -> StatisticalBeamSplineResult:
        """Solve the assembled beam spline boundary-value problem."""
        return StatisticalBeamSplineResult(
            self.t,
            self.solver.solve(),
        )


def _create_elements(
    element_class: type[TMMElement],
    lengths: np.ndarray,
    data: dict[str, Sequence],
):
    if not data:
        return [element_class(length) for length in lengths]

    keys = data.keys()
    values_per_element = zip(*data.values())  # Transposes columns into rows

    elements_n = len(lengths)
    for k in keys:
        len_k = len(data[k])
        if len_k == len(lengths):
            continue
        raise ValueError(
            f"The number of values ({len_k}) for the \"{k}\" key "
            f"doesn't match the number of elements ({elements_n})"
        )

    elements = []
    for length, vals in zip(lengths, values_per_element):
        kwargs = dict(zip(keys, vals))
        elements.append(element_class(length, **kwargs))  # type: ignore[call-arg]

    return elements


def _create_nodes(
    node_class: type[BeamSplineNode],
    nodes_n: int,
    data: dict[str, Sequence],
):
    if not data:
        return [node_class(i, i+1) for i in range(nodes_n)]

    keys = data.keys()
    values_per_node = zip(*data.values())  # Transposes columns into rows

    for k in keys:
        len_k = len(data[k])
        if len_k == nodes_n:
            continue
        raise ValueError(
            f"The number of values ({len_k}) for the \"{k}\" key "
            f"doesn't match the number of nodes ({nodes_n})"
        )

    nodes = []
    for i, vals in enumerate(values_per_node):
        kwargs = dict(zip(keys, vals))
        nodes.append(node_class(i, i+1, **kwargs))

    return nodes
