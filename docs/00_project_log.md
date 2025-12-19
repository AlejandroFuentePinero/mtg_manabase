# Chapter 0 
## 2025-12-19 — Chapter 0 / Notebook 00 - Foundation: baseline hypergeometric land-drop model

Completed the baseline (no mulligans, no selection) land-drop model for a 60-card deck using a hypergeometric formulation. Implemented utilities to compute P(X ≥ k) for lands seen by a given turn and generated a tidy results table sweeping realistic land counts for both play and draw. Produced a baseline plot showing P(≥2 lands by T2) and P(≥3 lands by T3) with an 80% reference line to support quick threshold readouts. This baseline now serves as the reference curve for future notebooks that add London mulligans, cantrips, fetch/surveil effects, tapland constraints, and player behaviour.

Implemented the foundational bookkeeping for early turns (T1–T3) on the play vs on the draw, and a baseline hypergeometric probability function for land outcomes in a 60-card deck. Built the first baseline dataset by sweeping realistic land counts and calculating core metrics (P(≥2 lands by T2), P(≥3 lands by T3)), plus visualised the curves with an 80% reference threshold. This establishes the reference point for all later additions (London mulligan behaviour, cantrips, fetch/surveil effects, tapland constraints, and player-profile preferences).

