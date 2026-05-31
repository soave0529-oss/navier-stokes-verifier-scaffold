# Navier-Stokes Verifier-First Research Program

Date: 2026-05-23

Status: Steps 1-136 complete. This project has not solved the Navier-Stokes problem.

## Abstract

This project builds a verifier-first research scaffold for the 3D periodic incompressible
Navier-Stokes problem on `T^3` with smooth divergence-free mean-zero data, viscosity `nu > 0`,
and zero force. The program treats LLMs as candidate generators only. Every mathematical claim is
filtered through known theorem maps, cheap falsifiers, numerical diagnostics, or Lean artifacts.

The main result so far is infrastructure: a theorem map, a pseudo-spectral diagnostic solver, a
Track A candidate evaluator, a small Lean project, and one upstream formal-conjectures PR. The
strongest negative finding is that the first apparent survivors were BKM-with-extra-assumptions
or underdefined pressure proxies. A third, evaluator-v3-aware round produced 50 substrates; Step
35 tightened definition rules, Step 36 added one definition-tightened dyadic flux rewrite,
Step 37 added a diagnostic-only `Pi_N^LES` Track B harness, Step 38 added finite-mode
spectral-tail Lean vocabulary, Step 39 added one definition-tightened parabolic Morrey
rewrite, Step 40 marked vortex-stretching/strain geometric families as registry-first due
to known-result overlap, Step 41 turned that registry into an evaluator hook, Steps 42-43
added finite Lean vocabulary for shell projectors and parabolic Morrey cylinders, and Step 44
compressed the remaining unresolved families into registry/action buckets. Step 45 added a
critical-space known-result registry and evaluator hook for broad Besov/Morrey candidates, and
Step 46 added formal-only finite Duhamel bilinear vocabulary, Step 47 extended geometric
known-result filtering to the remaining depletion/alignment families, Step 48 classified the
last seven candidates before any expert review, Step 49 compared the parabolic Morrey candidate
against CKN/ESS/local-enstrophy literature, Step 50 compared the dyadic flux candidate against
Onsager/LES/energy-flux literature, Step 51 audited the low-pass flux balance, Step 52 marked
the dyadic flux rewrite as `needs_review` rather than active candidate, Step 53 decomposed the
parabolic Morrey proof obligations, Step 54 marked that rewrite as `needs_review`, and Step 55
moved the remaining formal-only Duhamel variants out of active candidate status. Step 56 added a
stricter v4 candidate-generation contract and preflight linter; Step 57 added Lean vocabulary for
that candidate gate. Step 58 refused to emit a v4 seed without a credible exact proof route and
added buildable Lean examples for the candidate gate instead. Step 59 made the v4 preflight an
executable pre-emission CLI. Step 60 wired that CLI into the reproducibility smoke workflow.
Step 61 froze active candidate emission behind the v4 gate and selected Track C
local-energy/suitable-weak vocabulary as the next branch. Step 62 added the first finite Lean
artifact for that branch. Step 63 mapped that artifact back to the `lemma_0252` proof obligations.
Step 64 added Lean proof-obligation graph vocabulary that keeps the missing analytic mechanisms
as explicit promotion blockers. Step 65 exposed that graph through a Track A report sidecar.
Step 66 wired report freshness into the reproducibility smoke workflow. Step 67 added a Lean
accessor bridge connecting the v4 candidate gate to proof-obligation graph blockers. Step 68 added
a machine-readable JSON export and freshness check for the proof-obligation report. Step 69 added
a JSON-consuming blocker consistency check. Step 70 added canonical Markdown/JSON blocker summary
dashboards and smoke freshness checks for that blocker state. Step 71 connected zero-blocker
proof-obligation report metadata to the v4 candidate preflight. Step 72 added a candidate-specific
proof-obligation report/summary template generator for future gated candidates. Step 73 added a
registry that inventories the seven existing `needs_review` records by blocker family and
candidate-specific scaffold status. Step 74 materialized blocked-by-default scaffold
report/summary JSON pairs for all seven current `needs_review` records. Step 75 added a
family-specific blocker matrix that maps the six generic template obligations to actual Duhamel,
dyadic-flux, and parabolic-Morrey blockers. Step 76 connected that matrix back to each scaffold's
actual promotion blocker keys and added a reproducibility guard for scaffold/matrix consistency.
Step 77 added source/provenance references for every matrix blocker row and a smoke guard that
fails if those references are empty or missing. Step 78 added a compact source/provenance
dashboard that groups those 24 referenced files by blocker family and source file, with freshness
checks in the smoke workflow. Step 79 connected that source index to the v4 preflight gate for
future active-candidate metadata. Step 80 added a generated v4 metadata checklist and a
blocked-by-default template example outside the active candidate pool. Step 81 added a
proposed-candidate staging audit so future YAML is checked outside `track-a-regularity/candidates/`
before any manual copy into the active pool. Step 82 added a no-copy manual promotion packet
that lists the exact pre-copy artifacts and post-copy commands before staged YAML can enter the
active pool. Step 83 added an active-pool ingress audit that fails staged, template, or v4-like
YAML copied into `track-a-regularity/candidates/` without a matching ready manual packet. Step 84
added a promotion lifecycle dashboard that ties staging, manual packet, and ingress states into
one no-copy review surface. Step 85 added an end-to-end temporary promotion dry-run fixture that
exercises a synthetic ready candidate through staging, manual packet, lifecycle, and temporary
authorized ingress without touching the real active candidate pool. Step 86 added a read-only
promotion gate regression dashboard that makes explicit why that dry-run is necessary but not
sufficient for real candidate emission. Step 87 added a read-only `lemma_0252` known-theorem
mapping that ties the three substantive proof-obligation blockers to CKN/Lin, ESS/Seregin/KNSS,
BKM/Prodi-Serrin/Constantin-Fefferman, and Tao/BV caution anchors without promoting a candidate.
Step 88 expanded the compactness/Liouville branch into an explicit deferred-new-result checklist.
Step 89 expanded the finite-bound-to-smallness branch into a read-only checklist showing that
CKN/Lin-style routes remain smallness-only and do not discharge `lemma_0252`. Step 90 expanded
the smooth-continuation branch into a read-only checklist showing that local regularity metadata
is not automatically BKM, Prodi-Serrin, high-Sobolev, or Constantin-Fefferman continuation input.
Step 91 joined the Step 87-90 artifacts into a blocker-closure dashboard showing that all three
substantive branches are present but unresolved, with zero discharged blockers and no candidate
emission authorization. Step 92 connected that closure verdict back into the promotion gate
regression dashboard, so real candidate emission is blocked directly by
`closure_verdict=blocked_no_discharge` rather than only by older proof-obligation blocker counts.
Step 93 added a closure-dependency consistency guard, so the promotion gate regression smoke fails
if that gate drifts away from the Step 91 closure dashboard values it cites. Step 94 added a
read-only promotion-gate blocker ledger that classifies the six current real-emission blockers by
operator action family before any future discharge attempt. Step 95 added an action-readiness
guard that keeps process blockers non-actionable while proof-obligation and closure analytic
blockers remain. Step 96 added a read-only analytic-prerequisite packet that lists the exact
proof-obligation and closure discharge artifacts required before any process gate can open.
Step 97 added a read-only dependency guard so that packet cannot drift away from Step 95
action-readiness, the proof-obligation graph, or the Step 91 closure dashboard. Step 98 added a
read-only analytic discharge work-order matrix that groups those eight prerequisites by required
artifact type and source branch while keeping every work order blocked and non-actionable. Step 99
added a blocked-by-default analytic discharge template audit for those eight work-order types,
recording required evidence keys and forbidden mutations without making any work order actionable.
Step 100 added a dependency/freshness guard so the Step 99 template audit cannot drift from the
Step 98 matrix, Step 96 prerequisites, or Step 97 dependency report. Step 101 added a compact
read-only operator dashboard/index that consolidates the Step 96-100 analytic-discharge gate stack
into one surface while keeping all gates closed and all templates blocked. Step 102 added a
read-only discharge-artifact gap index that maps the eight blocked Step 98/99 work-order/template
types to missing concrete theorem/formal artifacts and required review evidence. Step 103 added a
read-only dependency/freshness guard so that gap index cannot drift from the Step 101 operator
dashboard, Step 100 template-dependency guard, Step 99 template audit, or Step 98 work-order
matrix. Step 104 added a compact read-only operator/source index for the Step 102-103 gap
artifacts while preserving blocked and non-actionable status for every gap. Step 105 added a
read-only dependency/freshness guard so that operator index cannot drift from the Step 102-103
canonical reports or the broader Step 101 analytic-discharge dashboard. Step 106 added a
read-only literature source index over the 15 local `papers/blockers/` materials, mapping them to
the three substantive `lemma_0252` blockers and cross-cutting anchors without discharging any
blocker. Step 107 added a read-only dependency/freshness guard so that literature index cannot
drift from `papers/blockers/index.md`, the `lemma_0252` proof-obligation graph, or the Step 91
blocker-closure dashboard. Step 108 added a read-only literature source-to-gap matrix that maps
those 15 sources onto the eight blocked analytic-discharge gaps and ranks the direct analytic
attack order without changing blocker state. Step 109 added a read-only dependency/freshness
guard so that gap matrix cannot drift from the Step 106 literature index, Step 107 literature
dependency guard, Step 102 analytic-discharge gap index, or broader Step 101 analytic-discharge
dashboard. Step 110 added a compact read-only operator/source index consolidating the Step 108
gap matrix and Step 109 gap-dependency guard into one literature-gap review surface while keeping
every gap blocked and non-actionable. Step 111 added a read-only dependency/freshness guard so
that Step 110 operator index cannot drift from the Step 108/109 canonical reports or the Step
106/107 literature stack. Step 112 added a read-only, non-promotional theorem-artifact review
queue that maps direct analytic gaps `gap_002`, `gap_003`, and `gap_004` to local blocker
literature and the missing theorem/formal artifacts needed before any future discharge attempt.
Step 113 added a read-only dependency/freshness guard so that queue cannot drift from the Step
102 analytic-discharge gap index, the Step 108-111 blocker-literature gap stack, or
`papers/blockers/index.md`. Step 114 added a compact read-only operator/source index that
consolidates the Step 112 queue and Step 113 dependency guard into one review surface while
keeping all queue items blocked and non-actionable. Step 115 added a read-only dependency/
freshness guard so that Step 114 operator index cannot drift from the Step 112-113 queue stack,
the Step 102 analytic-discharge gap index, the Step 108-111 blocker-literature gap stack, or
`papers/blockers/index.md`. Step 116 added a read-only finite-bound-to-smallness source-read
packet for queue gap `gap_002`, extracting hypothesis, conclusion, and mismatch fields from the
seven local sources while keeping the gap blocked and non-actionable. Step 117 added a read-only
dependency/freshness guard so that source-read packet cannot drift from the Step 89
finite-bound-to-smallness checklist, the Step 112-115 theorem-artifact queue stack, or
`papers/blockers/index.md`. Step 118 added a read-only compactness/Liouville source-read packet
for queue gap `gap_003`, extracting hypothesis, conclusion, and mismatch fields from the six local
sources while keeping the gap blocked and non-actionable. Step 119 added a read-only dependency/
freshness guard so that packet cannot drift from the Step 88 compactness/Liouville checklist, the
Step 112-115 theorem-artifact queue stack, or `papers/blockers/index.md`. Step 120 added a
read-only smooth-continuation source-read packet for queue gap `gap_004`, extracting hypothesis,
conclusion, and mismatch fields from the two local smooth-continuation sources while keeping the
gap blocked and non-actionable. Step 121 added a read-only dependency/freshness guard so that
packet cannot drift from the Step 90 smooth-continuation checklist, the Step 112-115
theorem-artifact queue stack, or `papers/blockers/index.md`. Step 122 added a compact read-only
operator/source index consolidating the Step 120 packet and Step 121 dependency guard while
keeping `gap_004` blocked and non-actionable. Step 123 added a read-only dependency/freshness
guard so that operator/source index cannot drift from Step 120, Step 121, Step 90, the Step
112-115 theorem-artifact queue stack, or `papers/blockers/index.md`. Step 124 added a compact
read-only operator/source dashboard consolidating the Step 120-123 smooth-continuation source-read
stack while keeping `gap_004` blocked and non-actionable. Step 125 added a compact read-only
cross-gap source-read status dashboard consolidating `gap_002`, `gap_003`, and `gap_004` source-read
packets and dependency guards into one review surface while keeping every direct analytic gap
blocked and non-actionable. Step 126 added a read-only dependency/freshness guard so that
cross-gap dashboard cannot drift from the Step 116-124 source-read reports, the Step 112-115
theorem-artifact queue reports, the Step 89/88/90 branch checklists, or `papers/blockers/index.md`.
Step 127 added a compact read-only operator/source dashboard consolidating the Step 125-126
cross-gap source-read status stack while keeping all direct analytic gaps blocked and
non-actionable. Step 128 added a read-only dependency/freshness guard so that Step 127 stack
dashboard cannot drift from Step 125, Step 126, Steps 116-124 source-read reports, Steps 112-115
queue reports, Step 89/88/90 branch checklists, or `papers/blockers/index.md`; it also keeps a
compactness guard on the Step 127 JSON. Step 129 added a compact read-only operator/source index
consolidating the Step 127-128 cross-gap source-read status stack while keeping all direct analytic
gaps blocked and non-actionable. Step 130 pivots back to blocker mathematics by adding a Vasseur
2007 De Giorgi partial-regularity row to the original known-theorem mapping: the route is adjacent
but not direct, because it still requires small local velocity/gradient/pressure or scaled-gradient
smallness rather than mere finite parabolic Morrey/vorticity-enstrophy boundedness. Step 131
continues that math-substance pivot by refining the KNSS compactness/Liouville row: KNSS supplies
a bounded-ancient Liouville template, but its proved 3D branches are axisymmetric or
special-geometry, while the general 3D bounded ancient problem is explicitly open and the
`lemma_0252` setting lacks the required bounded ancient mild/suitable compactness package. Step
132 adds a companion Tao 2013 localisation/compactness verdict note: Tao is a useful framework
anchor, but it still leaves the ancient-limit, pressure/local-energy compactness, nontriviality,
and Liouville/backward-uniqueness inputs as a new-result requirement. Step 133 refines the ESS
backward-uniqueness row: the branch remains adjacent, but it needs endpoint velocity control,
compatible ancient/terminal compactness, boundedness/decay, and pressure/vorticity regularity not
available from the finite critical Morrey/vorticity-enstrophy metadata alone. Step 134 adds a
companion Tao 2013 finite-bound-to-smallness verdict note: Tao's localised enstrophy estimate is
the closest local-enstrophy architecture, but it propagates already-small local vorticity/curl-force
input under a short-time condition rather than converting finite critical parabolic
Morrey/vorticity-enstrophy boundedness into CKN epsilon smallness. Step 135 adds a companion
Wang 2023 finite-bound-to-smallness verdict note: Wang's small-energy partial-regularity theorem
and pressure compactness mechanism are useful `gap_002` anchors, but they assume all-scale small
scaled gradient energy and do not create CKN epsilon smallness from finite critical Morrey/
vorticity-enstrophy boundedness. Step 136 adds a companion Lei-Ren 2022 quantitative
partial-regularity verdict note: the paper gives logarithmically improved partial regularity,
regular strips/epochs, and axisymmetric criteria, but it does not convert finite critical
Morrey/vorticity-enstrophy boundedness into CKN epsilon smallness in the general `lemma_0252`
setting. Step 137 starts the separate theorem-generation pipeline with a Stage 1 Tao 2013
technique card: it records the localised energy/enstrophy mechanism, assumption/conclusion shape,
sharpness and break points, distance to the three `lemma_0252` blockers, and Stage 2 recombination
seeds, while adding no dashboard, gate, candidate, or blocker discharge.
Step 138 adds the Stage 1 exit/value assessment for that Tao card: the Tao path is worth exactly
one bounded Stage 2 obstacle-tree attempt, selecting the CKN/Lin pressure-local-energy package
plus Tao local vorticity cutoff seed and the `tao_ckn_pressure_local_energy_transfer` obstacle.

