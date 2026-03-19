# Geographic Reading Assistant — Architecture Plan

## Context

A web app for assisted reading of texts with heavy geographic content (history, current affairs). Users upload a PDF, image, or paste text. The system extracts location and year mentions, then displays contextual geographic/demographic annotations in a sidebar — city population at the mentioned time, country and continent population, and travel distances/times between co-mentioned locations.

**Tech stack**: React frontend, Rails API backend, Supabase PostgreSQL (free tier, 500MB). No authentication (demo/MVP).

**Existing assets**:
- CIESIN historical urban population dataset (10,352 records, 3700 BC–2000 AD) at `Datasets/urbanspatial-hist-urban-pop-3700bc-ad2000-xlsx.xlsx`
- Historical travel speeds reference at `historical_travel_speeds.md`

---

## 1. Wireframe: Dual-Panel with Map Strip

User chose dual-panel (text + annotation sidebar). Map placed as a collapsible strip above or below the main panels showing location markers + distance lines.

```
+=========================================================================+
|  GeoReader                                       [Upload] [Paste Text]  |
+=========================================================================+
|  +--Upload Zone (collapses after use)--------------------------------+  |
|  |  [Drop PDF/Image here]   or   [Paste text...]         [Process]  |  |
|  +-------------------------------------------------------------------+  |
|                                                                         |
|  +--MAP STRIP (collapsible, full width)------------------------------+  |
|  |     * Paris -------- 292 mi -------- * Lyon                       |  |
|  |                  [Leaflet.js map]                                  |  |
|  +-------------------------------------------------------------------+  |
|                                                                         |
|  +--TEXT PANEL (2/3 width)-----+  +--ANNOTATION RAIL (1/3)----------+  |
|  |                             |  |                                  |  |
|  |  In the summer of [1832],   |  |  +-- PARIS, 1832 -----------+   |  |
|  |  [Paris] was a city of   ------->|  City pop: ~774,000        |   |  |
|  |  barricades. The June       |  |  |  (nearest: 785K in 1846)  |   |  |
|  |  Rebellion drew thousands   |  |  |  France: ~32.5M           |   |  |
|  |  into the narrow streets... |  |  |  Europe: ~276M            |   |  |
|  |                             |  |  +---------------------------+   |  |
|  |                             |  |                                  |  |
|  |  Meanwhile in [Lyon],       |  |  +-- LYON, 1832 -------------+  |  |
|  |  the silk workers had    ------->|  City pop: ~150,000         |  |  |
|  |  already revolted the year  |  |  |  France: ~32.5M            |  |  |
|  |  before...                  |  |  +---------------------------+  |  |
|  |                             |  |                                  |  |
|  |                             |  |  +-- PARIS <-> LYON ---------+  |  |
|  |                             |  |  |  Distance: ~292 mi        |  |  |
|  |                             |  |  |  On foot: 16-22 days      |  |  |
|  |                             |  |  |  Horseback: 5-8 days      |  |  |
|  |                             |  |  +---------------------------+  |  |
|  +-----------------------------+  +----------------------------------+  |
|                                                                         |
|  [Page 1 of 12]  [<] [>]                                [Toggle Map]   |
+=========================================================================+
```

On narrow screens, the annotation rail stacks below the text panel, and the map collapses to a toggle button.

---

## 2. System Architecture

```
+-------------------+        +-------------------+        +-------------------+
|   REACT SPA       |  REST  |   RAILS API       |  SQL   |   SUPABASE PG     |
|                   |  API   |                   |        |                   |
| UploadComponent  ----------> DocumentsCtrl   ----------> documents         |
| TextViewer       <---------- AnnotationsCtrl <--------- entities           |
| AnnotationRail   <---------- PopulationCtrl  <--------- annotations       |
| MapStrip          |        | TravelCtrl       |        | urban_populations |
|  (Leaflet.js)     |        |                   |        | country_populations|
|                   |        | EntityExtractor   |        | continent_pops    |
|                   |        |  (regex + DB      |        | PostGIS enabled   |
|                   |        |   matching)       |        |                   |
|                   |        | TextExtraction    |        | Supabase Storage  |
|                   |        |  (pdf-reader,     |        |  (PDF/images)     |
|                   |        |   RTesseract)     |        |                   |
+-------------------+        +-------------------+        +-------------------+

PROCESSING PIPELINE (async via ActiveJob + GoodJob):

  Upload file/text
      |
      v
  Extract raw text (pdf-reader / RTesseract / passthrough)
      |
      v
  Split into pages/sections
      |
      v
  Regex extraction: find capitalized words + 4-digit years
      |
      v
  Match candidates against urban_populations + country tables
      |
      v
  Population lookup + linear interpolation (city, country, continent)
      |
      v
  Travel calculation for location pairs (Haversine + speed tables)
      |
      v
  Store annotations -> serve to frontend
```

