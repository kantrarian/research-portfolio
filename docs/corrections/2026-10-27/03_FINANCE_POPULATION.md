# Finance: evaluation population and method identity

Technical correction, 2026-10-27. The July 28 withdrawal of historical
detection-rate headlines remains in force. The v2 PDF's cover did not repair
the underlying evaluation definition or establish performance of a new model.

## Replace Definition 5.2

The paper's exclusion rule removes an event when both the pre-event maximum
Lambda signal and the correlation signal fall below their detection
thresholds. Those are exactly events the detector misses. Calling them
exogenous does not make the resulting sensitivity denominator independent.

Replacement: define the target event population using an external catalog or
a fully specified mechanical outcome rule, **without consulting any tested
signal, threshold crossing, detection result, or model score**. Freeze the
selection source, market universe, dates, event clustering, and exclusions
before confirmatory evaluation. Rules may use independently defined outcomes
to identify target events; they may not use the model's success on those
outcomes. A retrospective freeze is still retrospective, not preregistration.

Every target event remains visible in the ledger. Record `HIT`, `MISS`,
`UNSCORABLE`, or `PENDING` separately from population membership. Unknown
input availability is not a miss and not a negative signal. A signal-based
`EXCLUDED` status is prohibited. An outside-domain event may be excluded only
by an independently specified population rule, with its identity and reason
retained in the population audit, not decided after observing detector output.

Report total eligible population, scored count, unscorable/pending counts,
hits, misses, and scored recall `hits/(hits+misses)`. Also report conservative
all-population recall bounds `[hits/N, (hits+unscorable+pending)/N]` when
`N>0`; these are missing-outcome bounds, **not confidence intervals**.
Do not advertise scored recall without its coverage and unscorable reasons.

## Freeze the estimand and the clocks

- Event recall requires an independently enumerated event denominator.
  Alert precision uses emitted alert episodes; it cannot supply that denominator.
  Mechanical opportunity recall, named-event recall, and day-level alert
  occupancy are different quantities.
- State the channel and combination rule, threshold calibration history,
  persistence/merge rule, lead window, horizon, market, and model revision.
  A strict Q4 channel and a broad two-signal detector are not interchangeable.
- Specify calendar days versus trading sessions, feature availability,
  signal emission, execution price and execution delay. An end-of-day feature
  cannot imply a trade executed before it was available.
- Fix maturation/censoring at one as-of time. Do not prematurely compare
  resolved successes against still-open failures. Report survival/censoring
  assumptions where a resolved-only statistic is used.
- Compare models on a common independently specified evaluation population;
  show per-model availability separately. Purge overlapping outcome windows
  from fitting/calibration and use time/event-cluster uncertainty, not
  independent-day confidence intervals for overlapping 90-day outcomes.

## Identify the actual matrix pipeline

The paper's exponentially weighted covariance and the dashboard's Method C
are different algorithms. Method C smooths returns, standardizes each row
using its own trailing history, then computes a sample covariance over a
subsequent rolling window, differences adjacent matrices, normalizes the
commutator, applies `log1p(100 raw)`, a 14-session average and a two-session
lag. Bind a claim to the exact source/version, universe, missing-data rules,
window endpoint convention, percentile history and timestamps.

Important qualification to the review: covariance of **one consistently
standardized window** is a correlation matrix, but covariance of a sequence
whose rows were standardized against **different historical windows** is not
necessarily unit-diagonal. Therefore do not rename Method C a correlation
matrix without checking its construction. Neither implementation is silently
equivalent to the paper's EWMA equation.

`||[F,Fdot]||/(||F|| ||Fdot||+epsilon)` removes common magnitude factors when
epsilon is negligible; it is not an absolute rotation-speed measurement.
Changing units/scales relative to epsilon can change the value. Define zero
or near-zero derivative behavior, frame and asset-index consistency.

## Other withdrawn interpretations

Table 15 repeats the Lambda versus Lambda-plus-correlation comparison; it
does not identify a reflexivity-layer ablation. A proper test needs matched
Lambda-only, correlation-only, combined, reflexivity-only, and combined-plus-
reflexivity variants on the same frozen population, with multiplicity and
calibration controlled. The repeated table cannot establish incremental value.

The paper's conditional drawdown percentages likewise need a versioned
outcome ledger, full exposure denominator, clock rules and dependence-aware
uncertainty. A live dashboard does not restore withdrawn historical results,
and a later revised population does not retroactively validate them.

## Live scorecard correction

The public `vonlambda/lambda-f-dashboard` snapshot
`b5e79cf9b6077f9aeb56f7df6d7dcb06618253a2` also merged all calls before
assigning an episode to Q4 if any constituent call was Q4. That is not a
Q4-only evaluation: non-Q4 calls can bridge episodes, supply a success,
or keep an otherwise resolved Q4 failure open.

The repair selects Q4 calls before merging, and separately merges all calls.
On that snapshot's unchanged 96-call ledger, Q4 becomes 10 episodes:
2 TP, 4 FP, and 4 open, hence 2/6 (33%) resolved-only precision. All-channel
remains 28 episodes: 3 TP, 14 FP, and 11 open, hence 3/17 (18%). These are
snapshot-specific descriptive figures, not a new efficacy study. In the
affected UK Equity episode, a retained Q4 failure had been kept open by later
non-Q4 pending calls. The two observed Q4 successes do contain Q4 TP calls;
the actual correction is not evidence that those successes were fabricated.

The stored JSON at that base was also stale relative to its ledger and README.
The prepared schema-v2 repair records source identity, independently merged
channel episodes, and generates JSON and the headline from one snapshot.
Regression checks cover cross-channel success, pending contamination, bridging,
empty populations, and artifact drift. Early TP resolution versus waiting for
FP maturation is unchanged and remains an informative-censoring limitation.
Preparation and local testing of a patch are not evidence it is published.

## Acceptance

A population test must hold membership fixed when predictions are permuted,
retain misses, reject unexplained omissions/extra result IDs, reject
signal-dependent eligibility fields, preserve unscorable reasons, and report
the no-scored-events case as unknown rather than 100% or zero performance.
This is an evaluation contract, not a newly demonstrated financial edge.
