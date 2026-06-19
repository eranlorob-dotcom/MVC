# Methodological note

This note documents how MilieuxVie computes the service- and mobility-proximity (SMP) scores deposited in this archive. It is written to be read alongside the manuscript (Geographies, MDPI) and the data dictionary.

## 1. Origins (who is being measured from)

Accessibility is measured **from residents, not from territory**. Origins are residential parcels from the 2026 Québec property assessment roll (*rôle d’évaluation foncière*), each weighted by its number of dwelling units. A parameter’s coverage is therefore the share of **dwelling units** — not the share of land — within reach of a service. Where parcel data are unavailable, a fallback grid is used and flagged (`source_points = "grille"`). Because origins are dwelling-weighted parcels, uninhabited land is absent from both numerator and denominator and cannot dilute a score.

## 2. Milieu classification (which standard applies)

Each unit is classified by dwelling density (dwelling units ÷ area, in dwellings/km²):

- **Rural:** density < 10
- **Intermediate:** 10 ≤ density < 100
- **Dense:** density ≥ 100

The classification selects the distance radius applied to each parameter (Table B). For municipalities the denominator is municipal land area; **for urban perimeters the density is computed at the perimeter scale** (dwellings inside the perimeter ÷ perimeter area), so a compact built-up area inside a large rural municipality is not given inappropriately generous rural radii. (Recomputing perimeter density locally rather than inheriting the municipal class changes the milieu type of 47 of 89 perimeters, almost all toward a denser class.)

Units with unreliable inputs are set to **no-data** rather than scored — including any unit whose recorded area is implausibly small (< 1 km²), which would otherwise produce an undefined or infinite density (this is why Kanesatake is no-data in this version).

## 3. Parameters, OSM matching, and adaptive radii

Twelve parameters are scored, grouped into **services (D)** and **mobility (M)**. For each parameter, a facility is counted if its OSM tags match the rule below; the distance threshold depends on the unit’s milieu.

### Table B — OSM matching rules and adaptive radii (metres)

| Parameter | Group | OSM match (tag values) | Dense | Inter. | Rural |
|---|---|---|---:|---:|---:|
| Food retail | D | `shop` = supermarket, convenience, grocery, butcher, bakery, greengrocer, deli, food, general | 800 | 1500 | 3000 |
| Childcare | D | `amenity` = kindergarten, childcare | 400 | 800 | 1500 |
| Primary school | D | `amenity` = school (name not “secondaire/polyvalente”) | 800 | 1500 | 3000 |
| Secondary school | D | `amenity` = school (name “secondaire/polyvalente/cégep”) or `amenity` = college/university | 1600 | 3000 | 5000 |
| Green / natural | D | `leisure` = park, garden, nature_reserve **or** `landuse` = forest, grass, meadow | 400 | 800 | 1500 |
| Recreation & sport | D | `leisure` = sports_centre, fitness_centre, swimming_pool, stadium, pitch, recreation_ground, ice_rink | 800 | 1500 | 3000 |
| Cultural | D | `amenity` = theatre, cinema, library, community_centre, arts_centre, social_centre | 800 | 1500 | 3000 |
| Pharmacy | D | `amenity` = pharmacy | 400 | 800 | 2000 |
| Primary healthcare | D | `amenity` = clinic, hospital, doctors, health_centre, dentist | 800 | 1500 | 5000 |
| Public transit | M | `highway` = bus_stop **or** `amenity` = bus_station, ferry_terminal **or** `railway` = station, halt, tram_stop | 800 | 1500 | 3000 |
| Shared mobility | M | `amenity` = car_sharing, bicycle_rental | 800 | 1500 | 3000 |
| Cycling network | M | `highway` = cycleway **or** `bicycle` = designated/yes **or** any `cycleway*` tag present | 400 | 800 | 1500 |

The exact, verbatim Overpass query (regional bounding box `45.3964,-76.1985,47.8133,-73.6802`, S/W/N/E) is in `overpass_query_regional.txt`. Per-perimeter analyses reissue the same tag set restricted to each polygon.