---

## 3. Entity Extraction: Regex + DB Matching (No AI/NLP)

Simple programmatic approach for the MVP — no OpenAI, no spaCy.

### Step 1: Year extraction
```ruby
# Regex for 3-4 digit years, with boundary checks to skip page numbers
text.scan(/\b(\d{3,4})\b/).flatten.map(&:to_i).select { |y| y >= 100 && y <= 2100 }
```
Also handle "BC"/"BCE" suffixes: `\b(\d{1,4})\s*(BC|BCE|AD|CE)\b`

### Step 2: Location candidate extraction
Extract capitalized multi-word sequences (potential place names):
```ruby
# Matches "Paris", "New York", "United Kingdom", etc.
text.scan(/\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b/)
```
Filter out common non-location capitalized words (sentence starters, names) by checking against the DB.

### Step 3: DB matching
For each candidate, query `urban_populations`:
```sql
SELECT DISTINCT city, country, city_id, latitude, longitude
FROM urban_populations
WHERE LOWER(city) = LOWER($1)
   OR other_name ILIKE '%' || $1 || '%';
```
Also check `country_populations` for country name matches. If no match, the candidate is discarded (not a known location).

### Step 4: Year-location association
Simple proximity heuristic: associate each location with the nearest year mention on the same page (within N characters). If no year on the page, use the most recent year from a previous page.

### Future upgrade path
This regex approach can be swapped for OpenAI GPT-4o-mini structured output later for better accuracy with ambiguous names, coreference ("the city"), and relative dates ("the previous year").

---

## 4. Database Schema (Supabase PostgreSQL)

