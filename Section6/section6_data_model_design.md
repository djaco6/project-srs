# Section 6 -- Data and Model Design

## UML Class Diagram

See `UML/combined_uml.svg` for the full class diagram, and individual class SVGs in `UML/`.

### 9 Model Classes

1. **User** (Devise-managed) -- authentication and role
2. **UserProfile** -- personal info, preferences, UX settings
3. **Document** -- uploaded/pasted texts with processing audit trail
4. **DocPage** -- individual pages within a document
5. **Entity** -- extracted location/date mentions with resolution data
6. **Annotation** -- computed population and travel results
7. **UrbanPopulation** -- seed data: historical city populations (CIESIN, 10,352 rows)
8. **RegionalPopulation** -- seed data: country/continent/polity populations (Maddison + HYDE)
9. **TravelSpeedReference** -- seed data: historical travel speed constants

### Relationships (with UML notation)

| Relationship | Type | Multiplicity | Notes |
|---|---|---|---|
| User -- UserProfile | Composition | 1..1 | Profile destroyed with user |
| User -- Document | Composition | 1..* | Documents belong to a user |
| Document -- DocPage | Composition | 1..* | Pages destroyed with document |
| Document -- Entity | Composition | 1..* | Entities destroyed with document |
| Document -- Annotation | Composition | 1..* | Annotations destroyed with document |
| Entity -- Annotation | Association | 1..* | Annotation references entity(ies) |
| Entity -- UrbanPopulation | Association | *..0..1 | Entity optionally resolves to a city |
| Annotation -- RegionalPopulation | Dependency (lookup) | *..* | Annotation queries regional data |
| Annotation -- TravelSpeedReference | Dependency (lookup) | *..* | Travel annotations use speed constants |

---

## Model Classes with Attributes

### CL01: User (Devise-managed)

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| email | string | Devise: login credential |
| encrypted_password | string | Devise: bcrypt hash |
| reset_password_token | string | Devise: recoverable |
| reset_password_sent_at | datetime | Devise: recoverable |
| remember_created_at | datetime | Devise: rememberable |
| sign_in_count | integer | Devise: trackable |
| current_sign_in_at | datetime | Devise: trackable |
| last_sign_in_at | datetime | Devise: trackable |
| current_sign_in_ip | inet | Devise: trackable |
| last_sign_in_ip | inet | Devise: trackable |
| role | string | 'reader' or 'admin' |
| created_at | datetime | |
| updated_at | datetime | |

### CL02: UserProfile

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| user_id | bigint FK -> User | |
| first_name | string(50) | |
| last_name | string(50) | |
| display_name | string(100) | |
| avatar_url | text | |
| bio | text | |
| interests | text[] | e.g. ['history', 'geography'] |
| preferred_periods | string | e.g. '1800-1900' |
| preferred_reader_layout | string | 'dual_panel', 'stacked', or 'text_only' |
| prefers_historical_pops | boolean | DEFAULT true |
| preference_include_maps | boolean | DEFAULT true |
| created_at | datetime | |
| updated_at | datetime | |

### CL03: Document

| Attribute | Type | Notes |
|---|---|---|
| id | uuid PK | gen_random_uuid() |
| user_id | bigint FK -> User | |
| title | string | |
| source_type | string | 'pdf', 'image', or 'text' |
| storage_path | text | Supabase Storage path |
| raw_text | text | |
| status | string | 'pending', 'processing', 'ready', 'error' |
| page_count | integer | |
| submitted_ip | inet | Audit: IP at upload time |
| submitted_user_agent | string | Audit: browser info |
| processing_started_at | datetime | Audit: pipeline start |
| processing_completed_at | datetime | Audit: pipeline end |
| processing_duration_ms | integer | Audit: wall-clock time |
| error_message | text | Audit: error details |
| error_class | string | Audit: exception class |
| entity_count | integer | Cached count, DEFAULT 0 |
| annotation_count | integer | Cached count, DEFAULT 0 |
| last_accessed_at | datetime | Audit: last opened |
| created_at | datetime | |
| updated_at | datetime | |

