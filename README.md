# Universe 005 — Great Recursion Laboratory

Interactive browser-based **tutorial and experimentation dashboard** for the Universe 005 research program.

**[Open index.html](index.html)** · [EFMW candidate-law audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/docs/CANDIDATE_LAWS.md) · [Two Paths to Rotation](https://github.com/enuminous/papers/blob/main/Two-Paths-to-Rotation.md) · [Primordial Recursion R-001](https://github.com/enuminous/papers/blob/main/EFMW-Zoo-R001-Primordial-Recursion-Boundary.md)

## Launch

Open `index.html` in your browser after downloading or cloning the repository. The site is self-contained and does not require a server or dependencies. To publish it online, in repository **Settings → Pages**, choose **Deploy from a branch → main → /(root)** if that option is available for your account. Once deployed, the expected GitHub Pages address is `https://enuminous.github.io/Universe5/` (not yet verified as live).

## What the dashboard does

- Reproducible seeded initial conditions, with isotropic, biased, and zero-spin controls.
- Browser-based softened Newtonian N-body gravitational motion using velocity-Verlet/leapfrog.
- Spin axes with quaternion orientation updates compatible with the standard Spin(3) rotation representation.
- Interactive visualization of motion, stepwise relative energy error, momentum, orbital angular momentum, rotor normalization, and axial alignment.
- An independent scalar-wave **diagnostic only** (no back-reaction), with full JSON export.
- Guided tutorial, scientific-status ledger, and links to underlying research.

## Limitations

The UI is **an independent educational toy implementation**, not a browser port or proof of the prior Universe 005 Python calculation. It does not simulate black-hole horizons, relativistic mergers, photons or light pressure, an action-derived EFMW coupling, cosmic-scale vorticity, or a nonsingular rebound. Spin orientation updates are not dynamical spin-orbit interactions. Energy diagnostics concern the softened Newtonian particle sector only. A 6-sigma observational match has not been established.

## Research next steps

1. Verify independently conserved matter-plus-radiation energy/momentum accounting.
2. Implement covariant scalar-matter coupling *from an explicitly frozen action*, not an arbitrary force.
3. Replace softened Newtonian compact objects with validated relativistic approximations where justified.
4. Specify the high-curvature transition, derive and test its constraint preservation.
5. Freeze independent observable predictions before comparing to CMB or survey data.

## Source / credits

Research program: Matthew Chenoweth Wright, Monolithic LLC. Clifford-rotation discussion draws on the attributed work of Chris Forrester and the [joint discussion draft](https://github.com/enuminous/papers/blob/main/Two-Paths-to-Rotation.md), whose coauthorship status remains pending Chris's acceptance. All claims about physical validation are explicitly provisional.
