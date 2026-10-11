from abc import abstractmethod
from dataclasses import dataclass

from pytmm.beam_splines.constants import (
    BEAM_DISPLACEMENT,
    BEAM_FORCE,
    BEAM_MOMENT,
    BEAM_SLOPE,
    BEAM_STATE_SIZE,
)
from pytmm.core.base import ElementEdge, TMMEquation, TMMNode


@dataclass(slots=True, init=False)
class BeamSplineNode(TMMNode):
    """Base class for beam spline nodes.

    Can have only one inbound and one outbound elements.
    """

    # Custom init limits the number of inbound and outbound elements
    def __init__(self, inbound_element: int, outbound_element: int, **kwargs):
        super(BeamSplineNode, self).__init__(
            inbound_elements=[inbound_element],
            outbound_elements=[outbound_element],
        )

        # kwargs allow the init to be inherited by subclasses with additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def get_conjugation_eq(self) -> list[TMMEquation]:
        """Return the conjugation equations connecting elements."""
        pass

    def get_conjugation_eq_n(self) -> int:
        """Return the number of conjugation equations."""
        return BEAM_STATE_SIZE



@dataclass(slots=True, init=False)
class BeamPinnedSupport(BeamSplineNode):
    """Beam spline pinned support node.

    Set displacement.
    Enforce continuity of slope and moment.

    Attributes
    ----------
    displacement
        Support displacement at the node.
    """

    displacement: float

    def get_conjugation_eq(self) -> list[TMMEquation]:
        """Return the conjugation equations connecting elements."""
        in_el = self.inbound_elements[0]
        out_el = self.outbound_elements[0]

        return [
            TMMEquation(
                (in_el, ElementEdge.END, BEAM_DISPLACEMENT, 1),
                self.displacement,
            ),
            TMMEquation(
                (out_el, ElementEdge.START, BEAM_DISPLACEMENT, 1),
                self.displacement,
            ),
            _continuity_equation(in_el, out_el, BEAM_SLOPE),
            _continuity_equation(in_el, out_el, BEAM_MOMENT),
        ]


@dataclass(slots=True, init=False)
class BeamElasticSupport(BeamSplineNode):
    """Beam spline elastic support node.

    Set the force change proportional to the difference between
    the support displacement and the beam displacement.
    Enforce continuity of displacement, slope and moment.

    Attributes
    ----------
    displacement
        Support displacement at the node.
    next_length
        The length of the outbound element.
        The support stiffness adapts proportional to this value.
    bandwidth
        A smoothing bandwidth (g) that controls the support stiffness.
    """

    displacement: float
    next_length: float
    bandwidth: float

    def get_conjugation_eq(self) -> list[TMMEquation]:
        """Return the conjugation equations connecting elements."""
        in_el = self.inbound_elements[0]
        out_el = self.outbound_elements[0]

        k = self.next_length / self.bandwidth ** 4

        return [
            _continuity_equation(in_el, out_el, BEAM_DISPLACEMENT),
            _continuity_equation(in_el, out_el, BEAM_SLOPE),
            _continuity_equation(in_el, out_el, BEAM_MOMENT),
            TMMEquation(
                [
                    (in_el, ElementEdge.END, BEAM_FORCE, 1),
                    (out_el, ElementEdge.START, BEAM_FORCE, -1),
                    (out_el, ElementEdge.START, BEAM_DISPLACEMENT, -k),
                ],
                -k * self.displacement,
            ),
        ]


@dataclass(slots=True, init=False)
class BeamDummyNode(BeamSplineNode):
    """Beam spline dummy node.

    Enforce continuity of all beam state variables.
    """

    def get_conjugation_eq(self) -> list[TMMEquation]:
        """Return the conjugation equations connecting elements."""
        in_el = self.inbound_elements[0]
        out_el = self.outbound_elements[0]

        return [
            _continuity_equation(in_el, out_el, BEAM_DISPLACEMENT),
            _continuity_equation(in_el, out_el, BEAM_SLOPE),
            _continuity_equation(in_el, out_el, BEAM_MOMENT),
            _continuity_equation(in_el, out_el, BEAM_FORCE),
        ]


def _continuity_equation(in_el: int, out_el: int, var_i: int):
    return TMMEquation(
        [
            (in_el, ElementEdge.END, var_i, 1),
            (out_el, ElementEdge.START, var_i, -1),
        ],
        0,
    )
