"""News- and sentiment-aware layer.

Two honestly-scoped parts, both measurable via the backtester:
  1. an economic-calendar risk filter (don't trade into high-impact releases), and
  2. an experimental sentiment overlay (Claude scores fresh headlines; by default it
     only vetoes technical trades that fight strong fresh sentiment).

News moves FX, but predicting direction from public headlines is not a reliable retail
edge. This layer is built to manage risk and be measured — not as a profit oracle.
"""
