# Regional Population Estimates: Implementation Plan

## Context

The historical overlay annotation system requires population context at varying geographic granularities—from individual cities (already covered by time-series tables with coordinates) to subcontinental regions and historical administrative units. This document outlines two complementary paths for delivering that context, with the recommendation to ship Path B immediately and pursue Path A selectively as the annotation corpus grows.

---

## Path B: Pre-Aggregated Tables (Ship First)

### Objective

Provide country-level and continent-level historical population estimates from 1 AD to present, sourced from the best available scholarly databases, with explicit provenance and confidence metadata. No raster processing required. Target: one afternoon of work, ~3MB in Supabase.

### Data Sources

**Maddison Project Database 2023** — Country-level population from 1 AD onward for 169 countries. The 2023 update (Bolt and van Zanden 2024) is the current standard reference. Available as a single Excel download from the Groningen Growth and Development Centre. Coverage is sparse before 1500 (benchmark years only for most countries) and annual from roughly 1820 onward.

**Federico-Tena World Population Historical Database (2025)** — Annual population series for 174 polities from 1800 to 1938, compiled from first-hand sources and country-specific demographic literature. Available from Universidad Carlos III de Madrid. This is the best available replacement for McEvedy-Jones in the 19th century, with polity-by-polity source documentation in their Appendix I. Crucially, series refer to polities at their contemporary borders (Austria-Hungary as a unit, Ottoman Empire as a unit), not modern borders projected backward.

**HYDE 3.3 Aggregated Tables** — Pre-computed country and continent population totals extending back to 10,000 BCE. These are the tabular summaries that accompany the gridded rasters, available from Utrecht University. They provide the only systematic global coverage for deep history (pre-1 AD).

**Our World in Data / Gapminder** — Curated composites that stitch HYDE (pre-1800), Gapminder/Maddison (1800–1949), and UN World Population Prospects (1950+) into continuous series. Useful as a cross-check and for gap-filling.

### Schema

```sql
create table regional_population (
  id bigint generated always as identity primary key,
  region_name text not null,
  region_type text not null,        -- 'country', 'continent', 'subcontinent', 'polity'
  parent_region text,               -- nullable, for hierarchy traversal
  year integer not null,
  population_estimate bigint,
  estimate_source text not null,    -- 'maddison_2023', 'federico_tena_2025', 'hyde_3.3', 'un_wpp_2024'
  confidence_tier integer not null, -- 1=census, 2=specialist reconstruction, 3=national total, 4=model inference
  notes text,                       -- free-text caveats, e.g. "MJ hard clone from Iran"
  unique(region_name, region_type, year, estimate_source)
);

create index idx_rpop_type_year on regional_population(region_type, year);
create index idx_rpop_name_year on regional_population(region_name, year);
```

### Confidence Tier Definitions

- **Tier 1 — Census/registration data.** Post-1800 Scandinavia, post-1871 British India, post-1950 globally. Direct enumeration with known biases.
- **Tier 2 — Specialist demographic reconstruction.** Pre-1800 England (Wrigley & Schofield), China across dynasties (Deng, Ge Jianxiong), France (Dupâquier), Japan (Hayami). Based on parish registers, fiscal records, or corrected official censuses.
- **Tier 3 — National/continental totals from standard databases.** Maddison, McEvedy-Jones, HYDE aggregates. These are the numbers most global datasets propagate. Known weaknesses per Guinnane (2023): hard cloning, systematic rounding, circular economic reasoning.
- **Tier 4 — Pure model inference.** Pre-contact Americas, pre-colonial sub-Saharan Africa, ancient Central Asia. Order-of-magnitude uncertainty (factors of 2–20 depending on region and period).

### Ingestion Workflow

1. Download Maddison Project Database 2023 Excel file. Extract the population sheet. Normalize country names to a consistent standard (ISO 3166 where applicable, historical names otherwise). Assign `confidence_tier` based on period and region: Tier 1 for post-1950, Tier 2 for countries with known specialist series, Tier 3 otherwise.
2. Download Federico-Tena data from UC3M. These arrive as annual series at contemporary borders. Ingest with `estimate_source = 'federico_tena_2025'` and `region_type = 'polity'`. Cross-reference against Maddison for overlapping years; where they diverge, keep both rows with different `estimate_source` values.
3. Download HYDE 3.3 aggregated tables for continent-level deep history (pre-1 AD). Ingest with `confidence_tier = 4` for anything before 1 CE, `confidence_tier = 3` for 1 CE–1800.
4. For any year/region pair with no direct observation, implement linear interpolation in the application layer between the two nearest bracketing data points. If only one side exists, use nearest value with `notes = 'extrapolated'`.

### What This Gets You

Any annotation in the system can query: "What was the population of [country/continent] in [year]?" and get back one or more estimates with full provenance. Response time: sub-millisecond. Storage: under 5MB. Scholarly defensibility: high, because you're using the actual standard references and being transparent about their limitations.

### What This Doesn't Get You

Sub-country granularity. You cannot answer "What was the population of Provence?" or "How many people lived in the Diocese of Pontus?" without either the raster pipeline (Path A) or a dedicated sub-national dataset for that specific region.

---

## Path A: HYDE Raster Extraction (Build Selectively)

### Objective

For specific historical regions relevant to active annotation work, extract population estimates from HYDE 3.3 gridded rasters using zonal statistics against boundary polygons. Produce rows in the same `regional_population` table with `region_type` values like `'roman_diocese'`, `'chinese_province'`, `'mughal_suba'`, etc. This is a research activity, not a bulk ETL — each new region type requires sourcing or creating defensible boundary polygons.

