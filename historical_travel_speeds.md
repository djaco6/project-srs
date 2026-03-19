# Historical Travel Speeds — Reference for Narrative Overlay System

Sources compiled from scholarly literature and primary-source-based histories.
Note: true mean/stdev statistics exist for only one study (Hall 2023); elsewhere, low/high figures can be treated as roughly ±1 SD from the central estimate.

---

## Distance Calculation

For straight-line distance between two lat/lon coordinate pairs, use the **Haversine formula** — no API required.

```python
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))
```

For road/routing distance, options include:
- **Google Maps Distance Matrix API** (paid after free tier)
- **OpenRouteService** (free, open source)
- **Mapbox Matrix API**

### Terrain Multipliers (apply to straight-line distance)

| Terrain | Multiplier |
|---|---|
| Flat, well-roaded (Roman roads, river valleys, plains) | 1.10–1.15× |
| Rolling hills, typical European countryside | 1.20–1.30× |
| Mountain crossings (Alps, Pyrenees, Zagros) | 1.50–2.00× |
| Desert with oasis routing | 1.40–1.60× |
| River travel downstream | may be < 1.00× |

**Recommended default:** 1.20× for general-purpose use.

---

## Travel Speed Estimates by Mode

### On Foot

| Condition | Low (km/day) | Central (km/day) | High (km/day) |
|---|---|---|---|
| Loaded traveler, poor conditions, winter | 15 | 20 | 25 |
| Normal traveler, average roads | 25 | 30 | 35 |
| Roman military pace (loaded, disciplined) | 29 | 32 | 36 |
| Forced march / urgent travel | 35 | 40 | 48 |

**Key sources:**

