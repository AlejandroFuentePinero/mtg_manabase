# MTG Manabase Optimiser — Roadmap (foundation-first)

This project will be built in layers:
1) establish a minimal, correct foundation (Chapter 0)
2) add game mechanics modularly (Chapter 1)
3) add behaviour/preferences (Chapter 2)
4) add optimisation + recommendations + visuals (Chapters 3–5)

The intent is to keep each layer independently testable and switchable (including zero-count mechanics).

---

## Chapter 0 — Foundation: early-turn mana reliability (v0)
Purpose: define the “game engine” for turns 1–3 and produce trustworthy baseline probabilities.
Once this exists, all mechanics and behaviour become add-on modules.

### 0.1 Definitions and shared vocabulary
- Deck size = 60 only (for now)
- Turn model: play vs draw
  - Play: 7-card opener; no draw on turn 1
  - Draw: 7-card opener; draw on turn 1
- “Cards seen by turn T” definition (hand + draws + optional look effects later)
- Primary v0 metrics:
  - P(hit 2nd land by T2)
  - P(hit 3rd land by T3)
  reported separately for play vs draw.

### 0.2 Mulligan model (London mulligan, simplified keep heuristic)
- London mulligan:
  - Each mulligan: shuffle, draw 7
  - Keep after m mulligans: bottom m cards (final hand size 7−m)
- v0 keep policy:
  - keep decision depends ONLY on land count in the 7-card look
  - keep-range parameter, e.g. keep lands in {2,3,4,5}
  - max mulligans parameter (e.g. stop at 5 cards)
- v0 bottoming policy:
  - deterministic parameter (simple rule)
  - minimal version: bottom lands first if excess lands; otherwise bottom spells first
  - goal is not perfect realism, but a stable baseline to build on.

### 0.3 Baseline probability engine
- Two implementations:
  1) Analytic baseline (hypergeometric) for “no mulligan, no selection” sanity checks
  2) Simulation baseline (Monte Carlo) for London mulligan + bottoming
- The simulation must reduce to the analytic baseline when mulligans are disabled.

### 0.4 Acceptance checks (Chapter 0 is “done” when)
- For each land count L in a reasonable range (e.g., 18–28):
  - produce the four values:
    - play: P(2 by T2), P(3 by T3)
    - draw: P(2 by T2), P(3 by T3)
- Results are stable under reruns (within tolerance) at a fixed seed / large N
- Edge cases handled cleanly:
  - L=0 and L=60 (sanity)
  - keep ranges that make “always keep” or “almost always mull”
  - max mulligans = 0 vs 1 vs 2+
- Unit tests exist for:
  - probability bounds [0,1]
  - invariants (e.g., P(3 by T3) ≤ P(2 by T2) generally; play vs draw ordering makes sense)
- One notebook/report exists that visualises the baseline curves.

Deliverables:
- `docs/02_v0_rules.md` (exact turn order + mulligan/bottoming rule)
- baseline curves notebook: land count vs probability (play/draw)
- core simulation module + tests

---

## Chapter 1 — Add game mechanics as modules (v1)
Purpose: incorporate real deck features while preserving modularity and “zero counts” behavior.

Mechanics (added one-by-one, each toggleable):
- Cantrips: “extra looks” only if castable (mana-gated)
- Top manipulation: scry/surveil decisions when they occur
- Fetchlands: colour fixing first; thinning tracked separately (optional)
- Ramp: simple early ramp categories (mana next turn; land-to-battlefield; etc.)
- Taplands: tempo constraint (ETB tapped reduces usable mana on key turns)

Outputs remain the same as Chapter 0 (plus optional additional metrics), but now conditional on module settings.

Acceptance:
- Setting all module counts to zero reproduces Chapter 0 outputs.
- Each module has a minimal policy definition and tests.

---

## Chapter 2 — Player behaviour layer (v2)
Purpose: represent subjective choices as parameters, not hard-coded assumptions.

Introduce a “player profile”:
- Mulligan aggressiveness: keep ranges, max mulligans
- Flood vs screw tolerance: weights in an objective/utility function
- Sequencing preferences: e.g., when to cantrip, when to fetch, keep/bin rules for surveil

Output becomes:
- probabilities + “utility score” for a given profile
- sensitivity: how recommendations change with profile knobs

---

## Chapter 3 — Optimisation engine (v3)
Purpose: given a deck and constraints, find the best manabase under the chosen player profile.

Decision variables (initially):
- total land count
- mix of land types (basic/typed/tap/fetch/utility)
- tapland budget / life-loss budget

Constraints:
- colour requirements (added in v3.1 if not earlier)
- available land pool
- max taplands, max life loss, etc.

Deliverable:
- return “best” and “near-best” configurations + tradeoffs.

---

## Chapter 4 — Positioning and visual outputs (v4)
Purpose: make the optimisation understandable.

- Heatmaps that position the current deck vs optimal under the chosen profile
- “distance to optimal” summary
- show which constraint is binding (tapland budget, colour, land count, etc.)

---

## Chapter 5 — Recommendation system (v5)
Purpose: actionable changes rather than raw numbers.

- Suggest minimal edits:
  - +1 land, -1 spell
  - swap tapland → untapped source
  - adjust fetch/typed mix
- Rank recommendations by improvement per change and by cost (tempo/life/budget)

---

## Notes on colour constraints (planned)
A later milestone will incorporate “sources needed to cast spells on curve” requirements (e.g., UU by T2), integrated into the same simulation/optimisation framework.
