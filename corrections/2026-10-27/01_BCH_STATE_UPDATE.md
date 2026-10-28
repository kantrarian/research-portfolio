# BCH: corrected state and update derivation

Technical correction, 2026-10-27. This supplements the historical
`patents/BCH_Provisional_Patent.pdf`; it is not an amendment to a filing or a
statement about patent validity. Previously reported timings and error rates
are not validation of the corrected algorithm below.

## 1. Preserve the state, not just its eigenvalues

Use the multiplicative decomposition `F = Fe Fp`, with
`Lp = dot(Fp) inv(Fp)` represented in one fixed intermediate frame.
`F`, `Fe`, and `Fp` are dimensionless invertible maps with positive determinant;
`Lp` has units inverse time. Define

$$
C_e=F_e^T F_e\in\mathrm{SPD}(3),\qquad E_e=\tfrac12\log C_e\in\mathrm{Sym}(3).
$$

The numerical state retains `Fp` and the full elastic deformation `Fe`, or
enough information to recover them from `F`. Strain `Ee` alone is insufficient:
`Fe = Re Ue`, and `Ce = Ue^2` discards the elastic rotation `Re`. Recovering
`sqrt(Ce)` is not recovering `Fe`. Lattice orientation cannot be silently reset.

## 2. The exact frozen-generator reference

At prescribed new total deformation `Fnew`, define
`Fe_trial = Fnew inv(Fp_old)`. Freeze `Lp` during a step of length `h`:

$$
F_p^{new}=e^{hL_p}F_p^{old},\qquad
F_e^{new}=F_e^{trial}e^{-hL_p},
$$
$$
C_e^{new}=e^{-hL_p^T}C_e^{trial}e^{-hL_p},\qquad
E_e^{new}=\tfrac12\log\!\left(e^{-hL_p^T}e^{2E_e^{trial}}e^{-hL_p}\right).
$$

Multiplying `Fe_new Fp_new` recovers `Fnew`. The congruence preserves positive
definiteness. If `trace(Lp)=0`, it also preserves `det(Fp)` in exact arithmetic.
This is exact for the **frozen-generator kinematic substep**, not an exact
solution of a coupled, state-dependent constitutive problem. It is not the
backward-Euler update `(I-h Lp)^(-1) Fp_old`. A constitutive solve still needs
its own integration, consistency, stress and tangent-error controls.

A BCH representation, when its local convergence/logarithm conditions hold,
must represent the sandwich product:

$$
2E_e^{new}=\mathrm{BCH}\left(-hL_p^T,
                 \mathrm{BCH}(2E_e^{trial},-hL_p)\right).
$$

`BCH(E_trial,-h Lp)` describes a different product and is not this strain.
Independent truncations need not preserve symmetry; the SPD reference above
is the acceptance oracle for any proposed acceleration.

Even a symmetric positive-definite trial `Fe_trial = exp(E_trial)` is not
enough to make the product logarithm a strain. For `E_trial=diag(.3,-.2,0)`,
symmetric `Lp[0,1]=Lp[1,0]=1` (other entries zero), and `h=.1`, the product
`exp(E_trial) exp(-h Lp)` is nonsymmetric. Its logarithm has symmetry defect
about `0.0707087` and differs from the Hencky sandwich result by about
`0.0365688`. Symmetry of each factor is not commutativity of the factors.

## 3. What the first-order derivative actually is

Let `Lp = D + W`, with `D` symmetric and `W` skew symmetric. In an orthonormal
eigenbasis of `E_trial`, write its eigenvalues as `e_i`, and `c_i=exp(2 e_i)`.
The exact first variation follows from

$$
\dot C_e=-L_p^TC_e-C_eL_p,\qquad
\dot E_e=\tfrac12 D\log_{C_e}[\dot C_e].
$$

For `i != j`, with `g=e_i-e_j`,

$$
(\dot E_e)_{ij}=-g\coth(g)D_{ij}-gW_{ij},\qquad
(\dot E_e)_{ii}=-D_{ii}.
$$

Use the continuous limit `g coth(g) -> 1` for repeated eigenvalues. This
derivative is symmetric. Near small spectral gaps its expansion is

$$
\dot E_e=-D+[W,E_e]-\tfrac13[E_e,[E_e,D]]+\cdots.
$$

Thus even the spin-free case does not have a first-order correction
proportional to the skew matrix `[E,D]` alone. This derivation is a local
kinematic result, not a new universal error bound.

## 4. A valid additive branch, and a counterexample to the old gate

An exact sufficient condition for the frozen step is `W=0` and `[E_trial,D]=0`.
Then all three symmetric exponents commute and
`E_new = E_trial - h D`. Even then, retain the full multiplicative state.
Numerically small spin/commutator is **not** an exact condition or a certified
error tolerance; an approximation needs a bound or a checked local error.

Counterexample: take `E_trial=0`, `Fe_trial=I`, `Lp[0,1]=1`, all other entries
zero, and `h=0.1`. The diagnostic `||[E_trial,Lp]||` is zero, but the printed
additive update `-h Lp` is nonsymmetric. Its symmetry defect is
`0.1414213562`, and its Frobenius difference from the exact Hencky strain is
about `0.0707988156`. A zero commutator has not certified a valid strain update.
For pure spin, the correct strain evolution is a conjugation
`E_new = exp(h W) E_trial exp(-h W)`, not subtraction of a skew strain.

## 5. Claims to replace

- Interpret `||[E,Lp]||` as a frame-declared diagnostic, not sectional curvature
  on `GL(3)` or `SL(3)` with the Frobenius metric. The familiar positive
  commutator sectional-curvature formula requires a bi-invariant Riemannian
  metric; it does not apply to these kinematics as printed. Orthogonal vectors
  also need their norm factors in the sectional denominator.
- The difference between the two displayed truncated formulas is
  `0.5 h ||[E,Lp]||` when they differ only by that term. It is neither a
  quadratic error law nor error against the physical sandwich update.
- `h ||[E,Lp]||` is dimensionless. A threshold on it cannot be justified by
  equating it to an unscaled average of `||[E,Lp]||`, which has inverse-time
  units. An empirical gate needs its exact dimensionless normalization,
  population and independent error validation.
- Withdraw universal scaling, zero-false-negative and FE-squared speedup
  assurances from the current summary. Re-evaluate them with the corrected
  state, physical reference, constitutive residual and matched tolerances.

## Acceptance

The companion reference tests check state reconstruction, symmetry/SPD,
plastic-volume preservation, retained rotation, the commuting symmetric
branch, the spin counterexample, and the first-variation formula against
finite differences. These are mathematical/software checks, not a material
benchmark, solver-speed study, or validation of historical quantitative claims.
