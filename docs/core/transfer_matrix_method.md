# Transfer Matrix Method

Given a system of 1D elements connected at their edges:
- $\vec{Y}^i(s)$ – state ($N \times 1$ vector) of an $i$-th element at a point $s$.
- $\vec{Y}^i_0 = \vec{Y}^i(0)$ – state at the start of an $i$-th element.
- $\vec{Y}^i_e = \vec{Y}^i(s_e)$ – state at the end of an $i$-th element.

The system is described by such equations:
1. **Transfer equations**: the relation between $\vec{Y}^i_0$ and $\vec{Y}^i(s)$.
2. **Conjugation equations**: the relation between $\vec{Y}^i_e$ and $\vec{Y}^{i+1}_0(s)$.
3. **Boundary conditions**: $N/2$ additional equations per each boundary element.

## Transfer Equations

A state of an element at a certain point can be calculated by the transfer equation:

$$\vec{Y}^i(s) = A(s)\vec{Y}^i_0+\vec{B}(s)$$

The transfer matrix $A(t)$ and the vector $\vec{B}(t)$ are found analytically by the Krylov method for each problem individually (see `krylov_method.md`).

The state at the end of the element is:

$$\vec{Y}^i_e = A(s_e)\vec{Y}^i_0+\vec{B}(s_e)$$

## Conjugation Equations

### Two Consequent Elements

Is used for beam splines and other systems without branching.

To pass the state from the end of an element to the beginning of the next one a conjugation equation is used:

$$\vec{Y}^{i+1}_0 = C\vec{Y}^i_e+\vec{D}$$

The simplest case is when the state is continuous: then $C = I$ (identity matrix) and $\vec{D} = 0$.

However, for some problems (such as a beam supported at conjugation points) the matrix form of this equation can't be used. Then the single matrix equation is replaced by a system of $N$ regular  equations.

### Multiple Elements

Such cases are present in electrical circuits and pipeline modeling.

Let's say that the state consists of two groups of variables:
1. $I$ – Those that depend on direction (e.g., current or flow)
2. $E$ – Those that do not depend on direction (e.g., voltage or pressure)

For the first group:

$$\sum_1^k{I^i_e} + \hat{I} = \sum_{k+1}^N{I^i_0}$$

where $k$ is a number of inbound elements, $\hat{I}$ is an external factor.

For the second group:

$$E^1_e = E^2_e + \hat{E^2} = \dots = E^k_e + \hat{E^k} = E^{k+1}_0 + \hat{E^{k+1}} = \dots = E^{N}_0 + \hat{E^N}$$

where $\hat{E}$ is an external factor.