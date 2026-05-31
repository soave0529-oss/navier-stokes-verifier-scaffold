# Candidate Generation Spec v4

Date: 2026-05-19

Status: Step 56 complete.

Scope: define the next Track A candidate-generation contract after Step 55 left zero active
candidate-status lemmas. This is a generation gate, not a proof system and not a Navier-Stokes
solution claim.

Step 71 update: future active candidates must also reference a fresh zero-blocker
proof-obligation report/summary pair. This is metadata gating only; it is not proof evidence.

Step 72 update: `track-a-regularity/evaluator/candidate_obligation_template.py` can create
candidate-specific proof-obligation report/summary JSON scaffolds. Its default output is blocked
`needs_review` metadata; zero-blocker active reports require explicit discharge flags.

Step 79 update: future active candidates must also reference fresh blocker source-index
Markdown/JSON reports. This keeps the Step 77/78 provenance dashboard attached to the v4
emit gate. It is metadata gating only; it is not proof evidence.

Step 80 update: `track-a-regularity/evaluator/v4_metadata_checklist.py` renders the full v4
metadata checklist and audits `track-a-regularity/templates/v4_blocked_candidate_template.yaml`.
The template is blocked by default with `expected_evaluator.status: needs_review`; it is an
example shape only, not a candidate emission.

Step 81 update: `track-a-regularity/evaluator/proposed_candidate_staging.py` audits proposed YAML
before any manual copy into `track-a-regularity/candidates/`. It rejects inputs already inside the
active candidate directory and records whether a staged file is blocked, rejected, or ready for
manual copy. It never copies files and never emits candidates.

Step 82 update: `track-a-regularity/evaluator/manual_promotion_packet.py` renders a no-copy
manual promotion packet for staged YAML. It lists the exact pre-copy artifacts and post-copy
commands required before a `ready_for_manual_copy` record can enter
`track-a-regularity/candidates/`. It never copies files and never promotes candidates.

Step 83 update: `track-a-regularity/evaluator/active_pool_ingress_audit.py` audits the active
candidate directory against the manual promotion packet. It fails if staged, template, or v4-like
YAML appears in `track-a-regularity/candidates/` without a matching ready packet. It never copies
files, promotes candidates, or interprets metadata as proof evidence.

Step 84 update: `track-a-regularity/evaluator/promotion_lifecycle_dashboard.py` ties the Step 81
staging audit, Step 82 manual packet, and Step 83 ingress audit into one no-copy review surface.
It records whether a staged record is blocked, ready for manual copy, authorized in the active
pool, or an ingress violation. It does not promote candidates.

Step 85 update: `track-a-regularity/evaluator/promotion_dry_run_fixture.py` exercises a synthetic
ready candidate through staging, manual packet, lifecycle, and active-pool ingress checks using a
temporary candidate directory only. It creates and removes temporary sidecars and does not write
to the real `track-a-regularity/candidates/` pool.

Step 86 update: `track-a-regularity/evaluator/promotion_gate_regression.py` is the read-only
operator regression dashboard for this path. It treats the Step 85 dry-run as necessary but not
sufficient, and requires real staged readiness, a ready manual packet, real lifecycle readiness or
authorization, zero proof-obligation blockers, a checked v4 candidate-status YAML, source-index
freshness, evaluator coherence, clean ingress, and a passing full-smoke reference before real
candidate emission can be considered.

## Why v4 Exists

The v3 pipeline did its job: it produced broad substrates and let the evaluator collapse them into
known controls, known-overlap failures, definition failures, or manual-review blockers. The final
Step 55 distribution is:

```text
falsified 227
known_control 12
known_control_with_extra_assumption 6
needs_review 7
candidate 0
```

The next generator must not refill the candidate bucket with placeholders. A v4 candidate can be
emitted only if it has enough exact structure for a later proof or falsifier route.

## Emit-Ready Contract

A generated lemma may be emitted as expected evaluator `candidate` only if it includes all of the
following metadata markers in `related_known`:

```text
V4:ExactQuantityDefinitions
V4:ExactFunctionSpaces
V4:KnownResultSeparation
V4:ProofRoute
V4:SolutionClassBridge
V4:ZeroProofObligationBlockers
V4:FreshBlockerSourceIndex
```

These markers are not mathematical evidence. They are an audit trail that the generator has
explicitly supplied the minimum information needed for review.

## Required Content

### Exact Quantity Definitions

Every analytic quantity must be defined before it is used.

Allowed:

- named Fourier projector and sign convention;
- named local cylinder, admissible time interval, and cutoff convention;
- named norm with indices, time interval, domain, and endpoint convention;
- named pressure quantity with local/nonlocal decomposition.

Rejected:

- "critical norm" without indices;
- "flux envelope" without sign and projector convention;
- "pressure proxy";
- "diagnostic quantity";
- "normalization conventions made explicit" without actually listing them.

### Exact Function Spaces

The statement must specify all function-space indices and norms.

Minimum acceptable form:

```text
u in L^q_t X^s,p_x([0,T) x T^3), with q,p,s named and scaling noted.
```

Bare phrases such as `critical space-time norm`, `Besov-type`, `Morrey-type`, or `Duhamel term is
bounded` are not emit-ready.

### Known-Result Separation

