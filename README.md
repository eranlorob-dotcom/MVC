# MilieuxVie — Replication data, code and documentation

**An open-source web-mapping tool for assessing complete-neighbourhood (service- and mobility-proximity) accessibility in rural and peri-urban municipalities — Laurentides region (RSS 15), Québec, Canada.**

This archive accompanies the manuscript *“MilieuxVie: An Open-Source Web Mapping Tool for Assessing Complete-Neighbourhood Accessibility in Rural and Peri-Urban Municipalities”* (Geographies, MDPI; manuscript ID geographies-4364677). It provides everything required to reproduce the figures and tables of the paper from a single frozen analysis snapshot.

- **Version:** v2.0.2 (software release archived on Zenodo)
- **Snapshot / analysis date:** 2026-06-19
- **DOI (this version):** [10.5281/zenodo.20775043](https://doi.org/10.5281/zenodo.20775043)
- **Software release (immutable):** `eranlorob-dotcom/MVC`, release tag `2.0.2` (https://github.com/eranlorob-dotcom/MVC/tree/2.0.2)
- **Author:** Éric Robitaille, Ph.D. — Direction de santé publique, Santé Québec Laurentides; Département de médecine sociale et préventive, ESPUM, Université de Montréal — ORCID [0009-0009-4834-7613]
- **Contact:** [eric.robitaille@umontreal.ca]

---

## 1. What this archive contains

| File | Type | Description |
|---|---|---|
| `analyse3.html` | Code | The MilieuxVie tool — a single, self-contained HTML/JavaScript application (Leaflet). The exact release used to produce the deposited results. |
| `mvc_laurentides_2026-06-19.geojson` | Data | Municipal results: one feature per territorial unit (93), with the composite score, the 12 parameter scores, dwelling counts, area, milieu type, and geometry. |
| `lacunes_MVC_tous_perimetres.csv` | Data | Urban-perimeter results: one row per *périmètre d’urbanisation* (89 scored), with composite and per-parameter scores, dwelling counts and the count of below-target gaps. |
| `pu_laurentides.geojson` | Data | Geometries of the 93 urban perimeters (*périmètres d’urbanisation*, source: Données Québec / MAMH). `OBJECTID` joins to the `#n` identifier in the CSV. |
| `overpass_query_regional.txt` | Code | The exact Overpass QL query issued by the tool (verbatim), with the regional bounding box. |
| `osm_extract_2026-06-19.*` | Data | **[TO ADD]** The date-stamped raw OSM response (or the processed POI dataset) returned by the query above. Required for byte-for-byte reproducibility because OSM is queried live. |
| `DATA_DICTIONARY.md` | Doc | Field-by-field description of every data file. |
| `METHODS_NOTE.md` | Doc | Concise methodological note: origins, parameters and adaptive radii, milieu classification, distance computation, the composite, the perimeter analysis, and limitations. |

> **Note on reproducibility.** The tool queries OpenStreetMap live, so a fresh run reflects the current OSM state by design. All tables and figures in the paper derive from the **single 2026-06-19 snapshot** deposited here. To reproduce them exactly, use the deposited OSM extract rather than a live query.

## 2. Study area and units

- **Region:** Laurentides administrative region (RSS 15), Québec, plus a small northern margin in the query bounding box.
- **Territorial units:** 93 municipal-level features (8 MRC). 79 received a score; once Kanesatake is set to *no-data* (unreliable area/coverage), **78 scored units** remain (29 dense, 32 intermediate, 17 rural).
- **Urban perimeters:** 93 *périmètres d’urbanisation*; **89 scored** (three returned no residential parcels and were excluded).

## 3. How to use the tool

`analyse3.html` opens directly in a modern browser from the local filesystem (`file://`) — no web server is required. Internet access **is** required for: the mapping library and basemap tiles (loaded from a CDN) and live Overpass API queries. A previously exported GeoJSON can be re-loaded through the in-app file picker (no server, no CORS configuration).

Two analysis modes are provided: a single-municipality mode (click a unit) and a one-pass regional mode that scores all units and exports the GeoJSON deposited here.

## 4. How to reproduce the published results

1. Open `analyse3.html` in a browser **with the deposited `osm_extract_2026-06-19` loaded** (or accept a live query, understanding results will reflect the current OSM state).
2. Run the regional analysis; export the municipal GeoJSON. It should match `mvc_laurentides_2026-06-19.geojson`.
3. For perimeter results, run the perimeter analysis and export the gap table; it should match `lacunes_MVC_tous_perimetres.csv`.
4. Statistical analyses (Kruskal–Wallis across milieu types, the paired municipal-vs-perimeter Wilcoxon test, the latitude gradient, and the weighting/threshold sensitivity analyses) are described in `METHODS_NOTE.md` and reproduce directly from the two result files.

## 5. Licensing and attribution

- **OpenStreetMap data** © OpenStreetMap contributors, under the **Open Database License (ODbL)**.
- **Municipal boundaries and urban-perimeter geometries** — Gouvernement du Québec (MAMH / MERN), via **Données Québec**, under the applicable open licence; attribution required.
- **Dwelling counts** derive from the 2026 provincial property assessment roll (*rôle d’évaluation foncière*).
- **This documentation** — [https://github.com/eranlorob-dotcom/MVC?tab=GPL-3.0-1-ov-file].

## 6. How to cite

> Robitaille, É. (2026). *MilieuxVie: An Open-Source Web Mapping Tool for Complete-Neighbourhood Accessibility in Rural and Peri-Urban Municipalities (Laurentides, Quebec)* (v2.0.2) [Software]. Zenodo. https://doi.org/10.5281/zenodo.20775043

Please also cite the accompanying article once published.

## 7. Provenance and change log

- **v2.0.2 (2026-06-20):** Public deposit accompanying the revised manuscript; DOI 10.5281/zenodo.20775043. Single frozen 2026-06-19 analysis snapshot. Kanesatake set to *no-data*; urban-perimeter milieu computed at perimeter scale (see `METHODS_NOTE.md`).
