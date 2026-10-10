# AI Agent Guidelines

This document outlines the architectural patterns and mathematical precision rules for this project. 

## 1. Core Stack
* **Language:** Python 3.13
* **Libraries:** `numpy` (calculations/arrays), `scipy` (advanced math/spatial).

## 2. Type Hinting & Precision
* **Arrays:** Use `np.ndarray | Sequence[float]`.
* **Scalars:** Use Python's built-in `float` for scalar type hints, not `np.float64`.
* **Input Boundaries:** Functions accepting arrays must allow flexible sequence inputs and normalize them internally using `np.asarray(points, dtype=np.float64)`.

## 3. Documentation
* **Format:** Strictly use **NumPy-style** docstrings. Do not duplicate types in the docstring; let Python type hints in the signature act as the single source of truth.
* **Content:** All public and private functions require comprehensive docstrings detailing mathematical constraints, expected coordinate frames, and expected array shapes (e.g., `(N, 3)`). If the function is simple and arguments are self-explanatory, the `Prameters` and `Returns` sections can be omitted.

## 4. Post-Editing Actions
* **Linting:** Run `ruff check --fix .`.

## 5. Standard Code Template Example

```python
from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
from scipy.spatial.transform import Rotation


def generate_sweep_surface(
    profile_curve: np.ndarray | Sequence[float],
    path_curve: np.ndarray | Sequence[float],
) -> np.ndarray:
    """
    Generate a 3D sweep surface by extruding a profile along a path.
    
    Parameters
    ----------
    profile_curve
        2D or 3D coordinates forming the cross-section profile. 
        Expected shape (M, 2) or (M, 3).
    path_curve
        3D coordinates representing the generation path. 
        Expected shape (N, 3).
        
    Returns
    -------
    FloatArrayNumpy
        3D mesh grid representing the evaluated surface with shape (N, M, 3).
    """
    profile = np.asarray(profile_curve, dtype=np.float64)
    path = np.asarray(path_curve, dtype=np.float64)

    # Implementation follows...
    return np.zeros((len(path), len(profile), 3), dtype=np.float64)
```