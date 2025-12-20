# src/mtg_mana/layer_1_foundations/deck_parameters.py

from __future__ import annotations

from typing import Any, Iterable


def params(
    decksize: int = 60,
    min_lands: int = 16,
    max_lands: int = 29,
    land_count: Iterable[int] | None = None,
    mulligan: int = 0,
    dieroll: str = "Play",
) -> dict[str, Any]:
    """
    Return bookkeeping parameters for early turns (T1–T4) for a 60-card baseline model.

    Computes cards-in-hand and cards-seen counts for turns 1–4 given:
    - deck size
    - land-count sweep range
    - play vs draw (draw gets an extra card on T1)
    - a fixed mulligan count interpreted as final hand size = 7 - mulligan

    Notes:
    - This does not simulate London mulligan decisions (shuffle/redraw/bottoming); it only
      provides turn-by-turn counts conditional on a chosen mulligan count.
    """
    if decksize <= 0:
        raise ValueError("decksize must be a positive integer.")
    if min_lands < 0 or max_lands < 0:
        raise ValueError("min_lands and max_lands must be non-negative.")
    if min_lands > max_lands:
        raise ValueError("min_lands must be <= max_lands.")

    if mulligan > 3 or mulligan < 0:
        raise ValueError("No more than 3 (or less than 0) mulligans allowed.")

    dieroll_norm = dieroll.strip().lower()
    dieroll_options = {"play", "draw"}
    if dieroll_norm not in dieroll_options:
        raise ValueError('dieroll must be "Play" or "Draw".')

    land_counts: Iterable[int]
    if land_count is None:
        land_counts = range(min_lands, max_lands + 1)
    else:
        land_counts = land_count

    starting_hand = 7 - mulligan

    if dieroll_norm == "draw":
        cards_hand_t1 = starting_hand + 1
        cards_seen_t1 = 8
    else:
        cards_hand_t1 = starting_hand
        cards_seen_t1 = 7

    cards_hand_t2 = cards_hand_t1 + 1
    cards_hand_t3 = cards_hand_t2 + 1
    cards_hand_t4 = cards_hand_t3 + 1

    cards_seen_t2 = cards_seen_t1 + 1
    cards_seen_t3 = cards_seen_t2 + 1
    cards_seen_t4 = cards_seen_t3 + 1

    return {
        "decksize": decksize,
        "dieroll": dieroll,
        "land_count": land_counts,
        "cards_hand_t1": cards_hand_t1,
        "cards_hand_t2": cards_hand_t2,
        "cards_hand_t3": cards_hand_t3,
        "cards_hand_t4": cards_hand_t4,
        "cards_seen_t1": cards_seen_t1,
        "cards_seen_t2": cards_seen_t2,
        "cards_seen_t3": cards_seen_t3,
        "cards_seen_t4": cards_seen_t4,
    }
