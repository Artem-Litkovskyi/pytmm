from tmm_kit.beam_splines.constants import (
    BEAM_DISPLACEMENT,
    BEAM_FORCE,
    BEAM_MOMENT,
    BEAM_SLOPE,
)
from tmm_kit.tmm.base import ElementEdge, TMMEquation


def pinned_ends(start_displacement, end_displacement):
    """Pinned supports at both ends (zero moments)."""
    return [
        TMMEquation((0, ElementEdge.START, BEAM_DISPLACEMENT, 1), start_displacement),
        TMMEquation((-1, ElementEdge.END, BEAM_DISPLACEMENT, 1), end_displacement),
        TMMEquation((0, ElementEdge.START, BEAM_MOMENT, 1), 0),
        TMMEquation((-1, ElementEdge.END, BEAM_MOMENT, 1), 0),
    ]


def clamped_ends(
    start_displacement, end_displacement,
    start_slope=0, end_slope=0,
):
    """Clamped supports at both ends."""
    return [
        TMMEquation((0, ElementEdge.START, BEAM_DISPLACEMENT, 1), start_displacement),
        TMMEquation((-1, ElementEdge.END, BEAM_DISPLACEMENT, 1), end_displacement),
        TMMEquation((0, ElementEdge.START, BEAM_SLOPE, 1), start_slope),
        TMMEquation((-1, ElementEdge.END, BEAM_SLOPE, 1), end_slope),
    ]


def free_ends():
    """No supports at both ends (zero moments and forces)."""
    return [
        TMMEquation((0, ElementEdge.START, BEAM_MOMENT, 1), 0),
        TMMEquation((-1, ElementEdge.END, BEAM_MOMENT, 1), 0),
        TMMEquation((0, ElementEdge.START, BEAM_FORCE, 1), 0),
        TMMEquation((-1, ElementEdge.END, BEAM_FORCE, 1), 0),
    ]
