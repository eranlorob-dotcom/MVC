# MilieuxVie — open-source web mapping tool (Laurentides, Québec)

Companion software, data and analysis code for the manuscript *“MilieuxVie: An
Open-Source Web Mapping Tool for Assessing Complete Neighbourhood Accessibility
in Rural and Peri-Urban Municipalities”* (Geographies, MDPI; manuscript
geographies-4364677).

## Contents

| File | Description |
|------|-------------|
| `milieuxvie.html` | The tool. Single self-contained HTML file; open in any modern browser. Internet is required for the mapping library, basemap tiles (CDN) and live OpenStreetMap (Overpass) queries. Includes an on-map scale bar and score-class legend, and a high-resolution PNG/JPG map export. |
| `mvc_laurentides_2026-06-23.geojson` | Municipal results dataset (93 territorial units) underlying the manuscript. One attribute per parameter plus the composite SMP score and milieu classification. |
| `mvc_laurentides_tableau_2026-06-23.json` | Same municipal results in a flat tabular JSON (one record per territorial unit), convenient for spreadsheets. |
| `lacunes_MVC_tous_perimetres__2_.csv` | Urban-perimeter (PU) results (per-perimeter scores and per-parameter coverage). |
| `pu_laurentides.geojson` | Urban-perimeter geometries. |
| `milieuxviestats.py` | Reproduces the statistics reported in the paper: milieu distribution and Table 3, weighting and threshold sensitivity, Kruskal–Wallis across milieu types, north–south gradient, municipal vs perimeter Wilcoxon, and the per-parameter Table 5. |
| `validation_reseau_haversine_osrm.html` / `validation_reseau_synthese.json` | Straight-line vs pedestrian-network distance validation (Supplementary Table S4). |
| `validation_completude_osm.html` / `validation_completude_synthese.json` / `validation_completude_osm.csv` | OpenStreetMap completeness validation against the CUBF non-residential reference inventory (Supplementary Table S5). |
| `milieuxvie_benchmark.csv` | Runtime benchmark, regional analysis (Supplementary Table S3). |

## Reproduce the statistics

```
python3 milieuxviestats.py
```

Requires Python 3 with `numpy`, `pandas`, `scipy` and `shapely`. All data files
must be in the same directory as the script. Running it reproduces the
manuscript figures, including:

- Milieu distribution: dense 29 / intermediate 32 / rural 17 (n = 78).
- Composite SMP score: median 15 %, mean 20.2 % (SD 16.5).
- Kruskal–Wallis across milieu types: H = 10.29, df = 2, p = 0.006, ε² = 0.11.
- North–south gradient: Spearman ρ = −0.36, p = 0.001 (n = 78).

## Methodological notes

- Three adaptive radius tiers (dense / intermediate / rural) are assigned from
  residential dwelling-unit density, computed as dwelling units divided by the
  area of the municipality’s residential urban-affectation zone
  (field `superficie_km2`). This is a proxy for settlement intensity and avoids
  the dilution caused by large uninhabited territories common in the region.
- Service locations are drawn from OpenStreetMap via the Overpass API.
  Re-running the tool on live data may yield slightly different service counts
  than the archived dataset, because OSM evolves over time. The archived
  GeoJSON/CSV are the exact data underlying the published results.
- Kanesatake Mohawk Territory is treated as a no-data unit (unreliable recorded
  area) and is excluded from the scored statistics.

## License / citation

See `CITATION.cff`. Please cite the manuscript and this archived release.
