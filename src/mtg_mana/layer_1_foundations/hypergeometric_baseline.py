# src/mtg_mana/layer_1_foundations/hypergeometric_baseline.py

from __future__ import annotations

from scipy.stats import hypergeom


def land_prob(
    decksize: int = 60,
    land_count: int = 24,
    cards_seen: int = 8,
    lands_seen: int = 2,
) -> float:
    """
    Probability of seeing at least `lands_seen` lands in `cards_seen` cards from a deck.

    Models X ~ Hypergeometric(N=decksize, K=land_count, n=cards_seen) and returns P(X >= lands_seen).

    Notes:
    - This is a baseline probability utility (no mulligan process, no cantrips, no fetch/surveil/ramp).
    - Practical constraints are enforced for this project context (60-card competitive baseline).

    Parameters
    ----------
    decksize : int
        Total cards in deck (default 60).
    land_count : int
        Number of lands in deck.
    cards_seen : int
        Number of cards seen by a given point (e.g., by turn T).
    lands_seen : int
        Minimum number of lands desired among the seen cards.

    Returns
    -------
    float
        P(X >= lands_seen)
    """
    if decksize <= 0:
        raise ValueError("decksize must be a positive integer.")

    # Keep "practical" land-count bounds light; realism mostly comes from your sweep range.
    # This cap prevents absurd inputs while not over-constraining future work.
    if not (10 <= land_count <= decksize - 20):
        raise ValueError(
            "land_count must be between 10 and decksize-20 (inclusive) for this baseline."
        )

    # Cards seen: in this project we won't call this below 7, but allow 7 explicitly.
    if not (7 <= cards_seen <= decksize):
        raise ValueError("cards_seen must be between 7 and decksize (inclusive).")

    # lands_seen is bounded by what you could possibly see
    if not (0 <= lands_seen <= cards_seen):
        raise ValueError("lands_seen must be between 0 and cards_seen (inclusive).")

    prob = 1.0 - hypergeom.cdf(lands_seen - 1, decksize, land_count, cards_seen)
    return float(prob)
