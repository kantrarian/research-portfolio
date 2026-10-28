# QUBO: objective definitions and quantum-estimation scope

Technical correction, 2026-10-27. Supersedes conflicting sign, indexing,
information-theoretic and Hadamard-test statements in the historical public
paper. The corrected definitions below are not a reproduction of its IEEE
network experiments or a recovered version of their generating pipeline.

## 1. Distinguish the optimization problems

For nonnegative stress weights `w_i`, binary sensor decisions `x_i`, sensor
budget `k`, and fixed coverage incidence `M_ij=1[d(i,j)<=r]`:

1. Topological weighted coverage maximizes `sum w_i z_i`, with binary `z_i`,
   `z_i <= sum_j M_ij x_j`, and `sum x_i=k`.
2. Stress-weighted coverage uses the same constraints but weights from a
   **training-only** contingency library. It is not pairwise dispersion.
3. Worst uncovered stress minimizes `max_i w_i(1-z_i)` under those constraints.
   An exact formulation uses an epigraph `t >= w_i(1-z_i)`; a finite search
   over `t in {0,w_1,...,w_n}` can instead require coverage of every `w_i>t`.
4. A pairwise entropy-redundancy surrogate maximizes
   `sum H_i x_i - beta sum_(i<j) I_ij x_i x_j`. It is **not** generally the
   mutual information between the sensor set and a latent field.

The dispersion benchmark is a distinct fifth objective:
`V(x)=sum w_i x_i + alpha sum_(i<j) d_ij x_i x_j`. Do not label its coefficients
as an encoding of coverage or minimax. State the distance/weight normalization
and the units or conversion weights on every objective term.

Coverage inequalities require actual encodings. One option adds nonnegative
integer slack `s_i` and penalties
`lambda_c (sum_j M_ij x_j-z_i-s_i)^2`, with `s_i` represented in binary over
a sufficient finite range. Thus the qubit/variable count is not automatically
`2n`: it includes the slack bits (and a minimax epigraph encoding if used).
Other quadratizations must specify their ancillas and verify their minima.

## 2. One unambiguous dispersion QUBO

Minimize

$$
E(x)=-\sum_iw_ix_i-\alpha\sum_{i<j}d_{ij}x_ix_j
          +\lambda(\sum_i x_i-k)^2.
$$

Use upper-triangle coefficients, with each pair counted once:

$$
q_{ii}=-w_i+\lambda(1-2k),\quad
q_{ij}=2\lambda-\alpha d_{ij}\;(i<j),\quad c=\lambda k^2,
$$
$$
E(x)=c+\sum_iq_{ii}x_i+\sum_{i<j}q_{ij}x_ix_j.
$$

There is no outer minus sign and no second cardinality penalty. A symmetric
matrix representation `x^T Q x+c` instead has `Q_ij=q_ij/2` off diagonal.
For the pairwise information surrogate use `q_ii=-H_i+lambda(1-2k)` and
`q_ij=beta I_ij+2 lambda`. Its redundancy term has the opposite sign to the
dispersion reward.

With `x_i=(1-z_i)/2`, the exact Ising coefficients are

$$
h_i=-q_{ii}/2-\tfrac14\sum_{j\ne i}q_{\min(i,j),\max(i,j)},\quad
J_{ij}=q_{ij}/4,
$$
$$
c_I=c+\tfrac12\sum_iq_{ii}+\tfrac14\sum_{i<j}q_{ij}.
$$

Track the constants when comparing energies. Test equality for **all** bit
strings of a small fixture, not only feasible strings.

## 3. Penalty sufficiency

Enumeration of `choose(33,5)` feasible states checks constrained rankings;
the penalty is zero on all of them. It cannot show that an unconstrained
minimum is feasible. A simple conservative sufficient bound for dispersion is

$$
\lambda>\sum_i|w_i|+|\alpha|\sum_{i<j}|d_{ij}|.
$$