> **Calibration — honest statement.** The dense/intermediate/rural radii are anchored primarily in the rural-accessibility literature and were refined through **informal, unstructured discussions** with regional planners, not a structured elicitation. Their justification is empirical robustness (Section 6 of the manuscript), not a formal calibration exercise.

## 4. Distance computation

Distances use the **Haversine** great-circle formula (Earth radius R = 6 371 000 m). Point facilities (OSM nodes) are measured to their coordinate. For **ways and polygons** (e.g., parks, forests, cycleways), the Overpass query returns one representative point — the geometry’s **bounding-box centre** (`out center`) — and distance is measured to that point.

> **Limitation (consequence).** For spatially extensive features (large parks/forests) and long linear features (cycleways), distance to the bounding-box centre **overestimates** the true nearest-edge distance. Green-space and cycling-network coverage are therefore **conservative (biased low)**, not inflated. A future version will use full geometries (`out geom`) with nearest-point computation.

## 5. Coverage and the composite score

For each parameter, a dwelling unit is **covered** if the nearest matching facility lies within the adaptive radius. Parameter coverage is the dwelling-weighted share of covered dwellings:

```
pct_<param> = 100 × (dwelling units with a matching facility within radius) / (total dwelling units)
```

The **composite SMP score** is the **unweighted mean of the 12 parameter coverages**. The composite is intentionally compensatory; the actionable information is the parameter-level gap profile (which categories fall below the completeness target). A non-compensatory reading is supported by the per-parameter coverages and the gap count (`Nb lacunes`).

> **Interpretation.** The score measures **context-relative service proximity**, not absolute pedestrian accessibility: a 3–5 km rural radius is not a walking standard. Scores are not directly comparable as an absolute standard across milieu types. Proximity is also necessary but not sufficient for realised access — it captures neither service capacity, quality, affordability, nor operating hours.

## 6. Urban-perimeter analysis

Perimeter scores restrict the **origin set** to parcels inside the *périmètre d’urbanisation*; eligible destinations are unchanged (the calculation is parcel-centric, not perimeter-centric — a service outside the perimeter still counts for an inside parcel within range, and vice-versa). Because the origin set differs from the municipal one, municipal and perimeter scores are **not directly comparable** (a Modifiable Areal Unit Problem); higher perimeter scores partly reflect origin-set restriction rather than genuinely better access. The municipal-vs-perimeter difference is assessed with a **paired** test (Wilcoxon signed-rank on municipalities that have a perimeter), not unmatched medians.

## 7. Statistics reported in the paper (reproducible from the deposited files)

- **Across milieu types:** Kruskal–Wallis on the composite (H = 10.29, df = 2, p = 0.006, ε² = 0.11); dense > intermediate > rural. The differences are statistically significant — the adaptive tiers narrow but do not close the rural–urban gap.
- **Municipal vs perimeter:** Wilcoxon signed-rank, 53 paired municipalities (V = 101, p < 0.001, r = 0.72; perimeter higher in 48/53).
- **North–south gradient:** Spearman of composite vs centroid latitude (ρ = −0.36, p = 0.001, n = 78).
- **Sensitivity:** essential-service re-weighting vs equal weights (Spearman ρ = 0.99; 1/78 band change); ±20% milieu density cut-offs reclassify 5/78 units; no unit reaches the completeness target at 60/70/80%.

## 8. Known limitations (summary)

1. OSM completeness varies; low scores in sparsely mapped areas may partly reflect under-mapping. A building-footprint-density proxy flags such areas, and a stratified validation against official inventories is reported in the manuscript.
2. Distance to areal/linear features uses the bounding-box centre (Section 4) — conservative for green space and cycling.
3. Live OSM queries are not reproducible without the deposited extract (Section 1 of the README).
4. The composite is compensatory; read it with the parameter-level gap profile.
5. Proximity ≠ realised access (capacity, quality, affordability, hours not captured).
6. Seasonal/secondary dwellings are not separated from year-round dwellings in the origin weights.
