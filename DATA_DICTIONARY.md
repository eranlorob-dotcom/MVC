# Data dictionary

This dictionary describes every field in the three data files of the MilieuxVie deposit. Coordinates in both GeoJSON files use **WGS84 (EPSG:4326)**, longitude/latitude. The 12 accessibility parameters are abbreviated below as `<param>` and listed in full in Table A.

---

## 1. `mvc_laurentides_2026-06-19.geojson` — municipal results

GeoJSON `FeatureCollection`, 93 features (one per municipal-level territorial unit). Geometry: `Polygon` or `MultiPolygon`.

### Identification and context

| Field | Type | Description |
|---|---|---|
| `MUS_CO_GEO` | string | Québec geographic code of the municipality (*code géographique*). |
| `MUS_NM_MUN` | string | Municipality name. |
| `MUS_NM_MRC` | string | MRC (regional county municipality) name. |
| `superficie_km2` | number | Land area in km² (rounded to 0.1). Used as the denominator for dwelling density. |
| `nb_immeubles` | integer\|null | Number of residential buildings (parcels) from the 2026 assessment roll. `null` where no residential data. |
| `nb_logements` | integer\|null | Number of dwelling units (the origin weight). `null` where no residential data. |
| `source_points` | string | Origin source: `"rôle foncier 2026"` (parcel roll) or `"grille"` (fallback grid). |
| `type_milieu` | string | Milieu class with label: `Dense (≥100 log/km²)`, `Intermédiaire (10–100 log/km²)`, or `Rural (<10 log/km²)`. See classification rule in `METHODS_NOTE.md`. |
| `analyse_le` | string (ISO 8601) | Timestamp of the analysis run. |

### Scores

| Field | Type | Description |
|---|---|---|
| `score_mvc_pct` | integer\|null | **Composite service- and mobility-proximity (SMP) score**, 0–100. Unweighted mean of the 12 `pct_<param>` values. `null` for no-data units. |
| `pct_<param>` | integer | Coverage for a parameter: % of dwelling units within the adaptive radius of at least one matching facility (0–100). One field per parameter (12 total). |
| `nb_<param>` | integer | Number of matching OSM facilities found in range for the parameter. |
| `rayon_<param>_m` | integer | Adaptive radius (metres) applied for the parameter, given the unit’s milieu. |

> **No-data units.** Where `score_mvc_pct` is `null` (e.g., aquatic TNOs, and Kanesatake in this version), the unit is excluded from all scored statistics and shown in grey. Kanesatake is set to no-data because its recorded area is unreliable (≈0 km²), which would otherwise yield an undefined/infinite density.

---

## 2. `lacunes_MVC_tous_perimetres.csv` — urban-perimeter results

CSV, UTF-8, comma-separated, quoted fields. One row per scored *périmètre d’urbanisation* (89 rows + header).

| Column | Type | Description |
|---|---|---|
| `Périmètre` | string | Perimeter identifier `#n`. The integer `n` equals `OBJECTID` in `pu_laurentides.geojson` (join key). |
| `Municipalité` | string | Municipality containing the perimeter. |
| `MRC` | string | MRC name. |
| `Score %` | integer | Composite SMP score of the perimeter (0–100), computed on the origin set restricted to parcels inside the perimeter. |
| `Nb immeubles` | integer | Residential buildings (parcels) inside the perimeter. |
| `Nb logements` | integer | Dwelling units inside the perimeter (origin weight; also used for perimeter-scale density). |
| `<Parameter> %` | integer | Per-parameter coverage inside the perimeter (0–100). One column per parameter; French labels (e.g., `Alimentation %`, `Réseau cyclable %`). |
| `Nb lacunes` | integer | Number of parameters falling below the completeness target for this perimeter. |

> **Perimeter-scale milieu.** Dwelling density per perimeter = `Nb logements ÷ (perimeter area)`, with area computed from `pu_laurentides.geojson` (see file 3). In this version the perimeter milieu is computed at the perimeter scale rather than inherited from the municipality; recomputing locally changes the milieu type of 47 of 89 perimeters (mostly toward a denser class).

---

## 3. `pu_laurentides.geojson` — urban-perimeter geometries

GeoJSON `FeatureCollection`, 93 features. Geometry: `MultiPolygon`. Source: Données Québec / MAMH, *Périmètres d’urbanisation*.

| Field | Type | Description |
|---|---|---|
| `OBJECTID` | integer | Sequential identifier. **Join key:** equals the integer in the CSV `Périmètre` (`#n`). |
| `identifiant` | integer | Source dataset identifier. |
| `theme_province` | string | Source theme label (`"Périmètres d'urbanisation"`). |
| `code_territoire` | string | Territory code from the source dataset (note: not identical to `MUS_CO_GEO`). |
| `shape_Length` | number | Perimeter length **in decimal degrees** (source units; not metric). |
| `shape_Area` | number | Area **in square decimal degrees** (source units; **not km²**). For metric area, project the geometry (e.g., EPSG:32198, Québec Lambert) or compute a geodesic area; this is how perimeter-scale density is derived. |

---

## Table A — the 12 accessibility parameters

| Code (`<param>`) | English label | French label (CSV) | Group |
|---|---|---|---|
| `alimentation` | Food retail | Alimentation | Services |
| `service_garde` | Childcare | Service de garde | Services |
| `ecole_prim` | Primary school | École primaire | Services |
| `ecole_sec` | Secondary school | École secondaire | Services |
| `nature` | Green / natural space | Espaces naturels | Services |
| `loisirs` | Recreation & sport | Loisirs et sport | Services |
| `culture` | Cultural facilities | Équipements culturels | Services |
| `pharmacie` | Pharmacy | Pharmacie | Services |
| `sante` | Primary healthcare | Soins de santé 1re ligne | Services |
| `transport` | Public transit | Transport en commun | Mobility |
| `autopartage` | Shared mobility | Mobilité partagée | Mobility |
| `cyclable` | Cycling network | Réseau cyclable | Mobility |

OSM tag-matching rules and the adaptive radii for each parameter are given in `METHODS_NOTE.md`, Table B.