Proof: the range of the unpenalized quadratic reward over all bit strings is
at most the right-hand side; every infeasible cardinality has squared integer
violation at least one. Its penalty then exceeds any possible reward advantage
over a feasible state. Require integer `0<=k<=n`. Tighter bounds or exhaustive
small-instance checks are welcome, but feasible-only enumeration cannot
replace them. Very large penalties can impair numerical conditioning and
optimization; sufficiency does not imply an efficient solver choice.

## 4. A well-defined Gaussian information target

The full Laplacian pseudoinverse covariance is singular. An unqualified
`log det(Sigma_full)/det(Sigma_full|S)` is therefore not valid; its displayed
Schur complement also changes dimension. Observing a noiseless continuous
subset of the full field makes `I(field_subset; full_field)` generally
infinite, not a finite entropy ratio repaired by pseudodeterminants.

Use a declared Gaussian latent field `z~N(0,Sigma)` on a specified support,
and `y_S=H_S z+epsilon_S`, where independent observation noise has positive
definite covariance `R_S`. Then, in nats,

$$
I(z;y_S)=\tfrac12\log\det\!\left(I+
 R_S^{-1/2}H_S\Sigma H_S^T R_S^{-1/2}\right).
$$

This is finite even when `Sigma` is positive semidefinite and singular.
Declare the graph gauge/mean constraint or regularization, the fixed stress
weights, the selection operator, the noise units, and any covariance estimator.
Do not identify this graph prior with empirical Lambda values.

For noisy scalar Gaussian observations with correlation `rho_ij`, pairwise
`I_ij=-0.5 log(1-rho_ij^2)` is valid. Differential marginal entropy `H_i`
depends on the declared measurement units/reference scale. Pairwise penalties
omit higher-order dependence and need not rank sets like the exact log-det
objective. The exact information objective is monotone submodular with
conditionally independent sensor noise given the latent field; the associated
greedy guarantee does not transfer to arbitrary pairwise surrogates or a
dispersion optimizer. Nor does a centered `L+` covariance alone establish the
paper's asserted tree conditional-independence law. See the distinct sensor-
placement formulation in [Krause et al. (2008)](https://jmlr.org/papers/v9/krause08a.html).

## 5. What a group-commutator Hadamard test measures

For Hermitian `A,B`, normalized `psi`, `C=[A,B]`, and
`U(t)=exp(-iAt) exp(-iBt) exp(iAt) exp(iBt)`,

$$
\operatorname{Re}\langle\psi|U(t)|\psi\rangle
 =1-\tfrac12 t^4\langle\psi|C^\dagger C|\psi\rangle+O(t^5).
$$

The leading deficit is fourth order with coefficient one half, not second
order. This follows immediately from unitarity:
`1-Re<psi|U|psi> = 0.5 ||(U-I)psi||^2`, and `U-I=-t^2 C+O(t^3)`.
It estimates a state-dependent norm, not the Frobenius norm without a trace
estimator/basis average. A bus-specific basis expectation selects a column
norm; equating that to row attribution additionally requires structure such
as skew-Hermiticity. Finite-time bias and shot uncertainty must be included.
For elementary independent bounded-shot averaging, resolving an absolute
error `epsilon` in the coefficient has a sufficient Hoeffding-style budget
of order `t^(-8) epsilon^(-2) log(1/delta)`; this is not a lower bound or the
best possible quantum algorithm.

A generic power-flow Jacobian is not Hermitian; `exp(i J t)` is not generally
unitary. A Hermitian dilation changes the operator and its commutator, so its
mapping back to the claimed diagnostic must be proved. No universal 50,000-bus
crossover, one-shot measurement, or hardware advantage follows from this
expansion. State preparation, encoding, evolution, shots, bias, precision,
sparsity and the classical baseline all belong in a resource comparison.

## Acceptance and remaining evidence

Executable checks cover polynomial/upper/symmetric/Ising equivalence,
infeasible-state penalty competition, noisy Gaussian information with singular
latent covariance, and fourth-order unitary scaling. They do not reproduce
the archived network tables, cascade ensemble, QAOA success rates, or topology
claims. Those claims need the actual objective builders, input matrices,
sensor sets, simulator settings and seeds before being advertised as verified.
