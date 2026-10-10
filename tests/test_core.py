import numpy as np

from pytmm.core.base import ElementSide
from pytmm.core.result import TMMResult
from pytmm.core.solver import TMMSolver
from pytmm.electrical.boundary_conditions import electrical_circuit_boundary_node
from pytmm.electrical.constants import ELECTRICAL_STATE_SIZE
from pytmm.electrical.elements import ElectricalElement
from pytmm.electrical.nodes import ElectricalNode

ELEMENTS = [
    ElectricalElement(1, 2, 2),  # 0. 2R resistor, 2E battery
    ElectricalElement(1, 6, 0),  # 1. 6R resistor
    ElectricalElement(1, 0, 1),  # 2. E battery
    ElectricalElement(1, 0, 0),  # 3. Wire
    ElectricalElement(1, 2, 0),  # 4. 2R resistor
    ElectricalElement(1, 4, 0),  # 5. 4R resistor
]

NODES = [
    ElectricalNode([2], [0, 3]),
    ElectricalNode([0, 4], [1]),
    ElectricalNode([1, 5], [2]),
]

# Replace the last node with boundary conditions
BCS = electrical_circuit_boundary_node([3], [4, 5], 1)

I1 = 9 / 14
I2 = 15 / 28
I3 = 2 / 7

E1 = 1.0
E2 = 1.714285
E3 = 0.0

DESIRED_STATES_AT_NODES = np.array(
    [
        E1, I1,     # Element 0
        E2, I1,
        E2, I3,     # Element 1
        E3, I3,
        E3, I2,     # Element 2
        E1, I2,
        E1, I2-I1,  # Element 3
        E1, I2-I1,
        E1, I3-I1,  # Element 4
        E2, I3-I1,
        E1, I2-I3,  # Element 5
        E3, I2-I3,
    ]
)


def test_tmm_solver():
    """Test TMMSolver.solve on an electrical circuit example."""
    solver = TMMSolver(
        ELECTRICAL_STATE_SIZE,
        ELEMENTS,
        NODES,
        BCS,
    )

    result = solver.solve()

    np.testing.assert_allclose(
        result.states_at_nodes, DESIRED_STATES_AT_NODES, rtol=1e-6, atol=1e-6
    )


def test_tmm_result_evaluate_at_nodes():
    """Test TMMResult.evaluate on an electrical circuit example."""
    result = TMMResult(ELEMENTS, DESIRED_STATES_AT_NODES)

    states_at_nodes = []

    for i in range(len(ELEMENTS)):
        states_at_nodes.append(result.evaluate(i, 1))

    np.testing.assert_allclose(
        np.array(states_at_nodes).flatten(),
        np.concatenate(
            [
                DESIRED_STATES_AT_NODES[i : i + 2]
                for i in range(2, len(DESIRED_STATES_AT_NODES), 4)
            ]
        ),
        rtol=1e-6,
        atol=1e-6,
    )


def test_tmm_result_get_state_at_node():
    """Test TMMResult.get_state_at_node on an electrical circuit example."""
    result = TMMResult(ELEMENTS, DESIRED_STATES_AT_NODES)

    np.testing.assert_allclose(
        result.get_state_at_node(0, ElementSide.START),
        DESIRED_STATES_AT_NODES[0:2],
    )
    np.testing.assert_allclose(
        result.get_state_at_node(0, ElementSide.END),
        DESIRED_STATES_AT_NODES[2:4],
    )
    np.testing.assert_allclose(
        result.get_state_at_node(0),
        DESIRED_STATES_AT_NODES[0:4].reshape(2, 2),
    )
    np.testing.assert_allclose(
        result.get_state_at_node([0, 2], ElementSide.START),
        DESIRED_STATES_AT_NODES[[0, 1, 8, 9]].reshape(2, 2),
    )
