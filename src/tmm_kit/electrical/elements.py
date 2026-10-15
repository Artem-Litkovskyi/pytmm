from dataclasses import dataclass

import numpy as np

from tmm_kit.tmm.base import TMMElement


@dataclass(slots=True)
class ElectricalElement(TMMElement):
    """Electrical circuit element."""

    resistance: float
    voltage: float

    def get_transfer_eq(self, s: float) -> tuple[np.ndarray, np.ndarray]:
        """Return the transfer matrix K and right vector f."""
        K = np.array(
            [
                [1.0, -self.resistance],
                [0.0, 1.0],
            ],
            dtype=np.float64,
        )

        f = np.array(
            [
                self.voltage,
                0.0,
            ],
            dtype=np.float64,
        )

        return K, f
