# Section 1 — Product Description -- "Alexandria" Web App

Name is a homage to the Library of Alexandria, the largest library in the ancient world 

## 1.1 Problem Statement

Texts in history, geography, and current affairs are dense with place names, dates, and implicit spatial relationships. When a reader encounters a passage describing events in "Paris in 1832," they lack immediate access to the contextual information that would deepen their understanding — how large was Paris at the time? How did its population compare to the rest of France or Europe? If the text also mentions Lyon, how far apart were the two cities, and how long would it have taken to travel between them?

Today, readers who want this context must leave their text, search manually on Wikipedia or Google Maps, and piece together fragmented results across multiple tabs. This process is slow, disruptive to reading flow, and often yields modern-day data rather than period-accurate figures.

Alexandria solves this problem by automatically identifying locations and dates in uploaded texts and presenting historically accurate population data and pre-industrial travel estimates inline alongside the reading experience. It transforms passive reading into an geographically informed activity without requiring the reader to leave the page.

## 1.2 Product Perspective

Alexandria is a standalone web application. It does not replace or extend an existing tool — no comparable product currently offers automatic, inline geographic and demographic annotation of arbitrary uploaded texts with historical population data.

The system is self-contained: it consists of a React single-page application (frontend), a Ruby on Rails API (backend), and a Supabase-hosted PostgreSQL database seeded with historical population datasets. It does not depend on external AI or NLP services for its core functionality. Text extraction (from PDFs and images) and entity recognition (locations and dates) are handled entirely within the backend using open-source libraries and programmatic pattern matching against the database. User authentication is handled by Devise, the most widely adopted authentication framework for Rails, providing email/password registration, login, and session management.

The application operates independently and is not part of a larger platform, though its modular API design would allow future integration into other reading or research tools.

## 1.3 User Classes

### 1.3.1 Reader (Primary User)

- **Description**: Any person reading a text with geographic content — students, teachers, history enthusiasts, researchers, journalists, or casual readers.
- **Technical skill level**: Basic familiarity with web applications. No technical expertise required.
- **Goals**: Upload or paste a text, then read it with automatic geographic and demographic annotations displayed in a sidebar. View locations on an interactive map. Understand population scale and travel distances for the time period discussed in the text.
- **Frequency of use**: Occasional to moderate. A reader may use the tool whenever they encounter a geographically dense text.
- **Authentication**: Required. Readers register and log in via the Devise authentication system (email/password). Authenticated access allows documents to be associated with a user account.

### 1.3.2 Admin

- **Description**: A team member or system operator responsible for managing the reference datasets (historical population data, travel speed tables) and monitoring system health.
- **Technical skill level**: Comfortable with web-based admin interfaces. Familiar with the data sources used by the system.
- **Goals**: Add, update, or correct records in the population and travel speed reference tables. Review processing logs. Manage uploaded documents if needed.
- **Frequency of use**: Infrequent. Admins interact with the system primarily during initial setup, data imports, or when correcting data quality issues.
- **Authentication**: Authenticated access required. Admins log in through the same Devise system as readers, with an elevated role granting access to dataset management features.

## 1.4 Operating Environment

- **Platform**: Web application accessed through a browser. No installation required.
- **Supported browsers**: Latest stable versions of Google Chrome, Mozilla Firefox, Apple Safari, and Microsoft Edge.
- **Device targets**: Desktop-first design. The layout uses a dual-panel arrangement (text panel + annotation sidebar) optimized for screens 1024px and wider. On narrow screens (tablets and phones), panels stack vertically and the map strip collapses to a toggle button, providing basic mobile responsiveness.
- **Accessibility**: Standard semantic HTML and keyboard-navigable UI elements. Text remains readable at default and enlarged font sizes. No specific WCAG conformance level is targeted for the MVP, though the design avoids known accessibility anti-patterns (e.g., color-only indicators, missing alt text on map elements).
- **Backend hosting**: Rails API deployed to a cloud platform (e.g., Render or Railway). Database hosted on Supabase (free tier, 500 MB).
- **Frontend hosting**: React SPA deployed to a static hosting service (e.g., Vercel).

## 1.5 Scope

### What the System Does

- Accepts text input via direct paste, PDF upload, or image upload (with OCR)
- Extracts location names and date/year mentions from the text using pattern matching and database lookup
- Associates each detected location with the nearest date mention in the text
- Retrieves historical population data for identified cities, countries, and continents at the relevant time period, using linear interpolation between known data points
- Calculates straight-line distances between co-mentioned locations and estimates historical travel times by foot, horseback, and cart
- Displays the original text with highlighted location and date entities in a reading panel
- Shows population and travel annotations in a synchronized sidebar
- Renders detected locations on an interactive map (Leaflet.js) with distance lines between co-mentioned locations
- Processes documents asynchronously with status tracking
- Authenticates users via email/password (Devise), associating uploaded documents with user accounts
- Supports role-based access: Readers can upload and view their own documents; Admins can manage reference datasets

### What the System Does Not Do

- **No AI/NLP entity extraction**: The MVP uses regex-based pattern matching and database lookup — not machine learning or external AI APIs. AI-powered extraction (e.g., OpenAI GPT-4o-mini for structured output) is a planned future enhancement.
- **No OAuth or social login**: The MVP supports email/password authentication only. Third-party login (Google, GitHub, etc.) is a potential future enhancement.
- **No real-time collaboration**: Documents are processed and viewed individually. There is no shared annotation or multi-user editing.
- **No native mobile application**: The system is a web application only. No iOS or Android app is planned.
- **No modern routing or directions**: Travel estimates use Haversine straight-line distance with a terrain multiplier — not modern road routing APIs.
- **No editing or annotation by users**: Readers cannot add their own notes or correct extracted entities in the MVP.

### Possible Enrichments

- Authentication and storage of user's favorite texts -- problem: copyright -- PDF readers on desktop do allow local storage, unsure about webapps? Need to check into this
- Social features -- users (particularly enthusiast users) could potentially add annotations about a specific time or place to the system (eg: add to the "Paris 1832" data something like--"The June Rebellion occurred in Paris on 5 June" with a citation)...this is straying into Wikipedia territory with lots of potential conflict, so it might not be viable. We will probably just stick to a plain read only database 