### CL04: DocPage

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| document_id | uuid FK -> Document | |
| page_number | integer | |
| page_text | text | |
| created_at | datetime | |
| updated_at | datetime | |

### CL05: Entity

The Entity table is structured with clear section markers for future extensibility toward a TextSpan + EntityResolution split (Design B).

| Attribute | Type | Section | Notes |
|---|---|---|---|
| id | bigint PK | | |
| document_id | uuid FK -> Document | | |
| page_number | integer | SPAN | Future: TextSpan table |
| entity_type | string | SPAN | 'location' or 'date' |
| raw_text | string | SPAN | Exact text from document |
| char_offset_start | integer | SPAN | Position in page_text |
| char_offset_end | integer | SPAN | Position in page_text |
| resolved_city_id | string | RESOLUTION | Future: EntityResolution table |
| resolved_year | integer | RESOLUTION | Primary year interpretation |
| alternative_years | integer[] | RESOLUTION | Other plausible years |
| date_precision | string | RESOLUTION | 'exact_year', 'decade', 'century', 'approximate' |
| resolved_country | string | RESOLUTION | |
| resolved_lat | float | RESOLUTION | |
| resolved_lon | float | RESOLUTION | |
| extraction_method | string | AUDIT | 'regex_v1', future: 'gpt4o_mini' |
| match_type | string | AUDIT | 'exact', 'fuzzy', 'other_name', 'unresolved' |
| confidence_score | float | AUDIT | 0.0-1.0 |
| candidate_count | integer | AUDIT | DB candidates evaluated |
| resolution_notes | text | AUDIT | |
| resolved_at | datetime | AUDIT | |
| created_at | datetime | | |
| updated_at | datetime | | |

### CL06: Annotation

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| document_id | uuid FK -> Document | |
| page_number | integer | |
| annotation_type | string | 'population' or 'travel' |
| entity_id | bigint FK -> Entity | For population annotations |
| entity_a_id | bigint FK -> Entity | For travel annotations |
| entity_b_id | bigint FK -> Entity | For travel annotations |
| city_name | string | |
| year_queried | integer | |
| city_population | bigint | |
| city_pop_interpolated | boolean | |
| country_name | string | |
| country_population | bigint | |
| continent_name | string | |
| continent_population | bigint | |
| gdp_per_capita | float | From mpd2023 |
| distance_miles | float | Travel type only |
| distance_adjusted | float | After terrain multiplier |
| terrain_multiplier | float | DEFAULT 1.2 |
| foot_days_low | float | |
| foot_days_high | float | |
| horse_days_low | float | |
| horse_days_high | float | |
| computed_at | datetime | Audit: when generated |
| computation_duration_ms | integer | Audit: lookup time |
| data_sources_used | text[] | Audit: e.g. ['maddison_2023'] |
| city_pop_bracketing_years | integer[] | Audit: interpolation years |
| interpolation_method | string | 'exact', 'linear', 'nearest', 'extrapolated' |
| country_pop_source | string | Audit: estimate_source used |
| continent_pop_source | string | Audit: estimate_source used |
| stale | boolean | DEFAULT false, flag if data updated |
| created_at | datetime | |
| updated_at | datetime | |

### CL07: UrbanPopulation (seed data, read-only)

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| city | string | |
| other_name | string | Alternate names |
| country | string | |
| location | geography(Point, 4326) | PostGIS |
| latitude | float | |
| longitude | float | |
| certainty | smallint | 1=most accurate, 3=least |
| year | integer | Negative = BC |
| population | bigint | |
| city_id | string | Unique city identifier |