### Extensions
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- fuzzy text matching
```

### Core Data Tables

**`urban_populations`** — seed from CIESIN XLSX (10,352 rows, ~3MB)

| Column     | Type                    | Notes                          |
|------------|-------------------------|--------------------------------|
| id         | BIGSERIAL PK            |                                |
| city       | TEXT NOT NULL            |                                |
| other_name | TEXT                    | alternate names                |
| country    | TEXT NOT NULL            |                                |
| location   | GEOGRAPHY(POINT, 4326)  | PostGIS point from lat/lon     |
| latitude   | DOUBLE PRECISION        |                                |
| longitude  | DOUBLE PRECISION        |                                |
| certainty  | SMALLINT (1-3)          | 1=most accurate                |
| year       | INTEGER                 | negative = BC                  |
| population | BIGINT                  |                                |
| city_id    | TEXT                    | unique city identifier         |

Indexes: trigram on city, GIST on location, composite (city_id, year).

**`country_populations`** — from Maddison Project Database (~5,000 rows, ~200KB)

| Column       | Type         | Notes                    |
|--------------|-------------|--------------------------|
| id           | BIGSERIAL PK |                          |
| country_name | TEXT         |                          |
| country_code | CHAR(3)      | ISO 3166-1 alpha-3       |
| year         | INTEGER      |                          |
| population   | BIGINT       |                          |
| source       | TEXT         | e.g. 'Maddison', 'HYDE' |

**`continent_populations`** — from HYDE aggregates (~500 rows)

| Column    | Type         |
|-----------|-------------|
| id        | BIGSERIAL PK |
| continent | TEXT         |
| year      | INTEGER      |
| population| BIGINT       |

**`country_continent_map`** — lookup (~200 rows)

| Column       | Type     |
|--------------|----------|
| country_name | TEXT PK  |
| continent    | TEXT     |

**`travel_speed_references`** — from historical_travel_speeds.md (~15 rows)

| Column         | Type   | Notes                          |
|----------------|--------|--------------------------------|
| mode           | TEXT   | 'foot', 'horse', 'cart'        |
| condition      | TEXT   | 'normal', 'forced_march', etc. |
| km_per_day_low | REAL   |                                |
| km_per_day_mid | REAL   |                                |
| km_per_day_high| REAL   |                                |

### Document/Annotation Tables

**`documents`**

| Column       | Type         | Notes                          |
|--------------|-------------|--------------------------------|
| id           | UUID PK      | gen_random_uuid()              |
| title        | TEXT          |                                |
| source_type  | TEXT          | 'pdf', 'image', 'text'        |
| storage_path | TEXT          | Supabase Storage path          |
| raw_text     | TEXT          |                                |
| status       | TEXT          | pending/processing/ready/error |
| page_count   | INTEGER       |                                |

**`doc_pages`**

| Column      | Type      |
|-------------|-----------|
| id          | BIGSERIAL |
| document_id | UUID FK   |
| page_number | INTEGER   |
| page_text   | TEXT      |

**`entities`** — extracted location/date mentions

| Column            | Type     | Notes                        |
|-------------------|----------|------------------------------|
| id                | BIGSERIAL|                              |
| document_id       | UUID FK  |                              |
| page_number       | INTEGER  |                              |
| entity_type       | TEXT     | 'location' or 'date'         |
| raw_text          | TEXT     | exact text span              |
| char_offset_start | INTEGER  | position in page_text        |
| char_offset_end   | INTEGER  |                              |
| resolved_city_id  | TEXT     | matched city_id              |
| resolved_year     | INTEGER  |                              |
| resolved_country  | TEXT     |                              |
| resolved_lat      | DOUBLE   |                              |
| resolved_lon      | DOUBLE   |                              |

**`annotations`** — computed population + travel results

| Column                | Type     | Notes                           |
|-----------------------|----------|---------------------------------|
| id                    | BIGSERIAL|                                |
| document_id           | UUID FK  |                                |
| page_number           | INTEGER  |                                |
| annotation_type       | TEXT     | 'population' or 'travel'       |
| entity_id             | BIGINT FK| for population annotations     |
| entity_a_id           | BIGINT FK| for travel annotations         |
| entity_b_id           | BIGINT FK| for travel annotations         |
| city_name             | TEXT     |                                |
| year_queried          | INTEGER  |                                |
| city_population       | BIGINT   |                                |
| city_pop_interpolated | BOOLEAN  |                                |
| country_name          | TEXT     |                                |
| country_population    | BIGINT   |                                |
| continent_name        | TEXT     |                                |
| continent_population  | BIGINT   |                                |
| distance_miles        | DOUBLE   | travel type only               |
| distance_adjusted     | DOUBLE   | after terrain multiplier       |
| terrain_multiplier    | REAL     | default 1.2                    |
| foot_days_low         | REAL     |                                |
| foot_days_high        | REAL     |                                |
| horse_days_low        | REAL     |                                |
| horse_days_high       | REAL     |                                |

### Storage Budget (~120MB of 500MB free tier) — comfortable

---

## 5. Regional Population: Pre-Aggregated Tables (Not Raster)

**The raster approach (HYDE 3.2 GeoTIFF) is impractical:**
- A single HYDE time slice is 50-150 MB; 20+ slices = 1-3 GB (exceeds 500MB Supabase limit)
- Requires GDAL native libraries and Python interop
- Each query takes seconds of CPU

**Use pre-aggregated tables instead:**
- **Maddison Project Database 2023** — country-level population from 1 AD onward for 170+ countries (~2MB)
- **HYDE 3.2 aggregated tables** — pre-computed country/continent totals for pre-1 AD coverage
- **Our World in Data / Gapminder** — curated long-run datasets combining Maddison + UN + HYDE

Total: ~3 MB in the database. Millisecond lookups. Same accuracy for country/continent aggregation.

**Population interpolation**: Linear interpolation between the two nearest bracketing data points. If only one side exists, use nearest with an "extrapolated" flag.

---

## 6. API Endpoints (Rails)

```
POST   /api/v1/documents                             — upload file or submit text
GET    /api/v1/documents                             — list documents
GET    /api/v1/documents/:id                         — metadata + status
GET    /api/v1/documents/:id/status                  — processing progress
DELETE /api/v1/documents/:id                         — remove + cascade

