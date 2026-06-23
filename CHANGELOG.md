# Changelog

## [unreleased — to be tagged] (2026-06)

### Tool (milieuxvie.html)
- Added an on-map **metric scale bar** and a **score-class legend** so map
  panels are publication-ready (addresses reviewer comment on missing scale
  bars and legends).
- Added a **high-resolution PNG/JPG map export** (2×/3×/4×) producing ≥ 300 dpi
  figures at print size, for both the municipal and urban-perimeter views.
- **Kanesatake** Mohawk Territory is now shown as a **no-data (grey)** unit;
  municipalities with a small residential urban-affectation area (e.g. Gore,
  Mille-Isles) are scored correctly rather than being skipped.
- Removed the in-app benchmarking panel.

### Data & methods
- Dwelling-unit density (milieu classification) is computed from the residential
  **urban-affectation area** (`superficie_km2`), consistent across the tool, the
  archived dataset and the manuscript (dense 29 / intermediate 32 / rural 17).

### Validation & reproducibility
- Added a straight-line vs pedestrian-network distance validation app and result
  file (Supplementary Table S4).
- Added an OpenStreetMap completeness validation app and result files
  (Supplementary Table S5).
- Added the statistics reproduction script (`milieuxviestats.py`) and the
  runtime benchmark data (Supplementary Table S3).