### CL08: RegionalPopulation (seed data, read-only)

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| region_name | string | |
| region_type | string | 'country', 'continent', or 'polity' |
| parent_region | string | For hierarchy traversal |
| year | integer | |
| population_estimate | bigint | |
| gdp_per_capita | float | From mpd2023 gdppc column |
| estimate_source | string | e.g. 'maddison_2023' |
| confidence_tier | integer | 1=census, 2=specialist, 3=standard DB, 4=model |
| notes | text | |

UNIQUE(region_name, region_type, year, estimate_source)

### CL09: TravelSpeedReference (seed data, read-only)

| Attribute | Type | Notes |
|---|---|---|
| id | bigint PK | |
| mode | string | 'foot', 'horse', or 'cart' |
| condition | string | 'normal', 'forced_march', 'pack_horse', etc. |
| km_per_day_low | float | |
| km_per_day_mid | float | |
| km_per_day_high | float | |

---

## Validations Tables

### CL01: User
| Attribute | Validations |
|---|---|
| email | presence, uniqueness (case-insensitive), format (email regex) |
| encrypted_password | presence, length (min 6 via Devise) |
| role | presence, inclusion: ['reader', 'admin'] |

### CL02: UserProfile
| Attribute | Validations |
|---|---|
| user_id | presence, uniqueness (one profile per user) |
| first_name | presence, length (max 50) |
| last_name | presence, length (max 50) |
| display_name | length (max 100), optional |
| avatar_url | format (URL), optional |
| bio | length (max 500), optional |
| interests | each element in allowed list, optional |
| preferred_periods | format (e.g. '1800-1900'), optional |
| preferred_reader_layout | inclusion: ['dual_panel', 'stacked', 'text_only'], default 'dual_panel' |
| prefers_historical_pops | boolean, default true |
| preference_include_maps | boolean, default true |

### CL03: Document
| Attribute | Validations |
|---|---|
| user_id | presence |
| title | presence, length (max 255) |
| source_type | presence, inclusion: ['pdf', 'image', 'text'] |
| status | presence, inclusion: ['pending', 'processing', 'ready', 'error'] |
| raw_text | presence (after processing) |
| page_count | numericality (>= 0), optional |
| submitted_ip | format (IP), optional |
| submitted_user_agent | length (max 500), optional |
| processing_duration_ms | numericality (integer, >= 0), optional |
| error_message | length (max 5000), optional (required if status='error') |
| entity_count | numericality (integer, >= 0), default 0 |
| annotation_count | numericality (integer, >= 0), default 0 |

### CL04: DocPage
| Attribute | Validations |
|---|---|
| document_id | presence |
| page_number | presence, numericality (integer, >= 1), uniqueness scoped to document_id |
| page_text | presence |

### CL05: Entity
| Attribute | Validations |
|---|---|
| document_id | presence |
| page_number | presence, numericality (integer, >= 1) |
| entity_type | presence, inclusion: ['location', 'date'] |
| raw_text | presence |
| char_offset_start | presence, numericality (integer, >= 0) |
| char_offset_end | presence, numericality (integer, > char_offset_start) |
| resolved_year | numericality (integer, -4000..2100), optional |
| alternative_years | each element numericality (integer, -4000..2100), optional |
| date_precision | inclusion: ['exact_year', 'decade', 'century', 'approximate'], optional |
| resolved_lat | numericality (-90..90), optional |
| resolved_lon | numericality (-180..180), optional |
| extraction_method | inclusion: ['regex_v1', 'gpt4o_mini', 'spacy'], optional |
| match_type | inclusion: ['exact', 'fuzzy', 'other_name', 'unresolved'], optional |
| confidence_score | numericality (0.0..1.0), optional |
| candidate_count | numericality (integer, >= 0), optional |

### CL06: Annotation
| Attribute | Validations |
|---|---|
| document_id | presence |
| annotation_type | presence, inclusion: ['population', 'travel'] |
| entity_id | presence if annotation_type == 'population' |
| entity_a_id | presence if annotation_type == 'travel' |
| entity_b_id | presence if annotation_type == 'travel' |
| year_queried | numericality (integer, -4000..2100), optional |
| terrain_multiplier | numericality (0.5..3.0), default 1.2 |
| distance_miles | numericality (>= 0), optional |
| interpolation_method | inclusion: ['exact', 'linear', 'nearest', 'extrapolated'], optional |
| stale | boolean, default false |