## Problem Scope

Target statement:

- domain: periodic `T^3`;
- equation: 3D incompressible Navier-Stokes;
- force: `0`;
- data: smooth, divergence-free, mean-zero;
- goal class: smooth classical continuation/global regularity or a Clay-compatible breakdown
  alternative.

Non-goals:

- no claim of solving the Clay problem;
- no natural-language proof without formal or peer-reviewed verification;
- no weak-solution-to-smooth upgrade without explicit regularity theorem;
- no use of pseudo-spectral diagnostics as proof.

## Method

The project uses three coupled tracks.

| track | role | current artifact |
|---|---|---|
| Track A | generate and falsify candidate regularity lemmas | evaluator with scaling, Galilean, Taylor-Green, known-result, novelty, hypothesis, endpoint, convex-integration, pressure-proxy, known-control-extension, duplicate-family, flux-balance-risk, parabolic-Morrey-obligation, Duhamel-formal-only, solution-class checks, executable v4 generation preflight, reproducibility-checked Markdown/JSON proof-obligation report sidecars, blocker consistency checks, blocker summary dashboards, a zero-blocker proof-obligation gate, a candidate-specific proof-obligation template generator, a needs-review obligation registry, blocked scaffolds for all current `needs_review` records, a family-specific blocker matrix, a scaffold/matrix consistency guard, blocker-row provenance references, a blocker source index dashboard, a source-index v4 preflight gate, a v4 metadata checklist with blocked template audit, a proposed-candidate staging audit, a manual promotion packet report, an active-pool ingress audit, a promotion lifecycle dashboard, a temporary promotion dry-run fixture, a read-only promotion gate regression dashboard, a `lemma_0252` known-theorem blocker mapping with Vasseur 2007 finite-bound verdict refinement, compactness/Liouville, finite-bound-to-smallness, and smooth-continuation branch checklists, a `lemma_0252` blocker-closure dashboard, closure-verdict integration into the promotion gate regression surface, closure-dependency consistency smoke checks, a promotion-gate blocker ledger, an analytic-first action-readiness guard, a read-only analytic-prerequisite packet, an analytic-prerequisite dependency guard, an analytic discharge work-order matrix, an analytic discharge template audit, a template-dependency guard, an operator dashboard, an analytic discharge gap index, a gap-dependency guard, a gap operator/source index, a gap-operator dependency guard, a `lemma_0252` blocker-literature source index, a blocker-literature dependency guard, a blocker-literature gap matrix, a blocker-literature gap dependency guard, a blocker-literature gap operator/source index, a blocker-literature gap operator dependency guard, a theorem-artifact review queue for the three direct analytic gaps, a dependency guard for that queue, a queue operator/source index, a queue-operator dependency guard, a finite-bound-to-smallness source-read packet for `gap_002`, a dependency guard for that packet, a compactness/Liouville source-read packet for `gap_003`, a dependency guard for that packet, a smooth-continuation source-read packet for `gap_004`, a dependency guard for that packet, a smooth-continuation source-read operator/source index for `gap_004`, a dependency guard for that operator/source index, a smooth-continuation source-read stack dashboard, a cross-gap source-read status dashboard for `gap_002`, `gap_003`, and `gap_004`, a dependency guard for that cross-gap dashboard, a cross-gap source-read status stack dashboard, a dependency guard for that stack dashboard, and a cross-gap source-read status stack operator/source index |
| Track B | produce numerical diagnostic pressure against false lemmas | pseudo-spectral Taylor-Green, localized-swirl, and `Pi_N^LES` smoke diagnostics |
| Track C | formalize small stable vocabulary in Lean | heat semigroup toy artifact, solution-class vocabulary, spectral-tail vocabulary, shell-projector vocabulary, parabolic-cylinder vocabulary, local-energy vocabulary, proof-obligation graph vocabulary, Duhamel-bilinear vocabulary, candidate-gate vocabulary and gate examples, candidate-obligation bridge vocabulary, first promotion skeleton, upstream PR |

The workflow is intentionally conservative:

1. Start from the Clay/Fefferman statement and current Lean baselines.
2. Generate candidate lemmas only as structured YAML, not prose proof.
3. Reject candidates using cheap invariant and known-result checks.
4. Promote only small, typed, buildable Lean artifacts.
5. Record every waiver and blocked criterion explicitly.

## Findings

### Baselines

DeepMind formal-conjectures already contains Lean statements for the four Clay alternatives,
including the periodic statement closest to this project. lean-dojo's LeanMillenniumPrizeProblems
contains broader PDE scaffolding, including weak and Leray-Hopf-style structures, but not the
missing regularity proof.

### Numerical Track

The pseudo-spectral solver is stable and divergence-free on cheap Taylor-Green and localized
swirl diagnostics. Step 6's original strict `N64/T10` enstrophy match to a `512^3` reference was
reclassified as a DNS-quality validation target, not a solver MVP. The accepted MVP keeps the
solver as a falsifier and diagnostic tool, not as proof evidence.

Current reproducibility smoke:

- Taylor-Green `N=16`, `T=0.05`, `ifrk4` passed;
- final divergence max `2.893e-20`;
- Python full suite `454 passed`.

