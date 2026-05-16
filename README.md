# Milieux de vie complets (MVC) – Outil cartographique interactif

[![DOI](https://zenodo.org/badge/1240166025.svg)](https://doi.org/10.5281/zenodo.20218005).
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Outil cartographique interactif pour l'analyse des **milieux de vie complets** à l'échelle des 93 municipalités de la région des Laurentides (Québec, Canada).

## Contexte

Le concept de *milieu de vie complet* désigne un environnement bâti où les résidents peuvent accéder, à distance de marche ou à proximité raisonnable, aux services, commerces, équipements et espaces publics nécessaires à leur vie quotidienne. Ce concept s'inscrit dans les nouvelles **orientations gouvernementales en aménagement du territoire** (OGAT) du Québec et dans les travaux de la Direction de santé publique du CISSS des Laurentides sur les liens entre environnement bâti et santé des populations.

Cet outil vise à soutenir le **transfert de connaissances** vers les élus municipaux, les urbanistes et les professionnels de santé publique de la région des Laurentides en rendant accessibles et visuelles des données complexes sur l'aménagement du territoire.

## Fonctionnalités

- Cartographie interactive (Leaflet) des scores d'accessibilité aux services de proximité
- Analyse pondérée multi-indicateurs à l'échelle municipale
- Typologie du parc résidentiel à partir du rôle d'évaluation foncière MAMH 2026
- Indicateurs de logement abordable
- Interface responsive adaptée aux présentations et consultations sur le terrain

## Démonstration

🔗 **[Accéder à l'outil en ligne](https://eranlorob-dotcom.github.io/MVC/analyse3.html)**

## Technologies

- [Leaflet](https://leafletjs.com/) – cartographie interactive
- HTML / CSS / JavaScript
- Données ouvertes du rôle d'évaluation foncière (MAMH)
- Données de Statistique Canada (recensement)

## Installation locale

Aucune installation requise. L'outil fonctionne entièrement côté client (navigateur web).

Pour une copie locale :

```bash
git clone https://github.com/eranlorob-dotcom/MVC.git
cd MVC
# Ouvrir analyse3.html dans un navigateur
```

> **Note :** Certaines fonctionnalités nécessitent un serveur HTTP local en raison des politiques CORS. Vous pouvez utiliser `python -m http.server 8000` puis accéder à `http://localhost:8000/analyse3.html`.

## Citation

Si vous utilisez cet outil dans vos travaux, merci de le citer :

```
Robitaille, É. (2026). Milieux de vie complets – Outil cartographique interactif
pour l'analyse des territoires des Laurentides (version 1.0.0).
[https://doi.org/10.5281/zenodo.20218005]
```

Un fichier [`CITATION.cff`](CITATION.cff) est également fourni pour une intégration automatique dans les gestionnaires de références.

## Auteur

**Éric Robitaille, Ph.D.**
- Professeur, [École de santé publique de l'Université de Montréal](https://espum.umontreal.ca/) (ESPUM) – Département de médecine sociale et préventive
- Chercheur, Direction de santé publique, [CISSS des Laurentides](https://www.cisss-laurentides.gouv.qc.ca/)
- ORCID : [0009-0009-4834-7613](https://orcid.org/0009-0009-4834-7613)

## Projet C.A.R.T.O.S.

Cet outil s'inscrit dans le cadre du projet **C.A.R.T.O.S.** (*Cartographie et Analyse en Réseau pour la Transformation et l'Optimisation en Santé*), un programme de recherche visant le développement d'outils géoweb pour l'évaluation d'impact sur la santé (EIS) et le soutien à la planification territoriale au Québec.

## Licence

Ce projet est distribué sous licence [GNU General Public License v3.0](LICENSE).

Vous êtes libre de l'utiliser, le modifier et le redistribuer, à condition que les travaux dérivés soient distribués sous la même licence.
