# Layer 1 - Foundations

### 1.2.1 Turn/Deck Parameters
**Module:** `layer_1_foundations/deck_parameters.py`  
Defines baseline early-turn bookkeeping (play vs draw) and land-count sweep settings.

Outputs:
- `decksize`
- `dieroll`
- `land_count` (iterable sweep)
- `cards_seen_t1`, `cards_seen_t2`, `cards_seen_t3`, `cards_seen_t4`
- `cards_hand_t1`, `cards_hand_t2`, `cards_hand_t3`, `cards_hand_t4`

Notes:
- This is **not** a London mulligan simulator.
- `mulligan` is treated as a **final hand size adjustment** only (7 − mulligan).

### 1.2.2 Hypergeometric Baseline Probability
**Module:** `layer_1_foundations/hypergeometric_baseline.py`  
Analytic baseline probability utility for land-drop reliability (no mulligans, no selection).

Outputs:
- `land_prob(...) -> float` returning `P(X >= lands_seen)` where  
  `X ~ Hypergeometric(N=decksize, K=land_count, n=cards_seen)`