### Candidate Track

Across 252 generated candidates:

| status | count | meaning |
|---|---:|---|
| `known_control` | 12 | BKM/Prodi-Serrin controls |
| `known_control_with_extra_assumption` | 6 | BKM plus auxiliary assumptions |
| `falsified` | 227 | rejected by evaluator checks |
| `candidate` | 0 | no active candidates remain after current cheap checks and review metadata |
| `needs_review` | 7 | Duhamel formal-only variants plus `lemma_0251/0252` need rewrite before expert review |

Step 31 eliminated the previous survivor overcount. The former 10 survivors collapsed into
pressure-proxy failures and BKM-with-extra-assumption controls. Step 32 then generated 50
v3-aware candidates that avoid those two failure modes. Step 35 failed the five selected
definition-sensitive families until exact quantities are supplied, leaving 25 unresolved
lower-priority templates. Step 36 added `lemma_0251`, an exact dyadic flux rewrite, and Step 39
added `lemma_0252`, an exact parabolic Morrey enstrophy rewrite. They initially survived syntactic
filters as candidate substrates, but were later downgraded to review after targeted audits. Step 45
then removed broad critical Besov and velocity Morrey templates
from the candidate pool as known-overlap failures. Step 47 removed depleted vortex-stretching and
strain-vorticity alignment templates as geometric known-overlap failures. This survival is not a
truth signal.
Step 48 classified the remaining Duhamel variants as formal-only and initially kept `lemma_0251/0252`
as high-risk substrates needing targeted known-result comparison. Step 49 kept `lemma_0252` active
but blocked: it is not an obvious CKN/ESS restatement, yet it still lacks a finite-bound-to-smallness
or compactness/Liouville mechanism. Steps 50-52 downgrade
`lemma_0251`: the project sign makes positive `Pi_N^LES` a low-pass energy feeding/backscatter
quantity relative to usual forward SGS flux, and the weighted positive-part budget lacks a
coercive bridge to smooth continuation. Steps 53-54 also remove `lemma_0252` from active candidate
routing: no finite-bound-to-smallness route is identified, so promotion would require a
compactness/Liouville branch or a likely-known epsilon/pressure/local-energy rewrite. Step 55
removes the final five Duhamel variants from active candidate status because they lack exact
function spaces and the real NSE bilinear/Leray/time-integral structure.