The candidate must include a short separation note from the nearest known theorem family:

- BKM / Prodi-Serrin / Serrin endpoint;
- CKN / ESS / local-energy epsilon regularity;
- Kato / Koch-Tataru / Besov-Morrey critical criteria;
- Onsager / LES / energy equality / flux locality;
- geometric depletion / vorticity-direction / strain eigenvalue criteria.

If the note cannot separate the statement from known results, the output must be `known_control`,
`known_control_with_extra_assumption`, `falsified`, or `needs_review`, not `candidate`.

### Proof Route

Every candidate must name a proof route:

```text
hypothesis -> known continuation criterion
```

or

```text
hypothesis -> compactness/Liouville contradiction -> smooth continuation
```

The route can be incomplete, but the missing bridge must be explicit. A bare continuation theorem
claim is not emit-ready.

### Solution-Class Bridge

The statement must keep these classes separate:

- smooth classical solution on `[0,T)`;
- Leray-Hopf weak solution;
- suitable weak solution with local energy inequality;
- ancient blow-up limit;
- smooth continuation past `T`.

No weak-to-smooth upgrade is allowed unless an exact theorem and its hypotheses are named.

### Zero Proof-Obligation Blockers

Every emitted `candidate` must include candidate-specific proof-obligation metadata in
`expected_evaluator`:

```yaml
expected_evaluator:
  status: candidate
  proof_obligation_report_json: track-a-regularity/reports/<candidate>_proof_obligations.json
  proof_obligation_summary_json: track-a-regularity/reports/<candidate>_proof_obligation_summary.json
```

The v4 preflight requires the referenced report and summary to satisfy all of the following:

- the summary JSON is fresh relative to the report JSON;
- `lemma_id` matches the YAML candidate id;
- `candidate_status` is `candidate`;
- `active_candidate` is `true`;
- `promotion_blocker_count` is `0`;
- `active_candidate_blocker_conflict` is `false`.

If any proof-obligation blocker remains, the record must stay out of active candidate status.

### Fresh Blocker Source Index

Every emitted `candidate` must also include source-index metadata in `expected_evaluator`:

```yaml
expected_evaluator:
  status: candidate
  blocker_source_index_markdown: track-a-regularity/reports/needs_review_blocker_sources.md
  blocker_source_index_json: track-a-regularity/reports/needs_review_blocker_sources.json
```

The v4 preflight requires both source-index reports to be fresh relative to
`needs_review_blocker_sources.py` and to pass source existence checks. This connects future
candidate emission to the current provenance map for known blockers, without treating that map as
mathematical proof.

Template command for a blocked scaffold:

```bash
python track-a-regularity/evaluator/candidate_obligation_template.py \
  --candidate-id lemma_0253 \
  --report-output track-a-regularity/reports/lemma_0253_proof_obligations.json \
  --summary-output track-a-regularity/reports/lemma_0253_proof_obligation_summary.json
```

This does not create a candidate YAML and does not make the candidate emit-ready.

Checklist command:

```bash
python track-a-regularity/evaluator/v4_metadata_checklist.py \
  --output track-a-regularity/reports/v4_candidate_metadata_checklist.md \
  --check-output \
  --require-template-safe
```

The blocked template lives outside the active candidate pool:

```text
track-a-regularity/templates/v4_blocked_candidate_template.yaml
```

It must remain skipped by default preflight until a real proof-obligation discharge exists.

Staging audit command:

```bash
python track-a-regularity/evaluator/proposed_candidate_staging.py \
  track-a-regularity/templates/v4_blocked_candidate_template.yaml \
  --output track-a-regularity/reports/proposed_candidate_staging_audit.md \
  --check-output \
  --require-outside-candidates \
  --require-no-ready
```

The audit must pass before any future generated YAML is manually copied into
`track-a-regularity/candidates/`.

## Automatic Review Triggers

The v4 preflight linter routes a candidate to `needs_review` if it contains any of these patterns:

- `critical space-time norm`;
- `normalization conventions made explicit`;
- `diagnostic`;
- `proxy`;
- `placeholder`;
- `formal-only`;
- `finite vocabulary`;
- `weak solution` plus `extends smoothly`, unless a solution-class bridge marker exists.
- missing or stale `proof_obligation_report_json` / `proof_obligation_summary_json` for a
  candidate-status YAML;
- nonzero proof-obligation promotion blockers.
- missing or stale `blocker_source_index_markdown` / `blocker_source_index_json` for a
  candidate-status YAML;
- missing source paths in the blocker source index.

This is intentionally conservative. Review status is non-failing; it means the statement is not
ready to be treated as an active candidate.

## Output Rules

1. New generator output should use `expected_evaluator.status: candidate`, not legacy `pass`, only
   after the v4 preflight linter returns ready.
2. Formal vocabulary artifacts should use `needs_review`, not `candidate`.
3. Known theorem restatements should use `known_control`.
4. Known theorem plus auxiliary assumptions should use `known_control_with_extra_assumption`.
5. Badly posed or invariant-violating statements should use `fail` with a first expected failure.

## Bounded Next Step

Next candidate-generation work should use the template generator to create a blocked scaffold
first, then discharge obligations explicitly. Do not emit a new candidate unless the full v4
preflight and zero-blocker proof-obligation gate are satisfied.
