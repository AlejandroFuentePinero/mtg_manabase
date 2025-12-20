## MTG Manabase Optimiser — Roadmap (landscape → positioning → recommendations)

This project builds a **probabilistic landscape of mana reliability** for competitive 60-card decks, then lets a user (deck + format + behaviour) see **where they sit in that landscape**, and finally returns **a small number of actionable “best moves”** to improve the deck’s mana architecture.

Core design principle: **everything is modular and toggleable**, and **turning modules off must reproduce the prior layer**.

---

## Layer 1 — Foundation: the probabilistic landscape (mana reliability)
Purpose: build a correct baseline engine and then expand it into a “real-deck” landscape by adding mechanics one at a time.

### ✅ 1.0 Definitions and shared vocabulary
- ✅ Deck size: **60** (v1 scope)
- ✅ Play vs draw model (explicit turn order, cards seen by T)
- ✅ Primary reliability metrics (initial set):
  - **P(2nd land by T2)**
  - **P(3rd land by T3)**
  - **P(4th land by T4)**
- ✅ Separate reporting for **play vs draw**

### 1.1 Mulligan + keep/bottom policy (behaviour-neutral baseline)
- London mulligan, parameterised:
  - keep-range based on land count (v0)
  - max mulligans
  - deterministic bottoming rule (simple, stable)
- Key requirement: with mulligans disabled, simulation matches analytic baseline.

### 1.2 Baseline probability engine (two implementations)
- ✅ Analytic (hypergeometric) baseline for sanity checks
- Monte Carlo simulation for mulligans + sequencing rules
- Acceptance checks:
  - probabilities in [0, 1]
  - monotonicity with land count
  - stable reruns
  - edge cases (L=0, L=60, always-keep / always-mull settings)

### 1.3 Add deck mechanisms (landscape expansion modules)
Each module is:
- toggleable (including zero-count behaviour)
- defined by a minimal policy (not “perfect play”, but consistent and inspectable)
- tested
- evaluated for its effect on the baseline curves

Modules (order roughly from highest signal to highest complexity):
1) **Taplands / tempo costs** (ETB tapped reduces usable mana on key turns)
2) **Fetchlands** (first as colour fixing; thinning tracked separately as optional)
3) **Surveil/scry/top selection** (policy: keep/bin rules, conditional on land needs)
4) **Cantrips** (mana-gated: only matter if castable; define when they’re cast)
5) **Ramp** (simple early ramp categories; how it changes land-drop odds)

Deliverable at end of Layer 1:
- a “landscape runner” that outputs probability curves and (later) utility curves across:
  - land count
  - land-type mix knobs (tap %, fetch %, surveil %, utility slots, etc.)
  - play vs draw

---

## Layer 1.5 — Colour feasibility tool (cast spells on curve)
Purpose: complement “how many lands?” with “**what colours and how many sources?**”.

### 1.5.1 Spell colour requirements model
- Inputs from decklist:
  - colours
  - pip intensity (e.g., **WW vs 1W**)
  - earliest turn you want to cast
- Outputs:
  - probabilistic colour targets: e.g., “P(UU by T2) ≥ threshold”
  - integrated constraints that can shift the recommended land count / composition

### 1.5.2 Manabase colour builder (constraint-based)
- Given a land pool (format legality), propose feasible colour distributions:
  - basics/duals/fetch/typed/tap/utility
- The output is **not** a single answer yet; it produces a **feasible region** that optimisation can search inside.

---

## Layer 2 — User positioning (deck + format + behaviour → where you sit)
Purpose: let a user input their deck + preferences and get a clear diagnosis.

Inputs:
- Decklist-derived features (curve, cantrips/ramp counts, pip requirements)
- Format constraints (land pool availability, especially fetch legality)
- Player behaviour knobs:
  - mulligan aggressiveness
  - tolerance to screw vs flood
  - sequencing preferences (when to cantrip, when to fetch, surveil keep/bin rules)

Outputs:
- The deck’s position on the landscape:
  - “you are here” on curves/heatmaps
  - which constraint is binding (tempo, colour, land count, etc.)
- Sensitivity:
  - how much the answer changes if behaviour assumptions change

---

## Layer 3 — Recommendations (top 3 improvement approaches)
Purpose: turn diagnosis into **actionable edits**, not just charts.

### 3.1 Objective / utility function
Rank configurations by an explicit utility that can weight:
- early screw risk (missing 2/3/4 land drops)
- flood risk (late excess lands, if included)
- tempo costs (taplands)
- life costs (shock/fetch patterns if applicable)
- colour-fail risk (missing required pips on curve)

### 3.2 Optimisation / search (practical, not overkill)
- Decision variables:
  - total land count
  - land-type mix (tap/fetch/surveil/utility/basic/dual)
- Constraints:
  - colour requirements (Layer 1.5)
  - format land pool
  - budgets (tap %, life-loss, utility slots)

### 3.3 Output format: “three moves”
Return the **top 3 approaches**, each framed as:
- minimal change (low disruption)
- moderate change (structural fix)
- aggressive change (maximises reliability/colour at a cost)

Each recommendation includes:
- expected gain in the key probabilities (and utility)
- what you pay (tempo/life/utility slots)
- what matchups/deck styles it suits (fast vs slow, low vs high curve)

---

## “Done” criteria for each layer
- **Layer 1 done:** baseline engine + module toggles + reproducible landscape curves.
- **Layer 1.5 done:** colour feasibility constraints integrate cleanly (can fail fast with clear reasons).
- **Layer 2 done:** user can input deck + behaviour and get a stable “positioning report”.
- **Layer 3 done:** system returns 3 ranked, explainable upgrade paths under format constraints.
