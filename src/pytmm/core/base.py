from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias

import numpy as np


class ElementSide(StrEnum):
    """Side of an 1D element."""

    START = "start"
    END = "end"


# Format: (element_i, ElementSide, state_var_i, coefficient)
TMMEquationAddend: TypeAlias = tuple[int, ElementSide, int, float]


class TMMEquation:
    """An equation that can be added to the TMM equation system."""

    def __init__(
        self,
        left_side: TMMEquationAddend | Sequence[TMMEquationAddend],
        right_side: float,
    ):
        if isinstance(left_side, Sequence) and isinstance(left_side[0], tuple):
            self.left_side_addends = left_side
        else:
            self.left_side_addends = [left_side]
        self.right_side = right_side

    def __repr__(self) -> str:
        """Return an unambiguous representation of the equation."""
        return (
            f"{type(self).__name__}("
            f"left_side_addends={self.left_side_addends!r}, "
            f"right_side={self.right_side!r})"
        )


@dataclass(slots=True)
class TMMElement(ABC):
    """Abstract base class for all transfer matrix elements."""

    length: float

    @abstractmethod
    def get_transfer_eq(self, s: float) -> tuple[np.ndarray, np.ndarray]:
        """Return the transfer matrix K and right vector f.

        Parameters
        ----------
        s
            Local coordinate (from 0 to self.length).
        """
        pass


@dataclass(slots=True)
class TMMNode(ABC):
    """Abstract base class for nodes conjugating elements."""

    inbound_elements: list[int]
    outbound_elements: list[int]

    @abstractmethod
    def get_conjugation_eq(self) -> list[TMMEquation]:
        """Return the conjugation equations connecting elements."""
        pass

    @abstractmethod
    def get_conjugation_eq_n(self) -> int:
        """Return the number of conjugation equations."""
        pass