Step 56-61 changed the forward path from "generate more broad candidates" to "gate generation
before emission": future expected `candidate` YAML must pass the v4 preflight contract and the
corresponding Lean vocabulary now records the audit fields as typed metadata. Step 58 specifically
kept the active candidate count at zero rather than filling it with a forced seed.
Step 65 keeps that posture: it exposes `lemma_0252` blockers in a report, but does not promote it
or create any replacement candidate. Step 66 makes that report part of the reproducibility smoke.
Step 67 connects the v4 candidate gate to the proof-obligation graph at the Lean vocabulary level,
while keeping current graph-backed promotion blocked. Step 68 makes the same blocker state
machine-readable as JSON and checks freshness in the reproducibility smoke workflow. Step 69
consumes the JSON report and fails active-candidate-with-blockers metadata conflicts. Step 70
exposes the same state as canonical Markdown/JSON blocker summary dashboards and checks both for
freshness in the smoke workflow. Step 71 makes future active-candidate emission require a fresh,
candidate-specific zero-blocker proof-obligation report/summary pair in v4 preflight metadata.
Step 72 adds the blocked-by-default template generator for those future report/summary pairs.
Step 73 inventories the seven current `needs_review` records and shows that none yet has a Step
72 candidate-specific scaffold; `lemma_0252` still has its separate proof-obligation graph
sidecar.
Step 74 creates those seven Step 72 scaffold pairs and refreshes the registry to require
`present_blocked`: every scaffold stays `candidate_status=needs_review`, `active_candidate=false`,
and has six unresolved template blockers.
Step 75 maps those six generic blockers to actual family blockers for the three remaining
`needs_review` families. The current matrix covers five Duhamel formal-only records, one
dyadic-flux record, and one parabolic-Morrey record, and smoke fails if the canonical matrix
Markdown/JSON becomes stale.
Step 76 then reads each scaffold JSON back through the matrix and fails if the scaffold's actual
promotion blocker keys, candidate status, active flag, or matrix family no longer match the
guarded `present_blocked` state.
Step 77 adds `source_refs` to every matrix detail row, connecting each family-specific blocker to
the local triage notes, known-result registries, evaluator checks/logs, and Track C Lean vocabulary
that justify the blocker. The smoke workflow now fails if those references are empty or point to
missing files.
Step 78 turns those references into canonical Markdown/JSON source-index dashboards. The current
index has 18 matrix rows, 24 unique source files, and 0 missing sources. It groups source usage by
blocker family and by source kind (`doc`, `log`, `evaluator_check`, `lean_vocabulary`), and smoke
fails if either dashboard is stale or references a missing source.
Step 79 adds `V4:FreshBlockerSourceIndex` to the future candidate marker set and requires future
`candidate` YAML to reference fresh source-index Markdown/JSON reports in `expected_evaluator`.
The existing pool still has zero active candidates, so default preflight remains
`checked=0 skipped=252 blocked=0`.
Step 80 renders the full v4 metadata checklist as canonical Markdown/JSON and adds a loadable
blocked template under `track-a-regularity/templates/`. The template includes the required markers
and metadata keys but keeps `expected_evaluator.status=needs_review`; default preflight skips it
with `checked=0 skipped=1 blocked=0`, so it does not refill the active candidate bucket.
Step 81 adds a canonical proposed-candidate staging audit outside the active pool. The current
audit checks the blocked Step 80 template and reports `proposal_count=1`, `ready_count=0`,
`blocked_count=1`, `rejected_count=0`; smoke fails if the report is stale or if the canonical
blocked-template audit unexpectedly contains a ready staged candidate.
Step 82 adds a canonical manual promotion packet for that staged template. The current packet
reports `packet_count=1`, `ready_packet_count=0`, `blocked_packet_count=1`,
`rejected_packet_count=0`; smoke fails if the packet is stale or if the canonical blocked-template
packet unexpectedly becomes ready or rejected.
Step 83 adds a canonical active-pool ingress audit after the manual packet. The current audit
reports `active_candidate_file_count=252`, `legacy_skipped_count=252`,
`tracked_target_absent_count=1`, `authorized_ingress_count=0`, and `violation_count=0`; smoke
fails if the audit is stale or if staged/template/v4-like YAML appears in
`track-a-regularity/candidates/` without a matching ready packet.
Step 84 adds a canonical promotion lifecycle dashboard that joins the Step 81 staging audit, Step
82 manual packet, and Step 83 ingress audit. The current dashboard reports `proposal_count=1`,
`packet_count=1`, `lifecycle_entry_count=1`, `lifecycle_ready_count=0`,
`lifecycle_blocked_count=1`, `lifecycle_authorized_count=0`, and `lifecycle_violation_count=0`.
Smoke fails if the canonical blocked template becomes ready or if an ingress violation appears.
Step 85 adds a canonical temporary promotion dry-run fixture. The fixture creates a synthetic
ready v4 candidate and all required sidecars under a temporary directory, verifies staging
`ready_for_manual_copy`, renders a ready manual packet, checks pre-copy lifecycle readiness, copies
only into a temporary active candidate directory, and then verifies authorized ingress plus
`authorized_in_active_pool`. The canonical report shows `dry_run_passed=true`,
`temp_root_removed=true`, `real_candidate_pool_untouched=true`, and `phase_count=7`.
Step 86 adds a canonical promotion gate regression dashboard. It reports
`dry_run_passed=true` but `dry_run_sufficient_for_real_emission=false` and
`real_emission_ready=false`. Current real-emission blockers are the absent staged ready record,
absent ready manual packet, absent ready/authorized real lifecycle entry, nonzero proof-obligation
blockers for `lemma_0252`, and current-pool v4 preflight checking zero candidate-status YAML.
Step 87 drills into the `lemma_0252` proof-obligation blocker from that list. The canonical
known-theorem mapping has 9 rows across `finite_bound_to_smallness`, `compactness_liouville`, and
`smooth_continuation_bridge`. No row applies directly and `resolvable_known_count=0`; the best
available rows are either `resolvable_needs_new_result` or `permanently_blocked` route-specific
comparisons. The result is a negative clarification: `lemma_0252` cannot be emitted as an active
candidate without a new finite-bound-to-smallness, compactness/Liouville, or smooth-continuation
bridge theorem.
Step 88 expands the compactness/Liouville branch into exact missing artifacts. The canonical
checklist reports `branch_verdict=deferred_needs_new_result`, `checklist_item_count=6`,
`theorem_branch_count=3`, and `dischargeable_now_count=0`. The missing core is an ancient
solution class, rescaling compactness, pressure/local-energy package, nontriviality condition,
Liouville/backward-uniqueness theorem, and a return bridge to smooth continuation.
Step 89 expands the finite-bound-to-smallness branch into exact missing artifacts. The canonical
checklist reports `branch_verdict=deferred_needs_new_result`, `checklist_item_count=7`,
`theorem_branch_count=4`, and `dischargeable_now_count=0`. CKN and Lin remain smallness-only
branches, and local Morrey or Tao/BV comparison anchors do not supply the missing monotonicity,
self-improvement, pressure/cutoff, or continuation bridge.
Step 90 expands the smooth-continuation branch into exact missing artifacts. The canonical
checklist reports `branch_verdict=deferred_needs_new_result`, `checklist_item_count=7`,
`theorem_branch_count=5`, and `dischargeable_now_count=0`. BKM, Prodi-Serrin, and high-Sobolev
branches are all missing their required continuation inputs; Constantin-Fefferman is an
extra-assumption branch; and local terminal regularity still lacks a uniform global continuation
patching theorem.
Step 91 joins the three branch checklists with the Step 87 theorem mapping into a closure
dashboard. The canonical report has `closure_verdict=blocked_no_discharge`,
`checklist_branch_count=3`, `unresolved_branch_count=3`, `discharged_blocker_count=0`,
`direct_known_route_count=0`, and `candidate_emission_authorized=false`. This turns the negative
result into an executable guardrail: checklist presence is not blocker discharge.
Step 92 connects that guardrail back into the promotion gate regression dashboard. The canonical
promotion gate report now has `gate_count=12`, `blocking_gate_count=6`, and a dedicated blocked
gate `lemma_0252_blocker_closure_not_blocked` whose current state includes
`closure_verdict=blocked_no_discharge`, `unresolved_branch_count=3`,
`discharged_blocker_count=0`, and `candidate_emission_authorized=false`.
Step 93 adds an explicit closure-dependency block to the same dashboard. The canonical report now
has `closure_dependency_consistent=true`, `gate_current_state_matches_closure=true`,
`gate_blocks_when_closure_blocked=true`, and `issues=[]`; smoke invokes
`--require-closure-dependency` for both Markdown and JSON promotion gate reports.
Step 94 adds a canonical promotion-gate blocker ledger on top of that regression surface. It
classifies the six blocking gates into `staging`, `manual_packet`, `lifecycle`,
`proof_obligation`, `closure`, and `v4_preflight`, with four process blockers, one analytic
proof-obligation blocker, and one analytic closure blocker. The ledger is read-only and does not
authorize staging work, manual promotion, active-pool ingress, candidate emission, or blocker
discharge.
Step 95 adds an action-readiness guard on top of the ledger. The canonical report has
`analytic_first_guard_active=true`, `process_actionable_count=0`,
`process_blocked_by_analytic_count=4`, and `promotion_action_authorized=false`, so process gates
remain closed until the analytic `proof_obligation` and `closure` blockers genuinely move.
Step 96 turns that priority rule into a concrete analytic prerequisite packet. The canonical
packet has `prerequisite_count=8`, `satisfied_prerequisite_count=0`,
`unsatisfied_prerequisite_count=8`, and `process_gate_open_authorized=false`; it requires zero
proof-obligation blockers, reviewed discharge artifacts for `finite_bound_to_smallness`,
`compactness_liouville`, and `smooth_continuation_bridge`, a non-blocked closure verdict, zero
unresolved branches, three discharged substantive blockers, and explicit candidate-emission
authorization before any process gate can open.
Step 97 adds a dependency guard for that packet. The canonical report has
`dependency_check_count=17`, `passed_dependency_check_count=17`,
`failed_dependency_check_count=0`, `dependency_consistent=true`, and
`process_gate_open_authorized=false`; smoke now fails if Step 96 drifts from Step 95
action-readiness, the proof-obligation graph, or the Step 91 closure dashboard.
Step 98 adds the operator-facing work-order matrix for those prerequisites. The canonical report
has `work_order_count=8`, `blocked_work_order_count=8`, `actionable_work_order_count=0`,
`artifact_type_count=8`, `source_branch_count=8`, `dependency_consistent=true`,
`process_gate_open_authorized=false`, and `candidate_emission_authorized=false`; smoke now checks
Markdown/JSON freshness with `--require-blocked`, `--require-dependency-consistent`, and
`--require-sources-exist`.
Step 99 adds a blocked-by-default template audit for those eight work-order types. The canonical
report has `template_count=8`, `blocked_template_count=8`, `actionable_template_count=0`,
`may_discharge_template_count=0`, `artifact_type_count=8`, `source_branch_count=8`,
`dependency_consistent=true`, `process_gate_open_authorized=false`,
`blocker_state_changed=false`, and `candidate_emission_authorized=false`; smoke now checks
Markdown/JSON freshness with `--require-blocked`, `--require-matrix-consistent`, and
`--require-sources-exist`. These templates are audit scaffolds only: they list required evidence
keys and forbidden mutations, but do not discharge proof-obligation or closure blockers.
Step 100 adds a dependency guard for that template audit. The canonical report has
`dependency_check_count=26`, `passed_dependency_check_count=26`,
`failed_dependency_check_count=0`, `dependency_consistent=true`, `template_count=8`,
`matrix_work_order_count=8`, `packet_prerequisite_count=8`, `blocked_template_count=8`,
`actionable_template_count=0`, `may_discharge_template_count=0`,
`process_gate_open_authorized=false`, `blocker_state_changed=false`, and
`candidate_emission_authorized=false`; smoke now checks Markdown/JSON freshness with
`--require-consistent`, `--require-sources-exist`, and `--require-blocked`.
Step 101 consolidates the Step 96-100 analytic-discharge gate stack into one operator surface. The
canonical dashboard has `stack_step_count=5`, `source_report_count=10`, `prerequisite_count=8`,
`unsatisfied_prerequisite_count=8`, `work_order_count=8`, `blocked_work_order_count=8`,
`template_count=8`, `blocked_template_count=8`, `dependency_guard_count=2`,
`dependency_check_count=43`, `failed_dependency_check_count=0`,
`stack_consistency_check_count=23`, `failed_stack_consistency_check_count=0`,
`stack_consistent=true`, `process_gate_open_authorized=false`, `blocker_state_changed=false`, and
`candidate_emission_authorized=false`; smoke now checks Markdown/JSON freshness with
`--require-stack-consistent`, `--require-sources-exist`, and `--require-blocked`.
Step 102 adds a discharge-artifact gap index on top of that stack. The canonical index has
`gap_count=8`, `blocked_gap_count=8`, `actionable_gap_count=0`,
`may_discharge_gap_count=0`, `missing_artifact_count=8`,
`required_review_evidence_key_count=6`, `minimum_acceptance_check_count=24`,
`source_branch_count=8`, `artifact_type_count=8`, `stack_consistent=true`,
`process_gate_open_authorized=false`, `blocker_state_changed=false`, and
`candidate_emission_authorized=false`; it maps each proof-obligation and closure gap to the
missing theorem/formal artifact and required review evidence without changing blocker state.
Step 103 adds a dependency guard for that gap index. The canonical report has
`dependency_check_count=42`, `passed_dependency_check_count=42`,
`failed_dependency_check_count=0`, `dependency_consistent=true`, `gap_count=8`,
`blocked_gap_count=8`, `actionable_gap_count=0`, `may_discharge_gap_count=0`,
`missing_artifact_count=8`, `template_count=8`, `matrix_work_order_count=8`,
`template_dependency_check_count=26`, `operator_stack_consistent=true`,
`process_gate_open_authorized=false`, `blocker_state_changed=false`, and
`candidate_emission_authorized=false`; smoke now checks Markdown/JSON freshness with
`--require-consistent`, `--require-sources-exist`, and `--require-blocked`.
Step 104 adds a compact operator/source index over the Step 102-103 gap artifacts. The canonical
index has `section_count=2`, `source_report_count=4`, `source_ref_count=14`, `gap_count=8`,
`blocked_gap_count=8`, `actionable_gap_count=0`, `may_discharge_gap_count=0`,
`missing_artifact_count=8`, `gap_dependency_check_count=42`,
`gap_dependency_failed_check_count=0`, `gap_dependency_consistent=true`,
`operator_stack_consistent=true`, `operator_index_check_count=20`,
`failed_operator_index_check_count=0`, `operator_index_consistent=true`,
`process_gate_open_authorized=false`, `blocker_state_changed=false`, and
`candidate_emission_authorized=false`; smoke now checks Markdown/JSON freshness with
`--require-consistent`, `--require-sources-exist`, and `--require-blocked`.
Step 105 adds a dependency guard for that operator index. The canonical report has
`direct_source_report_count=8`, `source_ref_count=25`, `operator_dependency_check_count=40`,
`failed_operator_dependency_check_count=0`, `operator_dependency_consistent=true`,
`gap_operator_index_check_count=20`, `gap_operator_failed_check_count=0`,
`gap_operator_consistent=true`, `gap_dependency_check_count=42`,
`gap_dependency_failed_check_count=0`, `gap_dependency_consistent=true`,
`gap_index_stack_consistent=true`, `operator_dashboard_stack_consistent=true`, `gap_count=8`,
`blocked_gap_count=8`, `actionable_gap_count=0`, `may_discharge_gap_count=0`,
`missing_artifact_count=8`, `process_gate_open_authorized=false`,
`blocker_state_changed=false`, and `candidate_emission_authorized=false`; smoke now checks
Markdown/JSON freshness with `--require-consistent`, `--require-sources-exist`, and
`--require-blocked`.
Step 106 adds a read-only literature source index over the local `papers/blockers/` collection.
The canonical report has `literature_source_count=15`, `pdf_count=14`, `html_count=1`,
`search_log_count=3`, `blocker_family_count=4`, `substantive_blocker_count=3`,
`cross_cutting_source_count=3`, `missing_source_count=0`, `missing_search_log_count=0`,
`unmapped_source_count=0`, `direct_discharge_source_count=0`, `source_index_check_count=16`,
`failed_source_index_check_count=0`, `source_index_consistent=true`,
`process_gate_open_authorized=false`, `blocker_state_changed=false`, and
`candidate_emission_authorized=false`; smoke now checks Markdown/JSON freshness with
`--require-sources-exist`, `--require-consistent`, and `--require-blocked`.
Step 107 adds a read-only dependency/freshness guard for that literature index. The canonical
report has `direct_source_report_count=6`, `source_ref_count=40`,
`literature_dependency_check_count=33`, `failed_literature_dependency_check_count=0`,
`literature_dependency_consistent=true`, `literature_source_count=15`, `pdf_count=14`,
`html_count=1`, `search_log_count=3`, `proof_promotion_blocker_count=3`,
`closure_verdict=blocked_no_discharge`, `closure_unresolved_branch_count=3`,
`direct_discharge_source_count=0`, `closure_discharged_blocker_count=0`,
`closure_direct_known_route_count=0`, `process_gate_open_authorized=false`,
`blocker_state_changed=false`, `candidate_emission_authorized=false`, and
`missing_source_count=0`; smoke now checks Markdown/JSON freshness with
`--require-sources-exist`, `--require-consistent`, and `--require-blocked`.
Step 109 adds a dependency/freshness guard for that matrix. The canonical report has
`direct_source_report_count=10`, `source_ref_count=63`,
`literature_gap_dependency_check_count=38`,
`failed_literature_gap_dependency_check_count=0`,
`literature_gap_dependency_consistent=true`, `literature_source_count=15`, `gap_count=8`,
`source_gap_edge_count=45`, `blocked_gap_count=8`, `actionable_gap_count=0`,
`may_discharge_gap_count=0`, `direct_discharge_source_count=0`,
`analytic_gap_stack_consistent=true`, `operator_stack_consistent=true`,
`process_gate_open_authorized=false`, `blocker_state_changed=false`,
`candidate_emission_authorized=false`, and `missing_source_count=0`; smoke now checks Markdown/JSON
freshness with `--require-sources-exist`, `--require-consistent`, and `--require-blocked`.
Step 108 maps the same literature inventory onto the eight Step 102 analytic-discharge gaps. The
canonical report has `literature_source_count=15`, `gap_count=8`, `source_gap_edge_count=45`,
`source_with_gap_count=15`, `unmapped_source_count=0`,
`gap_with_literature_source_count=5`, `gap_without_literature_source_count=3`,
`direct_branch_edge_count=12`, `closure_bundle_edge_count=30`, `blocked_gap_count=8`,
`actionable_gap_count=0`, `may_discharge_gap_count=0`,
`direct_discharge_source_count=0`, `literature_dependency_consistent=true`,
`gap_stack_consistent=true`, `process_gate_open_authorized=false`,
`blocker_state_changed=false`, `candidate_emission_authorized=false`, and
`missing_source_count=0`; smoke now checks Markdown/JSON freshness with
`--require-sources-exist`, `--require-consistent`, and `--require-blocked`.

