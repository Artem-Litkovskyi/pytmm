import numpy as np

from pytmm.beam_splines.boundary_conditions import pinned_ends
from pytmm.beam_splines.elements import BeamElement
from pytmm.beam_splines.nodes import BeamPinnedSupport
from pytmm.beam_splines.solvers import StatisticalBeamSplineSolver

# Three points (two elements)
T = [2, 4, 5]
SUPPORTS = [-1, 4, 2]

# Start and end states for each element
DESIRED_EDGE_STATES = np.array([
    [-1, 4, 0, -2.25],       # Element 1
    [4, -0.5, -4.5, -2.25],
    [4, -0.5, -4.5, 4.5],    # Element 2
    [2, -2.75, 0, 4.5],
], dtype=np.float64)


def test_statistical_beam_spline_solver():
    """Test StatisticalBeamSplineSolver.solve."""
    spline = StatisticalBeamSplineSolver(
        t=T,
        element_class=BeamElement,
        element_data={},
        node_class=BeamPinnedSupport,
        node_data={"displacement": SUPPORTS[1:-1]},
        boundary_conditions=pinned_ends(SUPPORTS[0], SUPPORTS[-1]),
    )

    result = spline.solve()

    np.testing.assert_allclose(
        result.get_all_edge_states(),
        DESIRED_EDGE_STATES,
    )
