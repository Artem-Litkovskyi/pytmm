# Beam Spline System via Transition Matrix Method

## Overview
This document outlines a mathematical framework for solving a continuous Euler-Bernoulli beam (a beam spline) constrained by specific node points using the **Transition Matrix Method (TMM)**. 

By preserving the full state vectors at both ends of every segment (avoiding simplifications like the Three Moments Equation), this approach allows for the easy introduction of discontinuities, such as internal hinges or stepped displacements, later on.

## State Vector
The beam state at any cross-section is defined by the vector $W$:
$$ W = \begin{Bmatrix} w \\ \theta \\ M \\ Q \end{Bmatrix} $$
Where:
*   **$w$**: Displacement (directed along the y-axis)
*   **$\theta$**: Slope (rotation)
*   **$M$**: Bending moment
*   **$Q$**: Shear force

## Problem Geometry
*   The beam is divided into $N$ segments, conjugated at $N+1$ node points at coordinates $t_i$.
*   Each segment $i$ has two ends, represented by states $W_0^i$ (start) and $W_e^i$ (end).
*   The length of the $i$-th segment is $L_i = t^{i+1} - t^i$.
*   This setup yields a total of **$2N$ state vectors**, or **$8N$ total unknowns**. To solve the system, we must construct exactly $8N$ linearly independent equations.

---

## 1. Standard Transition Equations (4N equations)
For each segment, the state at the end is related to the state at the start via the transition matrix $A(L_i)$:

$$ W_e^i = A(L_i) \cdot W_0^i $$

When rearranged into the global matrix system as $W_e^i - A(L_i) \cdot W_0^i = 0$, this provides **4 equations per segment** (total of $4N$ equations).

For a standard Euler-Bernoulli beam with constant stiffness $EI$, the matrix $A(l)$ is:
$$ A(t) = \begin{bmatrix} 
1 & l & \frac{l^2}{2EI} & \frac{l^3}{6EI} \\ 
0 & 1 & \frac{l}{EI} & \frac{l^2}{2EI} \\ 
0 & 0 & 1 & l \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $$

where $l \in [0; L_i]$ is a local coordinate.

After the beam is solved and all $W_0^i$ are known, the same transition matrix can be used to **evaluate** the beam state $W$ in any point.

---

## 2. Standard Conjugation Equations (4N - 4 equations)
At each of the $N-1$ internal nodes, the end of the $i$-th segment meets the start of the $(i+1)$-th segment. To interpolate points $(t_i; \Pi_i)$ we construct such equations:

1.  **End of previous segment hits the node:**
    $$ w_e^i = \Pi_{i+1} $$
2.  **Start of next segment hits the node:**
    $$ w_0^{i+1} = \Pi_{i+1} $$
3.  **Slope is continuous across the node:**
    $$ \theta_0^{i+1} - \theta_e^i = 0 $$
4.  **Moment is continuous across the node:**
    $$ M_0^{i+1} - M_e^i = 0 $$

*Note: The shear forces $Q_e^i$ and $Q_0^{i+1}$ are intentionally uncoupled. The difference between them after the matrix is solved will naturally equal the vertical reaction force of the node.*

This provides **4 equations per internal node**, totaling $4(N-1) = 4N - 4$ equations.

---

## 3. Extra Boundary Conditions (4 equations)
To make the final system square ($8N$ equations for $8N$ unknowns), we must apply boundary conditions to the global start and end nodes.

1.  **First node displacement:** $w_0^0 = \Pi_0$
2.  **Last node displacement:** $w_e^{N-1} = \Pi_N$
3.  **First node moment (e.g., pinned):** $M_0^0 = 0$
4.  **Last node moment (e.g., pinned):** $M_e^{N-1} = 0$

*(These can be swapped for clamped conditions, e.g., $\theta_0^0 = 0$, depending on the required boundary type).*

---

## Summary of the Global System
The final linear system takes the form of $K \cdot X = F$, where $K$ is an $8N \times 8N$ sparse matrix, $X$ is the vector of all $8N$ unknown states, and $F$ is the load/boundary vector.

| Equation Type         | Count    |
|:----------------------|:---------|
| Transition Equations  | $4N$     |
| Conjugation Equations | $4N - 4$ |
| Boundary Conditions   | $4$      |
| **Total Equations**   | **$8N$** |

With the shear constraints correctly relaxed at the nodes, the matrix $K$ will be non-singular and solvable via standard sparse linear algebra routines (e.g., `scipy.sparse.linalg.spsolve`).