### CL07: UrbanPopulation
| Attribute | Validations |
|---|---|
| city | presence |
| country | presence |
| latitude | presence, numericality (-90..90) |
| longitude | presence, numericality (-180..180) |
| certainty | presence, inclusion: [1, 2, 3] |
| year | presence, numericality (integer) |
| population | presence, numericality (integer, > 0) |
| city_id | presence, uniqueness scoped to year |

### CL08: RegionalPopulation
| Attribute | Validations |
|---|---|
| region_name | presence |
| region_type | presence, inclusion: ['country', 'continent', 'polity'] |
| year | presence, numericality (integer) |
| population_estimate | numericality (integer, > 0), optional |
| gdp_per_capita | numericality (> 0), optional |
| estimate_source | presence |
| confidence_tier | presence, inclusion: [1, 2, 3, 4] |
| (composite unique) | region_name + region_type + year + estimate_source |

### CL09: TravelSpeedReference
| Attribute | Validations |
|---|---|
| mode | presence, inclusion: ['foot', 'horse', 'cart'] |
| condition | presence |
| km_per_day_low | presence, numericality (> 0) |
| km_per_day_mid | presence, numericality (> km_per_day_low) |
| km_per_day_high | presence, numericality (> km_per_day_mid) |

---

## Design Rationale

### Relationship Choices

The model uses composition for the User->Document->DocPage->Entity->Annotation chain because these objects have a clear ownership lifecycle: when a user is deleted, their documents cascade away, and when a document is deleted, its pages, entities, and annotations go with it. The User->UserProfile relationship is also composition (1:1) because a profile has no meaning without its user. By contrast, the reference data tables (UrbanPopulation, RegionalPopulation, TravelSpeedReference) use association/dependency relationships because they are shared, read-only seed data that exist independently of any user or document. An Entity's link to UrbanPopulation is an optional association (0..1) because not every extracted location candidate will match a known city in the dataset -- unmatched entities are retained with `match_type = 'unresolved'` for transparency. We considered splitting Entity into separate TextSpan and EntityResolution tables (separating "where in the document" from "what it means") but chose the monolithic design for MVP simplicity; this split is the planned refactor path when AI-based disambiguation is added in a future milestone.

### Unified RegionalPopulation

We consolidated country, continent, and polity population data into a single RegionalPopulation table with a `region_type` discriminator rather than maintaining separate tables. This design supports hierarchical lookups (country -> continent via `parent_region`) without joins across tables, and it naturally extends to sub-national historical regions (Roman provinces, Chinese prefectures) in future iterations without schema changes. The `estimate_source` and `confidence_tier` columns preserve scholarly provenance -- critical for a system presenting historical data where multiple sources may disagree. The `gdp_per_capita` column (sourced from the Maddison Project Database's existing `gdppc` field) is co-located with population data since both come from the same dataset and are queried together. Travel time estimates require no dedicated results table because they are computed on-the-fly using the Haversine formula, a terrain multiplier, and the TravelSpeedReference lookup, then stored as denormalized fields on the Annotation record for display performance.

### Audit Trail Philosophy

Every model in the processing pipeline (Document, Entity, Annotation) carries audit trail fields that record not just *what* was computed but *how* and *when*. Document tracks submission context (IP, user agent), processing lifecycle timestamps, and cached counts. Entity records the extraction method, match type, confidence score, and candidate count -- enabling future comparison of regex vs. AI extraction pipelines. Annotation captures computation provenance: which data sources contributed, which bracketing years were used for interpolation, and a `stale` flag for when underlying reference data is updated. This audit depth supports the admin audit view (user story RQ04/US4) and provides the traceability the SRS requires between entities, annotations, and data sources.