### Formal Track

The local Lean project builds and contains small, explicit artifacts:

- `NavierStokesProgram/HeatSemigroup.lean`: discrete Fourier-mode heat multiplier algebra;
- `NavierStokesProgram/SolutionClasses.lean`: typed separation of smooth, weak, Leray-Hopf, and
  suitable weak vocabulary;
- `NavierStokesProgram/SpectralTail.lean`: finite-mode spectral-tail diagnostic vocabulary;
- `NavierStokesProgram/ShellProjector.lean`: finite shell-projector and alpha=1 dyadic flux
  budget vocabulary;
- `NavierStokesProgram/ParabolicCylinder.lean`: finite parabolic-cylinder and beta=1 Morrey
  envelope vocabulary;
- `NavierStokesProgram/LocalEnergy.lean`: finite suitable-weak local energy inequality metadata;
- `NavierStokesProgram/ProofObligationGraph.lean`: finite graph metadata for `lemma_0252`
  proof obligations and promotion blockers;
- `NavierStokesProgram/DuhamelBilinear.lean`: finite Duhamel bilinear bookkeeping vocabulary;
- `NavierStokesProgram/CandidateGate.lean`: candidate-generation audit gate vocabulary;
- `NavierStokesProgram/CandidateGateExamples.lean`: buildable examples for complete audit,
  incomplete audit, and blocked weak-to-smooth class jumps;
- `NavierStokesProgram/CandidateObligationBridge.lean`: accessor bridge from v4 candidate gates
  to proof-obligation graph blockers;
- `promotion/lemma_0001.lean`: BKM statement skeleton as a typechecked proposition, not a proof.

Upstream contribution:

- PR: <https://github.com/google-deepmind/formal-conjectures/pull/4021>
- Patch: proves `divergence_add` and `divergence_smul` in the DeepMind Navier-Stokes file.
- Verification: local `lake --wfail build` passed with `8709 jobs`.
- Caveat: merge is blocked until Google CLA is signed for `soave0529-oss`.

## Limitations

The project has not produced a new theorem, proof, or blow-up construction.

The main current limitations are:

- current candidate generation still rediscovers BKM variants too easily unless constrained;
- pressure-related candidate language is underdefined;
- Taylor-Green long-time enstrophy matching remains below DNS-quality acceptance;
- Lean artifacts are vocabulary and toy algebra, not NSE regularity theory;
- external expert review has been queued but not performed.

## Next Quarter Plan

Recommended direction: hybrid Track A + Track C, with Track B kept as falsifier support.

Immediate next work:

1. Add a known-result registry note for localized vortex-stretching and strain/vorticity geometric
   criteria before rewriting those candidate families. Done in Step 40; evaluator hook done in Step 41.
2. Done in Step 58: no v4 seed was emitted because no credible exact route was available; Track C
   candidate-gate examples were added instead.
3. Done in Step 59: v4 preflight is now an executable CLI gate before future candidate emission.
4. Done in Step 60: the reproducibility smoke workflow now runs the v4 preflight gate.
5. Done in Step 61: active candidate emission is frozen behind v4 gates; next branch is Track C
   local-energy/suitable-weak vocabulary.
6. Step 62 started that branch with finite local-energy/suitable-weak vocabulary.
7. Step 63 mapped local-energy vocabulary to `lemma_0252` obligations while keeping the analytic
   blockers open.
8. Step 64 added proof-obligation graph vocabulary for `lemma_0252`, with missing mechanisms kept
   as blockers rather than claims.
9. Step 65 exposed the graph as a Track A report sidecar without changing candidate status.
10. Step 66 wired the report freshness check into reproducibility smoke.
11. Step 67 connected `CandidateGate` audit metadata to proof-obligation graph blockers through a
    finite Lean accessor layer.
12. Step 68 added a JSON export and JSON freshness smoke hook for the proof-obligation report.
13. Step 69 added a JSON blocker-summary CLI and active-candidate-with-blockers consistency check.
14. Step 70 added Markdown/JSON blocker summary dashboards and freshness smoke checks.
15. Step 71 connected the zero-blocker requirement to v4 preflight and future candidate metadata.
16. Step 72 added a blocked-by-default candidate proof-obligation report/summary template generator.
17. Step 73 added a small registry/report for existing `needs_review` records and whether each
    has a candidate-specific proof-obligation scaffold.
18. Step 74 generated blocked-by-default Step 72 scaffold report/summary JSON pairs for the seven
    existing `needs_review` records and made registry smoke require `present_blocked`.
19. Step 75 added a family-specific blocker matrix that maps generic template obligations to the
    real Duhamel, dyadic-flux, and parabolic-Morrey blockers without generating an active
    candidate.
20. Step 76 connected the family-specific matrix back to individual scaffold records and added a
    consistency guard over scaffold promotion keys and matrix families.
21. Step 77 added source/provenance references for each family-specific blocker row and a
    `--require-source-refs` smoke guard.
22. Step 78 added a compact source/provenance dashboard derived from matrix `source_refs` and
    wired Markdown/JSON freshness plus source-existence checks into smoke.
23. Step 79 connected the blocker source index to future v4/preflight metadata through
    `V4:FreshBlockerSourceIndex` and source-index Markdown/JSON fields.
24. Step 80 added a generated v4 candidate metadata checklist and blocked-by-default template
    example outside the active candidate pool.
25. Step 81 added a staging audit for future proposed candidate YAML before anything is copied
    into `track-a-regularity/candidates/`.
26. Step 82 added a manual promotion packet report that lists the exact artifacts required before
    any staged `ready_for_manual_copy` YAML can enter the active candidate directory.
27. Step 83 added an active-pool ingress audit that fails if staged/template/v4-like YAML enters
    `track-a-regularity/candidates/` without a matching ready manual promotion packet.
28. Step 84 added a promotion lifecycle dashboard that ties Step 81
    staging, Step 82 manual packet, and Step 83 ingress statuses into one no-copy review surface.
29. Step 85 added an end-to-end temporary promotion dry-run fixture that exercises a
    synthetic ready candidate through staging, packet, lifecycle, and temp ingress checks without
    touching the real active candidate directory.
30. Step 86 added a read-only promotion gate regression dashboard that explains why the temporary
    dry-run is necessary but not sufficient for real candidate emission.
31. Step 87 mapped the three substantive `lemma_0252` proof-obligation blockers to known theorem
    families and found no direct known theorem route; the artifact remains read-only and blocked.
32. Step 88 turned the Step 87 mapping into a read-only compactness/Liouville branch checklist;
    the branch remains deferred and has zero directly dischargeable known route.
33. Step 89 added a read-only finite-bound-to-smallness checklist; the branch remains deferred
    and has zero directly dischargeable known route.
34. Step 90 added the analogous read-only smooth-continuation bridge checklist; BKM,
    Prodi-Serrin, high-Sobolev, Constantin-Fefferman, and terminal-cover routes still discharge
    zero blockers.
35. Step 91 joined Steps 87-90 into a read-only `lemma_0252` blocker-closure dashboard; all three
    substantive branches are present but unresolved, and checklist presence cannot authorize
    active candidate emission.
36. Step 92 connected the Step 91 closure dashboard back into the existing promotion gate
    regression surface, so real-emission blockers now depend directly on
    `closure_verdict=blocked_no_discharge`.
37. Step 93 added a read-only closure-dependency consistency guard so promotion gate regression
    cannot silently drift away from the Step 91 closure dashboard it cites.
38. Step 94 added a read-only promotion-gate blocker ledger that classifies the six
    promotion-blocking gates by action family before any future work tries to discharge one.
39. Step 95 added a read-only action-readiness guard that prevents process blockers from being
    treated as actionable before the analytic proof-obligation and closure blockers move.
40. Step 96 added a read-only analytic-blocker discharge-prerequisite packet for the tier-1
    `proof_obligation` and `closure` families, without opening process gates or promoting any
    candidate.
41. Step 97 added a read-only dependency/freshness consistency guard so the Step 96 packet cannot
    drift away from the Step 95 action-readiness report, the proof-obligation graph, or the Step
    91 closure dashboard it cites.
42. Step 98 added a read-only analytic discharge work-order matrix for the eight Step 96
    prerequisites, grouped by required artifact type and source branch, without changing blocker
    state.
43. Step 99 added a blocked-by-default analytic discharge template audit for the Step 98
    work-order types. All eight templates remain blocked, non-actionable, and non-promotional.
44. Step 100 added a read-only dependency/freshness guard for the Step 99 template audit so it
    cannot drift from the Step 98 matrix, Step 96 prerequisites, or Step 97 dependency report.
45. Step 101 consolidated the analytic-discharge gate stack into a compact operator
    dashboard/index across Steps 96-100, preserving read-only status and zero candidate emission.
46. Step 102 added a read-only discharge-artifact gap index that maps the eight blocked Step
    98/99 work-order/template types to missing concrete theorem/formal artifacts and required
    review evidence, without opening process gates or making templates actionable.
47. Step 103 added a read-only dependency/freshness guard so the Step 102 gap index cannot drift
    from the Step 101 operator dashboard, Step 100 template-dependency guard, Step 99 template
    audit, or Step 98 work-order matrix.
48. Step 104 added a compact read-only operator/source index for the Step 102-103 gap artifacts,
    preserving blocked and non-actionable status for all eight gaps.
49. Step 105 added a read-only dependency/freshness guard so the Step 104 operator index cannot
    drift from the Step 102-103 canonical reports or broader analytic-discharge dashboard.
50. Step 106 used the collected `papers/blockers/` literature to build a read-only
    blocker-literature source index for the three substantive `lemma_0252` blockers and
    cross-cutting anchors, without changing blocker state.
51. Step 107 added that read-only dependency/freshness guard, tying the Step 106 literature index
    to `papers/blockers/index.md`, the `lemma_0252` proof-obligation graph, and the Step 91
    closure dashboard without changing blocker state.
52. Step 108 added that read-only literature attack-order/source-to-gap dashboard. The direct
    analytic attack order is finite-bound-to-smallness, compactness/Liouville, smooth continuation,
    then branch/closure bundles; metadata/process gaps stay non-literature-actionable.
53. Step 109 added that read-only dependency/freshness guard so the Step 108 gap matrix cannot
    drift from the Step 106 literature index, Step 107 literature dependency guard, Step 102
    analytic-discharge gap index, or Step 101 analytic-discharge dashboard.