- **Hall, Jacob (2023). "Travel Speed over the Longue Durée."** SSRN.
  Using daily travel itineraries of medieval kings across England and France over four centuries. Finds average travel speed of 15–20 miles/day, stable over the period but with "great heterogeneity at the journey level."
  [https://ssrn.com/abstract=4635304](https://ssrn.com/abstract=4635304)

- **Boyer, Marjorie Nice — cited in Medievalists.net (2025).**
  Based on records from 14th-century France: foot travelers expected ~30 miles/day (8–10 hours walking). The Countess of Leicester's household covered ~15 miles/day in midwinter and ~30 miles/day when hurrying in June.
  [https://www.medievalists.net/2025/01/struggles-travel-middle-ages/](https://www.medievalists.net/2025/01/struggles-travel-middle-ages/)

- **Vegetius / Roman military standards — Wikipedia: Loaded March.**
  Roman recruits required to complete 20 Roman miles (29.62 km) with 20.5 kg in five summer hours ("regular step"); advancing to 24 Roman miles (35.5 km) at "full pace." Training included forced marches of 20–30 miles.
  [https://en.wikipedia.org/wiki/Loaded_march](https://en.wikipedia.org/wiki/Loaded_march)

- **Bandaarcgeophysics.co.uk — "Marching Roman Legionaries."**
  Detailed biomechanical study of Roman legionary march. Establishes 29 km as the commonly assumed legionary day-rate at 4.59 kph (1.2741 m/s) with 40 kg load over flat Roman road. Includes energy expenditure tables and modern US Army heat stress comparisons.
  [https://www.bandaarcgeophysics.co.uk/arch/Roman_legionary_marchingV2.html](https://www.bandaarcgeophysics.co.uk/arch/Roman_legionary_marchingV2.html)

- **Imperium Romanum — "Roman Army March."**
  Roman military march types: *iter iustum* ~30 km/day; *iter magnum* ~36 km/day. Caesar's Corfinium-to-Brundisium march (465 km, 49 BC) corroborates these figures.
  [https://imperiumromanum.pl/en/roman-army/roman-army-march/](https://imperiumromanum.pl/en/roman-army/roman-army-march/)

- **EN World thread — "Travel times in fantasy/pre-industrial society."**
  Aggregates multiple historical sources. Notes 25–30 miles (40–45 km/day) as consistent for lightly-to-moderately encumbered healthy humans on flat hard terrain, citing WWII Wehrmacht estimates and Roman legion data.
  [https://www.enworld.org/threads/travel-times-in-fantasy-pre-industrial-society-by-foot-horse-boat-etc.318719/](https://www.enworld.org/threads/travel-times-in-fantasy-pre-industrial-society-by-foot-horse-boat-etc.318719/)

---

### On Horseback (single horse, sustained multi-day)

| Condition | Low (km/day) | Central (km/day) | High (km/day) |
|---|---|---|---|
| Pack horse with cargo | 30 | 35 | 40 |
| Ordinary riding, sustained multi-day | 40 | 50 | 65 |
| Military cavalry, sustained march | 40 | 48 | 55 |
| Single urgent day, one horse | 65 | 80 | 100 |
| Relay / post system (fresh horses) | 100 | 150 | 300 |

> **Important distinction:** Horses can sprint far faster than these figures but cannot sustain it. The sustained multi-day figures are the relevant ones for historical travel. Forced marches of 65–80 km resulted in significant horse casualties.

**Key sources:**

- **Spufford, Peter. *Power and Profit: The Merchant in Medieval Europe* — cited in writemedieval.livejournal.com.**
  Primary-source-based economic history. Normal distance for any carrier: 30–40 km/day. Pack animals over the Simplon pass: just over 30 km per stage. Heavy carts 30–40 km; lighter carts under 30 km. A convoy of 4 men and 6 horses averaged 50 km/day from Dijon to Paris in January 1412.
  [https://writemedieval.livejournal.com/4706.html](https://writemedieval.livejournal.com/4706.html)

- **HorseRacingSense.com — "How Far Can A Horse Travel In A Day?"**
  Military cavalry sustainable march: 25–30 miles (40–48 km/day). Forced marches of 40–50 miles resulted in 20–30% horse casualties. Pony Express: individual horses covered 10–15 miles per leg, then rested 3–4 days.
  [https://horseracingsense.com/how-far-can-a-horse-travel-in-a-day/](https://horseracingsense.com/how-far-can-a-horse-travel-in-a-day/)

- **PopularBeethoven.com — "Estimated Time of Arrival."**
  1700s–1800s European norms: typical horseback rider 50–70 km/day; fast messenger with horse changes 80–100 km/day; heavy carts 30–50 km/day.
  [https://www.popularbeethoven.com/estimated-time-of-arrival/](https://www.popularbeethoven.com/estimated-time-of-arrival/)

- **IndiesUnlimited.com — "Getting it Right: Time and Distance on Foot and Horse."**
  20–30 miles (32–48 km/day) sustainable for average horse; fit horse can do 40–50 miles (65–80 km) for 4–5 days before needing a day off. Walking humans: ~20 miles (32 km/day) on extended journeys.
  [https://indiesunlimited.com/2020/03/24/getting-it-right-time-and-distance-on-foot-and-horse/](https://indiesunlimited.com/2020/03/24/getting-it-right-time-and-distance-on-foot-and-horse/)

- **EN World thread (see above)** — notes that sustained cavalry march rates converge with infantry over multi-day journeys due to horse grazing requirements.
  [https://www.enworld.org/threads/travel-times-in-fantasy-pre-industrial-society-by-foot-horse-boat-etc.318719/](https://www.enworld.org/threads/travel-times-in-fantasy-pre-industrial-society-by-foot-horse-boat-etc.318719/)

---

### Cart / Wagon (for completeness)

| Type | Low (km/day) | Central (km/day) | High (km/day) |
|---|---|---|---|
| Ox cart, heavy load | 15 | 20 | 25 |
| Light two-wheeled cart | 20 | 25 | 30 |
| Heavy four-wheeled cart, good roads | 30 | 35 | 40 |

> **Note:** Before ~1000 CE in most regions (and much later in many), "horse travel" for ordinary people usually meant cart, not riding. Riding horses were expensive and elite. Cart speed is often comparable to or slower than walking.

---

## Suggested Implementation Logic

```python
distance_adjusted = haversine_miles * 1.2  # default terrain multiplier

# Walking
walking_low_days  = distance_adjusted / (25 * 0.621)  # 25 km/day in miles
walking_high_days = distance_adjusted / (15 * 0.621)  # 15 km/day in miles

# Horse (single horse, sustained)
horse_low_days  = distance_adjusted / (50 * 0.621)
horse_high_days = distance_adjusted / (35 * 0.621)
```

### Suggested UI Display

```
Journey: [Place A] → [Place B]  (~X miles as traveled)

On foot:      roughly N–M weeks
On horseback: roughly N–M days

Estimates vary by season, terrain, load, and era.
Relay/post riders (state actors, wealthy merchants) could cover 2–5× these distances.
```

---

## Historical Route Tools

### Roman Empire (~200 CE) — ORBIS

The gold standard. Interactive tool from Stanford University.

- **ORBIS: Stanford Geospatial Network Model of the Roman World**
  632 sites, 84,631 km of roads, 28,272 km of navigable rivers, 900 sea routes with monthly wind data. 14 modes of transport. Returns journey time, distance, and cost (in denarii) between any two points. Data downloadable.
  [https://orbis.stanford.edu/](https://orbis.stanford.edu/)

- **OmnesViae — Roman Route Planner**
  Based on the Tabula Peutingerina and Antonine Itinerary (primary sources). More historically grounded, less computational.
  [https://omnesviae.org/](https://omnesviae.org/)

- **Live Science overview of ORBIS**
  [https://www.livescience.com/20211-google-maps-ancient-rome-shows-travel-times-2000-years.html](https://www.livescience.com/20211-google-maps-ancient-rome-shows-travel-times-2000-years.html)

- **Brilliant Maps — ORBIS isochrone map from Rome**
  [https://brilliantmaps.com/travel-time-rome/](https://brilliantmaps.com/travel-time-rome/)

### Other Eras — No Equivalent Tools Exist

No interactive tools comparable to ORBIS exist for other regions or eras. Use per-day estimates above with Haversine + terrain multiplier.

| Region / Era | Notes |
|---|---|
| Medieval Europe | No tool. Use Hall (2023) and Boyer figures. |
| Silk Road | No tool. Caravan speed ~30–40 km/day but routes non-linear and politically fragmented. |
| Medieval Islamic world | Research literature only (al-Idrisi, Ibn Battuta). |
| Ancient China | No tool. |
| Mongol Empire | Yam relay system: 150–300 km/day for official couriers; regular army ~24 km/day. |
| Colonial Americas | No tool. |

---

## Seasonality

ORBIS makes a significant point of seasonal variation — worth noting in overlays when context is available:

- Winter travel in northern Europe / at altitude: reduce speed by 30–50%
- Mediterranean sea routes effectively closed October–March in antiquity
- Spring mud season in temperate regions: significant slowdowns
- Summer heat in desert or southern regions: limited daytime travel

---

## Additional Background Reading

- **Wikipedia: Preferred Walking Speed** — physiological basis for human walking pace (~5 km/h preferred, ~4.4 km/h metabolically optimal)
  [https://en.wikipedia.org/wiki/Preferred_walking_speed](https://en.wikipedia.org/wiki/Preferred_walking_speed)

- **Wikipedia: BIOS / Itinerarium** — Roman travel guides (itineraria) as primary sources for road distances
  [https://en.wikipedia.org/wiki/Itinerarium](https://en.wikipedia.org/wiki/Itinerarium)

- **Medievalists.net — "The Struggles of Travel in the Middle Ages"** (2025)
  Good narrative overview with Boyer citation and concrete examples including Margaret of Brabant's cart journey (18 days for 85 miles, London to Ipswich, 1297).
  [https://www.medievalists.net/2025/01/struggles-travel-middle-ages/](https://www.medievalists.net/2025/01/struggles-travel-middle-ages/)
