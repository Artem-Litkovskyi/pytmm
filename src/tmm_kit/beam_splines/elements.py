from dataclasses import dataclass

import numpy as np

from tmm_kit.beam_splines.constants import BEAM_STATE_SIZE
from tmm_kit.tmm.base import TMMElement


@dataclass(slots=True)
class BeamElement(TMMElement):
    """Standard beam spline segment."""

    def get_transfer_eq(self, s: float) -> tuple[np.ndarray, np.ndarray]:
        """Return the transfer matrix K and right vector f."""
        K = np.array(
            [
                [1.0, s, s**2 / 2.0, s**3 / 6.0],
                [0.0, 1.0, s, s**2 / 2.0],
                [0.0, 0.0, 1.0, s],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )

        f = np.zeros(BEAM_STATE_SIZE, dtype=np.float64)

        return K, f


@dataclass(slots=True)
class BeamElementStretched(TMMElement):
    """Stretched beam spline segment.

    Attributes
    ----------
    stretching_force
        A force that pulls from the edges of the beam.
        Higher values result in higher curvature but shorter length.
    """

    stretching_force: float

    def get_transfer_eq(self, s: float) -> tuple[np.ndarray, np.ndarray]:
        """Return the transfer matrix K and right vector f."""
        N = self.stretching_force

        k = np.sqrt(N)

        ch_kx = np.cosh(k * s)
        sh_kx = np.sinh(k * s)

        K = np.array(
            [
                [1.0, s, (ch_kx - 1) / N, (sh_kx - k * s) / (k * N)],
                [0.0, 1.0, sh_kx / k, (ch_kx - 1) / N],
                [0.0, 0.0, ch_kx, sh_kx / k],
                [0.0, 0.0, k * sh_kx, ch_kx],
            ],
            dtype=np.float64,
        )

        f = np.zeros(BEAM_STATE_SIZE, dtype=np.float64)

        return K, f


@dataclass(slots=True)
class BeamElementCompressed(TMMElement):
    """Compressed beam spline segment.

    Attributes
    ----------
    compressing_force
        A force that pushes from the edges of the beam.
        Higher values result in lower curvature but longer length.
    """

    compressing_force: float

    def get_transfer_eq(self, s: float) -> tuple[np.ndarray, np.ndarray]:
        """Return the transfer matrix K and right vector f."""
        N = self.compressing_force

        k = np.sqrt(N)

        cos_kx = np.cos(k * s)
        sin_kx = np.sin(k * s)

        K = np.array(
            [
                [1.0, s, (cos_kx - 1) / N, (sin_kx - k * s) / (k * N)],
                [0.0, 1.0, sin_kx / k, (cos_kx - 1) / N],
                [0.0, 0.0, cos_kx, sin_kx / k],
                [0.0, 0.0, k * sin_kx, cos_kx],
            ],
            dtype=np.float64,
        )

        f = np.zeros(4, dtype=np.float64)

        return K, f


@dataclass(slots=True)
class BeamElementOnElasticFoundation(TMMElement):
    """Smoothing beam spline segment on elastic foundation.

    Attributes
    ----------
    start_foundation
        Foundation displacement at the start of the beam.
    end_foundation
        Foundation displacement at the end of the beam.
    bandwidth
        A smoothing bandwidth (g) that controls the foundation stiffness.
    """

    start_foundation: float
    end_foundation: float
    bandwidth: float

    def get_transfer_eq(self, s: float) -> tuple[np.ndarray, np.ndarray]:
        """Return the transfer matrix K and right vector f."""
        g = self.bandwidth

        ksi = s / np.sqrt(2) / g

        g2 = g * g
        g3 = g2 * g
        g4 = g3 * g

        cos_ksi = np.cos(ksi)
        sin_ksi = np.sin(ksi)

        ch_ksi = np.cosh(ksi)
        sh_ksi = np.sinh(ksi)

        k1 = ch_ksi * cos_ksi
        k2 = g / np.sqrt(2) * (sh_ksi * cos_ksi + ch_ksi * sin_ksi)
        k3 = g2 * sh_ksi * sin_ksi
        k4 = g3 / np.sqrt(2) * (ch_ksi * sin_ksi - sh_ksi * cos_ksi)

        K = np.array(
            [
                [k1, k2, k3, k4],
                [-k4 / g4, k1, k2, k3],
                [-k3 / g4, -k4 / g4, k1, k2],
                [-k2 / g4, -k3 / g4, -k4 / g4, k1],
            ],
            dtype=np.float64,
        )

        a = self.start_foundation
        b = (self.end_foundation - self.start_foundation) / self.length

        f = np.array(
            [
                a * (1 - k1) + b * (s - k2),
                a / g4 * k4 + b * (1 - k1),
                a / g4 * k3 + b / g4 * k4,
                a / g4 * k2 + b / g4 * k3,
            ],
            dtype=np.float64,
        )

        return K, f
