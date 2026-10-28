# Technical Corrections and Evidence Status

October 27, 2026. This is a technical repair set, not publication acceptance,
patent clearance, a new confirmatory study, or certification of the portfolio.

1. [BCH state and update](01_BCH_STATE_UPDATE.md): multiplicative state,
   SPD sandwich logarithm, exact first variation, spin/rotation handling,
   valid commuting branch and retirement of unsupported error guarantees.
2. [Quantum claim scope](02_QUANTUM_SCOPE.md): exact identity versus slope
   surrogate, corrected upper-bound direction, Fourier hypotheses and a
   cubic-crossing counterexample. [Revised v3 paper](../../papers/Quantum_Dynamics_Spectral_Curvature_v3.pdf).
3. [Finance population](03_FINANCE_POPULATION.md): signal-independent event
   membership, explicit misses and missing coverage, consistent estimands,
   clocks, model identity and honest ablation scope.
4. [QUBO objectives](04_QUBO_OBJECTIVES.md): distinguish coverage, minimax,
   dispersion and pairwise information surrogates; correct encodings,
   penalties, information target and quantum-estimation expansion.

## Checks and limits

`reference_checks.py` and `test_reference_checks.py` contain small numerical
oracles and 14 tests for the BCH/QUBO corrections. Run from the repository root:

```powershell
python -m unittest discover -s corrections/2026-10-27 -p test_*.py -v
```

Requires numpy and scipy. They check equations and structural invariants, not
FE-squared speed, grid forecasting, financial returns or quantum advantage.
The quantum companion adds five scope checks, including two TDSE tolerances;
its archived 90-run data are checked for reported residual consistency, not
presented as a new independent cohort.

## Reconciled summaries

The portfolio README and both dashboard copies remove unsupported universal
and performance assurances. Grid v15 and other unrevised PDFs are labeled
historical; GeoSpec is described as observational research, not a validated
forecast. No held successor patent/grid material or private financial data is
copied into this public-facing repair set. Patent PDFs remain byte-unchanged.

The older quantum PDF remains available at its old URL; current links select
the explicitly versioned v3. A direct link to any old PDF can bypass this
notice, so historical copies must not be redistributed as corrected editions.

## Remaining work before stronger claims

- BCH: integrate the correct state update into a constitutive solver, derive
  or measure its error control, and rerun matched-tolerance benchmarks.
- Quantum: validate any new pulse/control claim against full dynamics,
  operational constraints and suitable baselines.
- Finance: assemble and freeze a genuinely independent target population
  before confirmatory evaluation; do not relabel legacy development data.
- QUBO: reproduce the network results from actual objective builders,
  matrices, solver settings, seeds and cascade outcomes.
- Grid and other manuscripts: release an authorized corrected paper with
  its evidence, or retain the historical label. These corrections are not
  permission to disclose held material.