GET    /api/v1/documents/:id/pages                   — all pages
GET    /api/v1/documents/:id/pages/:page_number      — single page
GET    /api/v1/documents/:id/entities?page=N         — extracted entities
GET    /api/v1/documents/:id/annotations?page=N      — annotations for page

GET    /api/v1/populations/city?city=Paris&year=1832 — ad-hoc city lookup
GET    /api/v1/populations/search?q=Par&limit=10     — fuzzy city search
GET    /api/v1/travel/calculate?from_city_id=X&to_city_id=Y — distance + travel time
```

### Rails Service Objects

```
app/services/
  text_extraction/
    pdf_extractor.rb          — pdf-reader gem
    image_extractor.rb        — RTesseract gem
    text_paginator.rb         — split into pages
  entity_extraction/
    regex_extractor.rb        — find capitalized words + year patterns
    db_matcher.rb             — match candidates against urban_populations
    year_associator.rb        — proximity-based year-location pairing
  population/
    city_lookup.rb            — query + linear interpolation
    country_lookup.rb
    continent_lookup.rb
  travel/
    distance_calculator.rb    — Haversine + terrain multiplier (port from historical_travel_speeds.md lines 13-21)
    travel_time_estimator.rb  — speed tables (from lines 47-53, 84-92)
  annotation/
    annotation_builder.rb     — orchestrates full pipeline
```

---

## 7. Key Gems and Libraries

**Rails backend:**
- `pg` + `activerecord-postgis-adapter` — Supabase + PostGIS
- `pdf-reader` — PDF text extraction
- `rtesseract` — OCR for images
- `good_job` — ActiveJob adapter (Postgres-backed, no Redis)
- `rack-cors` — CORS for React SPA
- `roo` — parse XLSX for seed script

**React frontend:**
- `react-leaflet` + `leaflet` — map strip
- `react-dropzone` — file upload
- `axios` — API calls

---

## 8. Implementation Phases

### Phase 1: Foundation
- `rails new geo_reader_api --api` with Supabase Postgres config
- Database migrations for all tables, enable PostGIS + pg_trgm
- Seed script: parse CIESIN XLSX into `urban_populations` (use `roo` gem)
- Import Maddison country data into `country_populations`
- Import continent data + country-continent mapping
- Seed `travel_speed_references` from the markdown tables
- `npx create-react-app geo-reader-client` with basic routing

### Phase 2: Core Pipeline
- File upload endpoint + Supabase Storage for PDFs/images
- Text extraction services (PDF, image, text passthrough)
- Regex entity extraction + DB matching
- Population lookup with linear interpolation
- Haversine distance + travel time calculation
- Annotation builder orchestrating the full pipeline
- Background job processing with status tracking (GoodJob)

### Phase 3: Frontend
- Upload component (drag-drop + paste)
- Text viewer with highlighted entity spans (clickable)
- Annotation sidebar with population + travel cards
- Leaflet.js map strip (collapsible) with markers + distance lines
- Scroll linking between highlighted text and annotation cards
- Page navigation
- Processing status indicator (polling `/status`)

### Phase 4: Polish
- Responsive layout (stack panels on narrow screens)
- Error handling and edge cases
- Cache repeated population queries
- Deploy: Render/Railway (Rails), Vercel (React)

---

## 9. Verification Plan

1. **Seed data**: `SELECT count(*) FROM urban_populations` = 10,352. Spot-check: `SELECT * FROM urban_populations WHERE city = 'Paris' ORDER BY year` returns multiple centuries of data.
2. **Population lookup**: `GET /api/v1/populations/city?city=Paris&year=1832` returns interpolated ~774K with bracketing data points.
3. **Travel calc**: `GET /api/v1/travel/calculate?from_lat=48.85&from_lon=2.35&to_lat=45.76&to_lon=4.83` returns ~292 miles, foot 16-22 days, horse 5-8 days.
4. **Full pipeline**: Upload text mentioning "Paris" and "Lyon" in "1832". Verify entities extracted, annotations created, displayed in dual-panel UI with map markers.
5. **Regex extraction**: Test with "In 1832, Paris was a city of barricades" — should extract year 1832 and location Paris, match to DB.