54. Step 110 added that compact read-only operator/source index for the Step 108-109
    literature-gap artifacts, keeping all eight gaps blocked, non-actionable, and
    non-dischargeable.
55. Step 111 added a read-only dependency/freshness guard so the Step 110 literature-gap operator
    index cannot drift from the Step 108/109 canonical reports or the broader Step 106/107
    literature stack.
56. Step 112 added a read-only, non-promotional theorem-artifact review queue for direct analytic
    gaps `gap_002`, `gap_003`, and `gap_004`, mapping them to the local blocker literature and
    missing theorem/formal artifacts without changing blocker state.
57. Step 113 added a read-only dependency/freshness guard so the Step 112 queue cannot drift from
    the Step 102 analytic-discharge gap index, the Step 108-111 blocker-literature gap stack, or
    `papers/blockers/index.md`.
58. Step 114 added a compact read-only operator/source index consolidating the Step 112 queue and
    Step 113 queue-dependency guard while preserving blocked/non-actionable status for every queue
    item.
59. Step 115 added a read-only dependency/freshness guard so the Step 114 queue operator index
    cannot drift from the Step 112-113 queue stack, Step 102 analytic gap index, Step 108-111
    blocker-literature gap stack, or `papers/blockers/index.md`.
60. Step 116 added a read-only source-read packet for `gap_002` finite-bound-to-smallness,
    extracting theorem-hypothesis shape, conclusion shape, and mismatch fields from the seven
    local queue sources while keeping the branch blocked and non-actionable.
61. Step 117 added a read-only dependency/freshness guard so the Step 116 source-read packet
    cannot drift from the Step 89 finite-bound checklist, the Step 112-115 theorem-artifact queue
    stack, or `papers/blockers/index.md`; `gap_002` remains blocked and non-actionable.
62. Step 118 added a read-only source-read packet for `gap_003` compactness/Liouville, extracting
    theorem-hypothesis shape, conclusion shape, and mismatch fields from the six local queue
    sources while keeping the branch blocked and non-actionable.
63. Step 119 added a read-only dependency/freshness guard so the Step 118 source-read packet
    cannot drift from the Step 88 compactness/Liouville checklist, the Step 112-115
    theorem-artifact queue stack, or `papers/blockers/index.md`; `gap_003` remains blocked and
    non-actionable.
64. Step 120 added a read-only source-read packet for `gap_004` smooth-continuation, extracting
    theorem-hypothesis shape, conclusion shape, and mismatch fields from the two local queue
    sources while keeping the branch blocked and non-actionable.
65. Step 121 added a read-only dependency/freshness guard so the Step 120 source-read packet
    cannot drift from the Step 90 smooth-continuation checklist, the Step 112-115
    theorem-artifact queue stack, or `papers/blockers/index.md`; `gap_004` remains blocked and
    non-actionable.
66. Step 122 added a compact read-only operator/source index consolidating the Step 120
    smooth-continuation source-read packet and Step 121 dependency guard while keeping `gap_004`
    blocked and non-actionable.
67. Step 123 added a read-only dependency/freshness guard so the Step 122 smooth-continuation
    source-read operator/source index cannot drift from Step 120, Step 121, Step 90, the Step
    112-115 theorem-artifact queue stack, or `papers/blockers/index.md`; `gap_004` remains
    blocked and non-actionable.
68. Step 124 added a compact read-only operator/source dashboard consolidating the Step 120-123
    smooth-continuation source-read stack while keeping `gap_004` blocked and non-actionable.
69. Step 125 added a compact read-only cross-gap source-read status dashboard consolidating
    `gap_002` finite-bound-to-smallness, `gap_003` compactness/Liouville, and `gap_004`
    smooth-continuation source-read packets/dependency guards into one review surface. The
    canonical report has `gap_count=3`, `source_read_count=15`,
    `blocked_source_read_count=15`, `actionable_source_read_count=0`,
    `may_discharge_source_read_count=0`, `exact_discharge_artifact_count=0`,
    `cross_gap_source_read_status_dashboard_check_count=61`,
    `failed_cross_gap_source_read_status_dashboard_check_count=0`, and
    `candidate_emission_authorized=false`.
70. Step 126 added a read-only dependency/freshness guard so the Step 125 cross-gap source-read
    status dashboard cannot drift from Steps 116-124 packet/dependency/operator/stack reports,
    Steps 112-115 theorem-artifact queue reports, Step 89/88/90 branch checklists, or
    `papers/blockers/index.md`. The canonical report has `direct_source_report_count=34`,
    `source_ref_count=104`,
    `cross_gap_source_read_status_dashboard_dependency_check_count=55`,
    `failed_cross_gap_source_read_status_dashboard_dependency_check_count=0`,
    `source_read_count=15`, `blocked_source_read_count=15`,
    `exact_discharge_artifact_count=0`, and `candidate_emission_authorized=false`.
71. Step 127 added a compact read-only operator/source dashboard consolidating the Step 125-126
    cross-gap source-read status stack. The canonical report has `stack_step_count=2`,
    `source_report_count=4`, `source_ref_count=106`,
    `cross_gap_source_read_status_stack_dashboard_check_count=50`,
    `failed_cross_gap_source_read_status_stack_dashboard_check_count=0`,
    `source_read_count=15`, `blocked_source_read_count=15`,
    `exact_discharge_artifact_count=0`, `process_gate_open_authorized=false`, and
    `candidate_emission_authorized=false`.
72. Step 128 added a read-only dependency/freshness guard so the Step 127 cross-gap source-read
    status stack dashboard cannot drift from Step 125, Step 126, Steps 116-124 source-read
    reports, Steps 112-115 queue reports, Step 89/88/90 branch checklists, or
    `papers/blockers/index.md`. The canonical report has `direct_source_report_count=69`,
    `source_ref_count=108`,
    `cross_gap_source_read_status_stack_dashboard_dependency_check_count=60`,
    `failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count=0`,
    `canonical_json_matches_fresh_build=true`, `canonical_markdown_matches_fresh_build=true`,
    `stack_json_compact=true`, `source_read_count=15`, `blocked_source_read_count=15`,
    `exact_discharge_artifact_count=0`, `process_gate_open_authorized=false`, and
    `candidate_emission_authorized=false`.
73. Step 129 added a compact read-only operator/source index consolidating the Step 127-128
    cross-gap source-read status stack. The canonical report has `section_count=2`,
    `source_report_count=4`, `source_ref_count=110`,
    `cross_gap_source_read_status_stack_operator_index_check_count=55`,
    `failed_cross_gap_source_read_status_stack_operator_index_check_count=0`,
    `cross_gap_source_read_status_stack_operator_index_consistent=true`,
    `stack_json_compact=true`, `source_read_count=15`, `blocked_source_read_count=15`,
    `exact_discharge_artifact_count=0`, `process_gate_open_authorized=false`, and
    `candidate_emission_authorized=false`.
74. Step 130 added one Vasseur 2007 row to the `finite_bound_to_smallness` known-theorem mapping.
    The canonical mapping now has `row_count=10`, `finite_bound_to_smallness` row count `4`,
    `resolvable_known_count=0`, `resolvable_needs_new_result_count=8`, and
    `permanently_blocked_count=2`. The Vasseur verdict is `resolvable_needs_new_result`, not a
    discharge: Theorem 1/2 require small local velocity-gradient-pressure or scaled-gradient
    input, while `lemma_0252` supplies only finite critical parabolic Morrey/vorticity-enstrophy
    boundedness. Full smoke passed at `logs/repro_20260523_172110/summary.md`.
75. Step 131 refined the existing KNSS row in the `compactness_liouville` known-theorem mapping.
    The canonical mapping stays at `row_count=10`, with `compactness_liouville` row count `3`,
    `resolvable_known_count=0`, and `permanently_blocked_count=2`. The KNSS verdict remains
    `permanently_blocked`: KNSS provides a bounded ancient mild/weak Liouville template, but the
    proved 3D branches are axisymmetric or special-geometry, the general 3D bounded ancient
    problem is open, and `lemma_0252` lacks the bounded-velocity ancient compactness,
    pressure/local-energy, and nontriviality package. Full smoke passed at
    `logs/repro_20260523_182837/summary.md`.
76. Step 132 added a companion Tao 2013 localisation/compactness verdict note for
    `compactness_liouville`. The verdict is `resolvable_needs_new_result`, not a discharge: Tao
    gives formulation-level implication, localisation, and concentration-compactness machinery,
    but Theorem 10.1 starts from small local enstrophy on a controlled time scale and the paper
    does not construct the required nonzero ancient suitable limit, pressure/local-energy
    compactness, or Liouville/backward-uniqueness contradiction from the `lemma_0252` finite
    critical Morrey/vorticity-enstrophy envelope. Full smoke passed at
    `logs/repro_20260523_194059/summary.md`.
77. Step 133 refined the existing ESS backward-uniqueness row in the `compactness_liouville`
    known-theorem mapping. The canonical mapping stays at `row_count=10`, with
    `compactness_liouville` row count `3`, `resolvable_known_count=0`, and
    `permanently_blocked_count=2`. The ESS verdict remains `resolvable_needs_new_result`:
    the route requires endpoint critical velocity control such as `L-infinity_t L3_x`, a
    compatible ancient or terminal limit, boundedness/decay for the Carleman/backward-uniqueness
    theorem, and pressure/vorticity regularity. The local `1509.04940` source is treated only as a
    caution source, and `lemma_0252` still supplies finite critical parabolic Morrey/
    vorticity-enstrophy metadata rather than the endpoint velocity, compactness/nontriviality, or
    backward-uniqueness hypothesis package. Full smoke passed at
    `logs/repro_20260523_205218/summary.md`.
78. Step 134 added a companion Tao 2013 finite-bound-to-smallness verdict note for `gap_002`.
    The verdict is `resolvable_needs_new_result`, not a discharge: Tao 2013 Theorem 10.1 assumes
    small local initial vorticity plus curl-force input and a short-time smallness condition, then
    propagates local enstrophy and vorticity-gradient control. It does not convert a merely finite
    critical parabolic Morrey/vorticity-enstrophy bound into the CKN epsilon-small
    velocity-pressure-local-energy package required by `lemma_0252`. The companion report records
    `applies_directly=false`, `blocker_state_changed=false`, and
    `candidate_emission_authorized=false`. Full smoke passed at
    `logs/repro_20260523_215246/summary.md`.