### Prerequisites

- Python 3.10+ with `rasterio`, `rasterstats`, `geopandas`, `shapely`, `fiona`
- HYDE 3.3 GeoTIFF files downloaded from Utrecht University (total population grids, baseline scenario). Each time slice is 50–150MB; download only the slices relevant to your annotation periods.
- Boundary shapefiles or GeoJSON for each historical region set.

### Boundary Sources by Region

**Modern countries (post-1816):** GADM v4.1 — admin-0 and admin-1 boundaries for all countries. Free download, well-maintained. Use for any modern or near-modern regional breakdown.

**Historical sovereign states (1886–present):** CShapes 2.0 — time-varying country boundaries. Covers the colonial and post-colonial era. Useful for "what did the borders of the Ottoman Empire look like in 1900?"

**Roman Empire administrative units:** Digital Atlas of Roman and Medieval Civilizations (DARMC), Harvard. Provides GIS layers for Roman provinces and dioceses. Quality is good for the 2nd–4th century CE reorganizations.

**Chinese historical administrative units:** China Historical GIS (CHGIS), Harvard/Fudan. Province and prefecture boundaries across major dynastic periods. The most comprehensive historical boundary dataset for any single civilization.

**Islamic caliphate/Ottoman provinces:** Limited systematic GIS coverage. The Islamic Civilization Spatial Data project and individual scholarly publications provide partial coverage. Expect to hand-draw many boundaries from historical atlas plates (e.g., Kennedy's *Historical Atlas of Islam*).

**Everything else:** Hand-drawn GeoJSON from historical atlas consultation. This is where the original scholarly contribution lives — synthesizing textual boundary descriptions, archaeological evidence, and atlas reproductions into defensible polygons.

### Extraction Script Architecture

```
hyde_extract/
├── boundaries/
│   ├── roman_dioceses.geojson
│   ├── chinese_provinces_han.geojson
│   ├── chinese_provinces_tang.geojson
│   └── ...
├── rasters/
│   ├── popc_0200AD.tif
│   ├── popc_0400AD.tif
│   └── ...
├── extract.py
├── config.yaml          # maps boundary files to relevant time slices
└── output/
    └── regional_population.csv
```

The core extraction loop in `extract.py`:

```python
for boundary_file, time_slices in config.items():
    regions = geopandas.read_file(boundary_file)
    for tif_path in time_slices:
        year = parse_year(tif_path)
        stats = rasterstats.zonal_stats(
            regions, tif_path,
            stats=['sum'], geojson_out=True
        )
        for feature in stats:
            emit_row(
                region_name=feature['properties']['name'],
                region_type=feature['properties']['type'],
                year=year,
                population_estimate=feature['properties']['sum'],
                estimate_source=f'hyde_3.3_zonal_{boundary_file}',
                confidence_tier=determine_tier(year, region_type)
            )
```

### Sensitivity Analysis

For each boundary polygon, also run zonal stats against a buffered version (e.g., 25km outward expansion) and record the delta. Store this as a `sensitivity_pct` column or in `notes`. This quantifies how much the estimate depends on exact boundary placement — critical for regions where the border is uncertain.

For regions where HYDE provides upper and lower scenario rasters in addition to the baseline, run extraction against all three and store each with a distinct `estimate_source` suffix (`hyde_3.3_baseline`, `hyde_3.3_upper`, `hyde_3.3_lower`).

### Cross-Referencing Protocol

For any region where independent demographic scholarship exists, add a separate row with the specialist estimate and `estimate_source` pointing to the publication. The application layer can then display: "HYDE estimates 2.3M for this region in 200 CE; Frier (2000) estimates 1.8M based on epigraphic evidence." Divergences are findings, not errors.

Key cross-references to prioritize:

- **Roman provinces:** Frier, Scheidel, and Lo Cascio for demographic estimates; compare against HYDE zonal output.
- **Chinese provinces:** Deng's census-based reconstructions and Ge Jianxiong's *Zhongguo Renkou Shi*.
- **England:** Broadberry et al. for medieval estimates; Wrigley & Schofield for early modern.
- **Africa:** Frankema and Jerven (2014) for 1850–1960 revisions.

### Sequencing

Do not attempt a comprehensive cross-civilizational extraction upfront. Instead, extract boundaries and population estimates only for regions you are actively annotating:

1. **First batch:** Roman dioceses (DARMC boundaries exist, HYDE has relevant time slices, Scheidel provides cross-reference estimates). This is the proof-of-concept.
2. **Second batch:** Chinese provinces across Han/Tang/Song/Ming/Qing (CHGIS boundaries are excellent, Deng and Ge provide cross-references).
3. **Third batch:** Whatever the narrative history project demands next — Mughal India, Ottoman provinces, Carolingian counties.

Each batch is a self-contained research task: source boundaries, run extraction, cross-reference, write up caveats, load into Supabase. Budget 1–3 days per batch depending on boundary availability.

---

## Summary

| Dimension | Path B (Pre-Aggregated) | Path A (Raster Extraction) |
|---|---|---|
| Granularity | Country / continent | Historical administrative unit |
| Time to ship | One afternoon | 1–3 days per region batch |
| Storage | ~3MB | +50–200KB per batch |
| Scholarly originality | None (standard references) | Moderate to high (novel boundary polygons) |
| HYDE dependency | Indirect (via Maddison/aggregates) | Direct (gridded rasters) |
| Risk of false precision | Low | Moderate (mitigated by sensitivity analysis) |

**Ship Path B now. Pursue Path A per-region as the annotation corpus demands it.**
