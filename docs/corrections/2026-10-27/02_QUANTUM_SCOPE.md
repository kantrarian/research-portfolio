# Quantum: exact identity versus model-dependent transition probability

Technical correction, 2026-10-27. Supersedes the universal pointwise-law and
spectral lower-bound wording in the v2 public manuscript. The revised source
and numerical scope checks are in `kantrarian/lambda-t-control`.

For a fixed Pauli basis, `B=H/hbar=(Delta sigma_z+Omega sigma_x)/2`, with
constant positive `Omega`, the operator-norm identity is exact:

$$
\Lambda(t)=\|[B,\dot B]\|_{op}=\tfrac12\Omega|\dot\Delta(t)|.
$$

With angular frequency measured in inverse time, `Lambda` has units
inverse-time cubed. It measures noncommuting generator change. In this model
it is exactly a rescaled detuning slope, not an additional independent
predictor. It is not itself an excited-state population or a guaranteed
advance warning of leakage. A two-level excited-state transition is not
automatically leakage outside a computational subspace in a multilevel qubit.

## Probability scope

For an infinite linear single crossing, with the standard asymptotic
preparation and constant coupling, the Landau-Zener result is

$$
P_{LZ}=\exp[-\pi\Omega^2/(2|\dot\Delta|)]
       =\exp[-\pi\Omega^3/(4\Lambda)].
$$

For a finite nonlinear pulse, denote substitution of the crossing slope into
that expression by `P_slope`, a **surrogate**, not an exact transition law.
It needs a nonzero approximately linear crossing over the relevant transition
time and appropriate endpoint preparation. Full pulse shape, endpoints,
interference, and higher levels can matter. The crossing value is not
necessarily the maximum of `Lambda`: the Gaussian-flattened example has a
local **minimum** of slope there.

A diagnostic counterexample uses nondimensional `Omega=1`, `Delta=t^3`,
`t in [-30^(1/3),30^(1/3)]`, initial instantaneous ground state and final
instantaneous excited-state projection. `Lambda(0)=0`, while direct TDSE
integration gives about `0.109231704` excited-state probability. Two solver
tolerances agree to better than `1e-9`. This invalidates a universal
crossing-slope law, not the exact commutator identity. Nonlinear crossing
effects are established in [Vitanov and Suominen (1999)](https://arxiv.org/abs/quant-ph/9811065).

## Fourier bound and direction of inequality

Under Fourier inversion with
`hat(Delta) in L1((1+|omega|) d omega)`, define
`M = integral |omega| |hat(Delta)(omega)| d omega`. Then

$$
\Lambda(t)\le U=\frac{\Omega M}{4\pi}.
$$

Since `exp(-a/x)` increases with positive `x`, the consequence is

$$
P_{slope}\le\exp[-\pi\Omega^3/(4U)]
              =\exp[-\pi^2\Omega^2/M],
$$

not a lower bound. This bounds the surrogate only, unless a separate error
bound connects that surrogate to actual dynamics. It is not a fundamental
minimum achievable leakage. The same direction applies after replacing
`M` by `omega_c ||hat(Delta)||_1` under the stated bandlimit.

For step-like sweeps it is often better to apply Fourier inversion to
`g=dot(Delta)`: if `g` is continuous with `g` and `hat(g)` integrable, then
`Lambda <= Omega ||hat(g)||_1/(4 pi)`. Integrability of `g` alone does not
imply integrability of `hat(g)`. An infinite linear sweep does not meet these
pulse-integrability assumptions. Do not silently combine the exact linear
scattering theorem with a different pulse class.

## Retained evidence

The archived 90-run data support the identity numerically and report maximum
absolute log-probability residuals about `0.000574` (linear), `0.002221`
(tanh), and `0.083920` (Gaussian-flattened) against the slope surrogate.
The three scaled coupling branches are not independent datasets. Three
matched-duration comparisons report reductions about `8.0`, `5713.3`, and
`349.2`; these are results for those specified noiseless two-level schedules,
not a universal exponential benefit or hardware-control demonstration.
The correction preserves those archived observations without upgrading their
scope. The new cubic case is a post-review falsification test, not a
preregistered extension of the old sweep.