79. Step 135 added a companion Wang 2023 finite-bound-to-smallness verdict note for `gap_002`.
    The verdict is `resolvable_needs_new_result`, not a discharge: Wang 2023 gives a modern
    small-energy partial-regularity route, including a pressure compactness mechanism, but its
    theorem assumes `E_r <= epsilon2` at all small scales. Lemmas 9 and 10 propagate decay after
    that smallness is present; they do not convert a merely finite critical parabolic Morrey/
    vorticity-enstrophy bound into the CKN epsilon-small velocity-pressure-local-energy package.
    The companion report records `applies_directly=false`, `blocker_state_changed=false`, and
    `candidate_emission_authorized=false`. Full smoke passed at
    `logs/repro_20260523_225734/summary.md`.
80. Step 136 added a companion Lei-Ren 2022 quantitative partial-regularity finite-bound-to-smallness
    verdict note for `gap_002`. The verdict is `resolvable_needs_new_result`, not a discharge:
    Lei-Ren improves the CKN partial-regularity gauge and gives quantitative regular strips or
    epochs, but the general branch still needs epsilon smallness or pigeonhole-produced sparse-scale
    smallness for measure/region conclusions. The strongest one-point criteria are
    axisymmetric/small-swirl results outside the general periodic `lemma_0252` setting. The
    companion report records `applies_directly=false`, `blocker_state_changed=false`, and
    `candidate_emission_authorized=false`. Full smoke passed at
    `logs/repro_20260523_235231/summary.md`.
81. Step 137 created the first Stage 1 theorem-generation technique card at
    `pipeline/stage1/tao2013_localisation/technique_card.md`. The card digests Tao 2013
    localisation as a reusable technique rather than a verdict row: localised enstrophy,
    Proposition 9.1 total-speed control, Theorem 10.1, the shrinking-radius Lipschitz cutoff,
    boundary-radius pigeonhole, sharpness points, `lemma_0252` distance, and four Stage 2
    recombination seeds. It adds no dashboard, candidate YAML, gate opening, or blocker discharge.
    Full Python suite passed with `497 passed`; all 252 candidates still matched expected status.
82. Step 138 added the Stage 1 exit/value assessment at
    `pipeline/stage1/tao2013_localisation/stage2_value_assessment.md`. The decision is
    `GO_LIMITED_TO_ONE_STAGE2_OBSTACLE_TREE`: select only
    `ckn_pressure_package_plus_tao_local_vorticity_cutoff` and analyze the obstacle
    `tao_ckn_pressure_local_energy_transfer`. This keeps the theorem-generation path bounded and
    adds no dashboard, candidate YAML, promotion metadata, gate opening, or blocker discharge.
    Focused Stage 1 tests passed with `6 passed`; all 252 candidates still matched expected status
    and preflight remained `checked=0 skipped=252 blocked=0`.
83. Extend Track C vocabulary only in finite, buildable increments. Shell-projector records and
   parabolic cylinder placeholders are done in Steps 42-43 and Duhamel bilinear vocabulary is done
   in Step 46. The candidate-family registry is drafted in Step 44 and critical-space known-overlap
   filtering is implemented in Step 45.
84. Use the expert review packet only after new non-redundant survivors exist.
85. Keep DNS-quality Taylor-Green work separate from the fast falsifier path.

Success criterion for the next phase:

- candidate survivors are no longer BKM variants by construction;
- at least one nontrivial but modest Lean infrastructure artifact is reusable outside this project;
- any externally reviewed candidate returns a precise "known/redundant/badly posed/promising"
  classification.

## Artifact Map

| artifact | path |
|---|---|
| roadmap | `docs/ROADMAP_STEPS.md` |
| theorem map | `docs/THEOREM_MAP.md` |
| Step 6 decision | `docs/STEP6_DECISION.md` |
| BV guardrail catalog | `docs/BV_TECHNIQUES.md` |
| expert review queue | `docs/EXPERT_REVIEW_QUEUE.md` |
| candidate generation spec v4 | `docs/CANDIDATE_GENERATION_SPEC_V4.md` |
| candidate generation freeze | `docs/CANDIDATE_GENERATION_FREEZE.md` |
| theorem-generation Stage 1 Tao technique card | `pipeline/stage1/tao2013_localisation/technique_card.md` |
| theorem-generation Stage 1 Tao value assessment | `pipeline/stage1/tao2013_localisation/stage2_value_assessment.md` |
| candidate generation preflight CLI | `track-a-regularity/evaluator/preflight_v4.py` |
| lemma 0252 local-energy formal map | `docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md` |
| lemma 0252 proof-obligation graph | `docs/STEP64_PROOF_OBLIGATION_GRAPH.md` |
| lemma 0252 proof-obligation report | `track-a-regularity/reports/lemma_0252_proof_obligation_graph.md` |
| lemma 0252 proof-obligation JSON | `track-a-regularity/reports/lemma_0252_proof_obligation_graph.json` |
| proof-obligation blocker consistency CLI | `track-a-regularity/evaluator/proof_obligation_blockers.py` |
| proof-obligation blocker summary | `track-a-regularity/reports/proof_obligation_blocker_summary.md` |
| proof-obligation blocker summary JSON | `track-a-regularity/reports/proof_obligation_blocker_summary.json` |
| v4 zero-blocker gate doc | `docs/STEP71_V4_ZERO_BLOCKER_GATE.md` |
| candidate proof-obligation template generator | `track-a-regularity/evaluator/candidate_obligation_template.py` |
| needs-review obligation registry CLI | `track-a-regularity/evaluator/needs_review_obligation_registry.py` |
| needs-review obligation registry | `track-a-regularity/reports/needs_review_obligation_registry.md` |
| needs-review obligation registry JSON | `track-a-regularity/reports/needs_review_obligation_registry.json` |
| needs-review blocked scaffold reports | `track-a-regularity/reports/lemma_02*_proof_obligations.json` |
| needs-review blocked scaffold summaries | `track-a-regularity/reports/lemma_02*_proof_obligation_summary.json` |
| needs-review blocker matrix CLI | `track-a-regularity/evaluator/needs_review_blocker_matrix.py` |
| needs-review blocker matrix | `track-a-regularity/reports/needs_review_blocker_matrix.md` |
| needs-review blocker matrix JSON | `track-a-regularity/reports/needs_review_blocker_matrix.json` |
| needs-review scaffold/matrix consistency guard | `track-a-regularity/evaluator/needs_review_blocker_matrix.py --require-scaffold-matrix-consistency` |
| needs-review blocker provenance guard | `track-a-regularity/evaluator/needs_review_blocker_matrix.py --require-source-refs` |
| needs-review blocker source index CLI | `track-a-regularity/evaluator/needs_review_blocker_sources.py` |
| needs-review blocker source index | `track-a-regularity/reports/needs_review_blocker_sources.md` |
| needs-review blocker source index JSON | `track-a-regularity/reports/needs_review_blocker_sources.json` |
| v4 source-index preflight gate | `track-a-regularity/evaluator/generation_spec_v4.py` |
| v4 metadata checklist CLI | `track-a-regularity/evaluator/v4_metadata_checklist.py` |
| v4 metadata checklist | `track-a-regularity/reports/v4_candidate_metadata_checklist.md` |
| v4 metadata checklist JSON | `track-a-regularity/reports/v4_candidate_metadata_checklist.json` |
| v4 blocked candidate template | `track-a-regularity/templates/v4_blocked_candidate_template.yaml` |
| proposed candidate staging CLI | `track-a-regularity/evaluator/proposed_candidate_staging.py` |
| proposed candidate staging audit | `track-a-regularity/reports/proposed_candidate_staging_audit.md` |
| proposed candidate staging audit JSON | `track-a-regularity/reports/proposed_candidate_staging_audit.json` |
| manual promotion packet CLI | `track-a-regularity/evaluator/manual_promotion_packet.py` |
| manual promotion packet | `track-a-regularity/reports/manual_promotion_packet.md` |
| manual promotion packet JSON | `track-a-regularity/reports/manual_promotion_packet.json` |
| active-pool ingress audit CLI | `track-a-regularity/evaluator/active_pool_ingress_audit.py` |
| active-pool ingress audit | `track-a-regularity/reports/active_pool_ingress_audit.md` |
| active-pool ingress audit JSON | `track-a-regularity/reports/active_pool_ingress_audit.json` |
| promotion lifecycle dashboard CLI | `track-a-regularity/evaluator/promotion_lifecycle_dashboard.py` |
| promotion lifecycle dashboard | `track-a-regularity/reports/promotion_lifecycle_dashboard.md` |
| promotion lifecycle dashboard JSON | `track-a-regularity/reports/promotion_lifecycle_dashboard.json` |
| promotion dry-run fixture CLI | `track-a-regularity/evaluator/promotion_dry_run_fixture.py` |
| promotion dry-run fixture | `track-a-regularity/reports/promotion_dry_run_fixture.md` |
| promotion dry-run fixture JSON | `track-a-regularity/reports/promotion_dry_run_fixture.json` |
| promotion gate regression CLI | `track-a-regularity/evaluator/promotion_gate_regression.py` |
| promotion gate regression | `track-a-regularity/reports/promotion_gate_regression.md` |
| promotion gate regression JSON | `track-a-regularity/reports/promotion_gate_regression.json` |
| promotion gate blocker ledger CLI | `track-a-regularity/evaluator/promotion_gate_blocker_ledger.py` |
| promotion gate blocker ledger | `track-a-regularity/reports/promotion_gate_blocker_ledger.md` |
| promotion gate blocker ledger JSON | `track-a-regularity/reports/promotion_gate_blocker_ledger.json` |
| promotion gate action-readiness CLI | `track-a-regularity/evaluator/promotion_gate_action_readiness.py` |
| promotion gate action-readiness | `track-a-regularity/reports/promotion_gate_action_readiness.md` |
| promotion gate action-readiness JSON | `track-a-regularity/reports/promotion_gate_action_readiness.json` |
| promotion gate analytic prerequisites CLI | `track-a-regularity/evaluator/promotion_gate_analytic_prerequisites.py` |
| promotion gate analytic prerequisites | `track-a-regularity/reports/promotion_gate_analytic_prerequisites.md` |
| promotion gate analytic prerequisites JSON | `track-a-regularity/reports/promotion_gate_analytic_prerequisites.json` |
| promotion gate analytic-prerequisite dependency CLI | `track-a-regularity/evaluator/promotion_gate_analytic_prerequisite_dependency.py` |
| promotion gate analytic-prerequisite dependency | `track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.md` |
| promotion gate analytic-prerequisite dependency JSON | `track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.json` |
| promotion gate analytic work-order matrix CLI | `track-a-regularity/evaluator/promotion_gate_analytic_work_order_matrix.py` |
| promotion gate analytic work-order matrix | `track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.md` |
| promotion gate analytic work-order matrix JSON | `track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.json` |
| promotion gate analytic discharge templates CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_templates.py` |
| promotion gate analytic discharge templates | `track-a-regularity/reports/promotion_gate_analytic_discharge_templates.md` |
| promotion gate analytic discharge templates JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_templates.json` |
| promotion gate analytic discharge template dependency CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_template_dependency.py` |
| promotion gate analytic discharge template dependency | `track-a-regularity/reports/promotion_gate_analytic_discharge_template_dependency.md` |
| promotion gate analytic discharge template dependency JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_template_dependency.json` |
| promotion gate analytic discharge operator dashboard CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_operator_dashboard.py` |
| promotion gate analytic discharge operator dashboard | `track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md` |
| promotion gate analytic discharge operator dashboard JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json` |
| promotion gate analytic discharge gap index CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_index.py` |
| promotion gate analytic discharge gap index | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md` |
| promotion gate analytic discharge gap index JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json` |
| promotion gate analytic discharge gap dependency CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_dependency.py` |
| promotion gate analytic discharge gap dependency | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_dependency.md` |
| promotion gate analytic discharge gap dependency JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_dependency.json` |
| promotion gate analytic discharge gap operator index CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_operator_index.py` |
| promotion gate analytic discharge gap operator index | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_operator_index.md` |
| promotion gate analytic discharge gap operator index JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_operator_index.json` |
| promotion gate analytic discharge gap operator dependency CLI | `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_operator_dependency.py` |
| promotion gate analytic discharge gap operator dependency | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_operator_dependency.md` |
| promotion gate analytic discharge gap operator dependency JSON | `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_operator_dependency.json` |
| lemma 0252 known-theorem mapping CLI | `track-a-regularity/evaluator/lemma_0252_blocker_known_theorem_mapping.py` |
| lemma 0252 known-theorem mapping | `track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md` |
| lemma 0252 known-theorem mapping JSON | `track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.json` |
| lemma 0252 compactness/Liouville checklist CLI | `track-a-regularity/evaluator/lemma_0252_compactness_liouville_checklist.py` |
| lemma 0252 compactness/Liouville checklist | `track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.md` |
| lemma 0252 compactness/Liouville checklist JSON | `track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.json` |
| lemma 0252 finite-bound-to-smallness checklist CLI | `track-a-regularity/evaluator/lemma_0252_finite_bound_smallness_checklist.py` |
| lemma 0252 finite-bound-to-smallness checklist | `track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.md` |
| lemma 0252 finite-bound-to-smallness checklist JSON | `track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.json` |
| lemma 0252 smooth-continuation checklist CLI | `track-a-regularity/evaluator/lemma_0252_smooth_continuation_checklist.py` |
| lemma 0252 smooth-continuation checklist | `track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md` |
| lemma 0252 smooth-continuation checklist JSON | `track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json` |
| lemma 0252 blocker-closure dashboard CLI | `track-a-regularity/evaluator/lemma_0252_blocker_closure_dashboard.py` |
| lemma 0252 blocker-closure dashboard | `track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.md` |
| lemma 0252 blocker-closure dashboard JSON | `track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json` |
| lemma 0252 blocker-literature index CLI | `track-a-regularity/evaluator/lemma_0252_blocker_literature_index.py` |
| lemma 0252 blocker-literature index | `track-a-regularity/reports/lemma_0252_blocker_literature_index.md` |
| lemma 0252 blocker-literature index JSON | `track-a-regularity/reports/lemma_0252_blocker_literature_index.json` |
| lemma 0252 blocker-literature dependency CLI | `track-a-regularity/evaluator/lemma_0252_blocker_literature_dependency.py` |
| lemma 0252 blocker-literature dependency | `track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md` |
| lemma 0252 blocker-literature dependency JSON | `track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json` |
| lemma 0252 blocker-literature gap matrix CLI | `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_matrix.py` |
| lemma 0252 blocker-literature gap matrix | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md` |
| lemma 0252 blocker-literature gap matrix JSON | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json` |
| lemma 0252 blocker-literature gap dependency CLI | `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_dependency.py` |
| lemma 0252 blocker-literature gap dependency | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md` |
| lemma 0252 blocker-literature gap dependency JSON | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json` |
| lemma 0252 blocker-literature gap operator index CLI | `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_operator_index.py` |
| lemma 0252 blocker-literature gap operator index | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.md` |
| lemma 0252 blocker-literature gap operator index JSON | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.json` |
| lemma 0252 blocker-literature gap operator dependency CLI | `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_operator_dependency.py` |
| lemma 0252 blocker-literature gap operator dependency | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_dependency.md` |
| lemma 0252 blocker-literature gap operator dependency JSON | `track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_dependency.json` |
| lemma 0252 theorem artifact review queue CLI | `track-a-regularity/evaluator/lemma_0252_theorem_artifact_review_queue.py` |
| lemma 0252 theorem artifact review queue | `track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md` |
| lemma 0252 theorem artifact review queue JSON | `track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json` |
| lemma 0252 finite-bound source-read packet CLI | `track-a-regularity/evaluator/lemma_0252_finite_bound_smallness_source_read_packet.py` |
| lemma 0252 finite-bound source-read packet | `track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.md` |
| lemma 0252 finite-bound source-read packet JSON | `track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.json` |
| lemma 0252 finite-bound source-read dependency CLI | `track-a-regularity/evaluator/lemma_0252_finite_bound_smallness_source_read_packet_dependency.py` |
| lemma 0252 finite-bound source-read dependency | `track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet_dependency.md` |
| lemma 0252 finite-bound source-read dependency JSON | `track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet_dependency.json` |
| lemma 0252 compactness/Liouville source-read packet CLI | `track-a-regularity/evaluator/lemma_0252_compactness_liouville_source_read_packet.py` |
| lemma 0252 compactness/Liouville source-read packet | `track-a-regularity/reports/lemma_0252_compactness_liouville_source_read_packet.md` |
| lemma 0252 compactness/Liouville source-read packet JSON | `track-a-regularity/reports/lemma_0252_compactness_liouville_source_read_packet.json` |
| lemma 0252 compactness/Liouville source-read dependency CLI | `track-a-regularity/evaluator/lemma_0252_compactness_liouville_source_read_packet_dependency.py` |
| lemma 0252 compactness/Liouville source-read dependency | `track-a-regularity/reports/lemma_0252_compactness_liouville_source_read_packet_dependency.md` |
| lemma 0252 compactness/Liouville source-read dependency JSON | `track-a-regularity/reports/lemma_0252_compactness_liouville_source_read_packet_dependency.json` |
| lemma 0252 smooth-continuation source-read packet CLI | `track-a-regularity/evaluator/lemma_0252_smooth_continuation_source_read_packet.py` |
| lemma 0252 smooth-continuation source-read packet | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.md` |
| lemma 0252 smooth-continuation source-read packet JSON | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.json` |
| lemma 0252 smooth-continuation source-read dependency CLI | `track-a-regularity/evaluator/lemma_0252_smooth_continuation_source_read_packet_dependency.py` |
| lemma 0252 smooth-continuation source-read dependency | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet_dependency.md` |
| lemma 0252 smooth-continuation source-read dependency JSON | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet_dependency.json` |
| lemma 0252 smooth-continuation source-read operator index CLI | `track-a-regularity/evaluator/lemma_0252_smooth_continuation_source_read_packet_operator_index.py` |
| lemma 0252 smooth-continuation source-read operator index | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet_operator_index.md` |
| lemma 0252 smooth-continuation source-read operator index JSON | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet_operator_index.json` |
| lemma 0252 smooth-continuation source-read operator dependency CLI | `track-a-regularity/evaluator/lemma_0252_smooth_continuation_source_read_packet_operator_dependency.py` |
| lemma 0252 smooth-continuation source-read operator dependency | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md` |
| lemma 0252 smooth-continuation source-read operator dependency JSON | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json` |
| lemma 0252 smooth-continuation source-read stack dashboard CLI | `track-a-regularity/evaluator/lemma_0252_smooth_continuation_source_read_stack_dashboard.py` |
| lemma 0252 smooth-continuation source-read stack dashboard | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_stack_dashboard.md` |
| lemma 0252 smooth-continuation source-read stack dashboard JSON | `track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_stack_dashboard.json` |
| lemma 0252 cross-gap source-read status dashboard CLI | `track-a-regularity/evaluator/lemma_0252_cross_gap_source_read_status_dashboard.py` |
| lemma 0252 cross-gap source-read status dashboard | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_dashboard.md` |
| lemma 0252 cross-gap source-read status dashboard JSON | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_dashboard.json` |
| lemma 0252 cross-gap source-read status dashboard dependency CLI | `track-a-regularity/evaluator/lemma_0252_cross_gap_source_read_status_dashboard_dependency.py` |
| lemma 0252 cross-gap source-read status dashboard dependency | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_dashboard_dependency.md` |
| lemma 0252 cross-gap source-read status dashboard dependency JSON | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_dashboard_dependency.json` |
| lemma 0252 cross-gap source-read status stack dashboard CLI | `track-a-regularity/evaluator/lemma_0252_cross_gap_source_read_status_stack_dashboard.py` |
| lemma 0252 cross-gap source-read status stack dashboard | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_stack_dashboard.md` |
| lemma 0252 cross-gap source-read status stack dashboard JSON | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_stack_dashboard.json` |
| lemma 0252 cross-gap source-read status stack dashboard dependency CLI | `track-a-regularity/evaluator/lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.py` |
| lemma 0252 cross-gap source-read status stack dashboard dependency | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.md` |
| lemma 0252 cross-gap source-read status stack dashboard dependency JSON | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.json` |
| lemma 0252 cross-gap source-read status stack operator index CLI | `track-a-regularity/evaluator/lemma_0252_cross_gap_source_read_status_stack_operator_index.py` |
| lemma 0252 cross-gap source-read status stack operator index | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_stack_operator_index.md` |
| lemma 0252 cross-gap source-read status stack operator index JSON | `track-a-regularity/reports/lemma_0252_cross_gap_source_read_status_stack_operator_index.json` |
| candidate-obligation bridge | `track-c-formal/lean/NavierStokesProgram/CandidateObligationBridge.lean` |
| reproducibility script | `scripts/verify_reproducibility.sh` |
| Track A candidates | `track-a-regularity/candidates/` |
| Track A evaluator | `track-a-regularity/evaluator/` |
| Track B solver | `track-b-blowup/solver/pseudospectral.py` |
| Track C Lean project | `track-c-formal/lean/` |

## Bottom Line

The program is now a functioning verifier and triage scaffold. It has converted the original
"LLM may solve a math problem" premise into a bounded system that mostly falsifies, classifies,
or formalizes small pieces. The correct next move is to improve candidate novelty detection and
formal vocabulary, not to claim progress on the Clay problem itself.
