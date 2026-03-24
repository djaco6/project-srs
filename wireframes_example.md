# Alexandria — ASCII Wireframe Options

## Prompt Used to Generate These

> For each of these user stories, please draw 3 different ASCII wireframes for me to choose from.
> We will then use these ASCII wireframes to create Balsamiq wireframes.
> Read the architecture plan to understand the context of the project.
>
> (1) As an external user, I need to be able to sign up for a profile
>
> (2) As an external user, I need to be able to save the texts I have analyzed
>
> (2a) As an external user, I need to be able to view an interface displaying all of the texts I have saved
>
> (3) As an admin user, I need to be able to view all user profiles
>
> (4) As an admin user, I need to be able to view all submitted texts and analyses performed to audit their accuracy

---

## User Story 1: Sign Up for a Profile

### Option A — Centered Form Card

Simple, centered registration card. Minimal and focused.

```
+=========================================================================+
|  Alexandria                                            [Log In]         |
+=========================================================================+
|                                                                         |
|                                                                         |
|              +---------- Create Your Account ----------+                |
|              |                                         |                |
|              |  Full Name                              |                |
|              |  +-------------------------------------+|                |
|              |  | e.g. Jane Smith                     ||                |
|              |  +-------------------------------------+|                |
|              |                                         |                |
|              |  Email                                  |                |
|              |  +-------------------------------------+|                |
|              |  | you@example.com                     ||                |
|              |  +-------------------------------------+|                |
|              |                                         |                |
|              |  Password                               |                |
|              |  +-------------------------------------+|                |
|              |  | ********                            ||                |
|              |  +-------------------------------------+|                |
|              |                                         |                |
|              |  Confirm Password                       |                |
|              |  +-------------------------------------+|                |
|              |  | ********                            ||                |
|              |  +-------------------------------------+|                |
|              |                                         |                |
|              |         [  Create Account  ]            |                |
|              |                                         |                |
|              |  Already have an account? Log in        |                |
|              +-----------------------------------------+                |
|                                                                         |
+=========================================================================+
```

### Option B — Split Screen (Branding Left, Form Right)

Left half shows app branding/description; right half has the form.

```
+=========================================================================+
|  Alexandria                                                             |
+=========================================================================+
|                                |                                        |
|   +--------------------------+|  +--- Sign Up ----------------------+  |
|   |                          ||  |                                   |  |
|   |   ~ Alexandria ~         ||  |  Full Name                       |  |
|   |                          ||  |  +-------------------------------+|  |
|   |   Your geographic        ||  |  |                               ||  |
|   |   reading assistant.     ||  |  +-------------------------------+|  |
|   |                          ||  |                                   |  |
|   |   Upload any text.       ||  |  Email                           |  |
|   |   See populations,       ||  |  +-------------------------------+|  |
|   |   distances, and         ||  |  |                               ||  |
|   |   travel times for       ||  |  +-------------------------------+|  |
|   |   every place and        ||  |                                   |  |
|   |   date mentioned.        ||  |  Password                        |  |
|   |                          ||  |  +-------------------------------+|  |
|   |   [map illustration]     ||  |  |                               ||  |
|   |                          ||  |  +-------------------------------+|  |
|   |                          ||  |                                   |  |
|   |                          ||  |  Confirm Password                |  |
|   |                          ||  |  +-------------------------------+|  |
|   |                          ||  |  |                               ||  |
|   |                          ||  |  +-------------------------------+|  |
|   |                          ||  |                                   |  |
|   |                          ||  |       [  Create Account  ]       |  |
|   |                          ||  |                                   |  |
|   |                          ||  |  Already have an account? Log in |  |
|   +--------------------------+|  +-----------------------------------+  |
|                                |                                        |
+=========================================================================+
```

### Option C — Stepped Registration (Wizard Style)

Two-step flow: account info first, then profile preferences.

```
+=========================================================================+
|  Alexandria                                            [Log In]         |
+=========================================================================+
|                                                                         |
|          Step [1]-------------[2]                                       |
|               Account Info     Preferences                              |
|                  *                                                       |
|              +---------- Step 1 of 2 -----------------+                 |
|              |                                         |                 |
|              |  Full Name                              |                 |
|              |  +-------------------------------------+|                 |
|              |  |                                     ||                 |
|              |  +-------------------------------------+|                 |
|              |                                         |                 |
|              |  Email                                  |                 |
|              |  +-------------------------------------+|                 |
|              |  |                                     ||                 |
|              |  +-------------------------------------+|                 |
|              |                                         |                 |
|              |  Password                               |                 |
|              |  +-------------------------------------+|                 |
|              |  |                                     ||                 |
|              |  +-------------------------------------+|                 |
|              |                                         |                 |
|              |  Confirm Password                       |                 |
|              |  +-------------------------------------+|                 |
|              |  |                                     ||                 |
|              |  +-------------------------------------+|                 |
|              |                                         |                 |
|              |                        [  Next ->  ]   |                 |
|              |                                         |                 |
|              |  Already have an account? Log in        |                 |
|              +-----------------------------------------+                 |
|                                                                         |
+=========================================================================+

--- After clicking Next: ---

+=========================================================================+
|  Alexandria                                            [Log In]         |
+=========================================================================+
|                                                                         |
|          Step [1]-------------[2]                                       |
|               Account Info     Preferences                              |
|                                   *                                     |
|              +---------- Step 2 of 2 -----------------+                 |
|              |                                         |                 |
|              |  What do you read most? (optional)      |                 |
|              |                                         |                 |
|              |  [ ] History texts                      |                 |
|              |  [ ] Current affairs / news             |                 |
|              |  [ ] Academic research                  |                 |
|              |  [ ] Literature / novels                |                 |
|              |  [ ] Other                              |                 |
|              |                                         |                 |
|              |  Preferred time periods (optional)      |                 |
|              |  +-------------------------------------+|                 |
|              |  | e.g. 1800-1900, Ancient Rome       ||                 |
|              |  +-------------------------------------+|                 |
|              |                                         |                 |
|              |       [<- Back]   [  Create Account  ] |                 |
|              +-----------------------------------------+                 |
|                                                                         |
+=========================================================================+
```

---

## User Story 2: Save Analyzed Texts

These wireframes show *how the save action appears* within the existing reading interface.

### Option A — Save Button in Top Action Bar

A persistent [Save] button in the header bar next to the document title.

```
+=========================================================================+
|  Alexandria    "Les Miserables Ch.1"    [Save] [Share] [New]   [jacob]  |
+=========================================================================+
|  +--MAP STRIP (collapsible)---------------------------------------------+
|  |     * Paris -------- 292 mi -------- * Lyon                          |
|  +----------------------------------------------------------------------+
|                                                                         |
|  +--TEXT PANEL (2/3)-------------+  +--ANNOTATION RAIL (1/3)----------+ |
|  |                               |  |                                  | |
|  |  In the summer of [1832],     |  |  +-- PARIS, 1832 -----------+   | |
|  |  [Paris] was a city of     ------->|  City pop: ~774,000        |   | |
|  |  barricades...                |  |  +---------------------------+   | |
|  |                               |  |                                  | |
|  +-------------------------------+  +----------------------------------+ |
|                                                                         |
|  --- After clicking [Save]: ---                                         |
|  +-------------------------------+                                      |
|  |  Saved to your library!       |                                      |
|  |  [View Library]    [Dismiss]  |                                      |
|  +-------------------------------+                                      |
+=========================================================================+
```

### Option B — Save via Modal Dialog

Clicking a save icon opens a modal where users can name and tag the text.

```
+=========================================================================+
|  Alexandria    "Untitled Document"         [Upload] [Paste]    [jacob]  |
+=========================================================================+
|  +--TEXT PANEL-------------------+  +--ANNOTATION RAIL----------------+ |
|  |  In the summer of [1832],    |  |  +-- PARIS, 1832 -----------+   | |
|  |  [Paris] was a city of    ------>|  City pop: ~774,000        |   | |
|  |  barricades...               |  |  +---------------------------+   | |
|  |                              |  |                                  | |
|  +---+----+---------------------+  +----------------------------------+ |
|      |    |                                                             |
|      v    v                                                             |
|  [Save icon] [Download]                                                 |
|                                                                         |
|     +============ Save to Library ============+                         |
|     ||                                        ||                        |
|     ||  Title                                 ||                        |
|     ||  +------------------------------------+||                        |
|     ||  | Les Miserables - Chapter 1         |||                        |
|     ||  +------------------------------------+||                        |
|     ||                                        ||                        |
|     ||  Tags (optional)                       ||                        |
|     ||  +------------------------------------+||                        |
|     ||  | history, france, 19th-century      |||                        |
|     ||  +------------------------------------+||                        |
|     ||                                        ||                        |
|     ||  Notes (optional)                      ||                        |
|     ||  +------------------------------------+||                        |
|     ||  | June Rebellion chapter             |||                        |
|     ||  +------------------------------------+||                        |
|     ||                                        ||                        |
|     ||       [Cancel]    [Save to Library]    ||                        |
|     +==========================================+                        |
+=========================================================================+
```

### Option C — Auto-Save with Status Indicator

Documents are saved automatically once analyzed. A status pill shows save state.

```
+=========================================================================+
|  Alexandria                         [New Text] [My Library]    [jacob]  |
+=========================================================================+
|                                                                         |
|  +--Document Header------------------------------------------------+   |
|  |  Les Miserables - Chapter 1           (Saved automatically)     |   |
|  |  Analyzed 2 min ago                   [cloud-check icon]        |   |
|  +------------------------------------------------------------------+  |
|                                                                         |
|  +--MAP STRIP-------------------------------------------------------+  |
|  |     * Paris -------- 292 mi -------- * Lyon                      |  |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +--TEXT PANEL (2/3)-------------+  +--ANNOTATION RAIL (1/3)--------+  |
|  |                               |  |                                |  |
|  |  In the summer of [1832],     |  |  +-- PARIS, 1832 ---------+   |  |
|  |  [Paris] was a city of     ------->|  City pop: ~774,000      |   |  |
|  |  barricades...                |  |  +-------------------------+   |  |
|  |                               |  |                                |  |
|  +-------------------------------+  +--------------------------------+  |
|                                                                         |
|  Status bar: [cloud-check] All changes saved   |   [Delete] [Export]   |
+=========================================================================+
```

---

## User Story 2a: View All Saved Texts (Library)

### Option A — Card Grid Layout

Saved texts displayed as cards in a responsive grid. Each card shows title, date, and entity count.

```
+=========================================================================+
|  Alexandria              [New Analysis]                        [jacob]  |
+=========================================================================+
|  [Reader] [My Library*]                                                 |
|                                                                         |
|  My Library (4 saved texts)                    Search: [___________]    |
|  Sort by: [Most Recent v]                                               |
|                                                                         |
|  +---------------------------+  +---------------------------+           |
|  | Les Miserables Ch.1      |  | Decline & Fall Ch.12     |           |
|  |                           |  |                           |           |
|  | 5 locations, 3 dates     |  | 12 locations, 8 dates    |           |
|  | Analyzed: Mar 20, 2026   |  | Analyzed: Mar 18, 2026   |           |
|  |                           |  |                           |           |
|  | [Open]         [Delete]  |  | [Open]         [Delete]  |           |
|  +---------------------------+  +---------------------------+           |
|                                                                         |
|  +---------------------------+  +---------------------------+           |
|  | NYT: Ukraine Update      |  | Age of Exploration       |           |
|  |                           |  |   Textbook Ch.3          |           |
|  | 8 locations, 2 dates     |  | 22 locations, 15 dates   |           |
|  | Analyzed: Mar 15, 2026   |  | Analyzed: Mar 10, 2026   |           |
|  |                           |  |                           |           |
|  | [Open]         [Delete]  |  | [Open]         [Delete]  |           |
|  +---------------------------+  +---------------------------+           |
|                                                                         |
+=========================================================================+
```

### Option B — List / Table Layout

Compact table format showing all saved texts with sortable columns.

```
+=========================================================================+
|  Alexandria              [New Analysis]                        [jacob]  |
+=========================================================================+
|  [Reader] [My Library*]                                                 |
|                                                                         |
|  My Library                                    Search: [___________]    |
|                                                                         |
|  +-----------------------------------------------------------------------+
|  | Title               | Source | Locations | Dates | Analyzed    |     |
|  |---------------------+--------+-----------+-------+-------------+-----|
|  | Les Miserables Ch.1 | Text   | 5         | 3     | Mar 20 2026 | [x]|
|  | Decline & Fall Ch12 | PDF    | 12        | 8     | Mar 18 2026 | [x]|
|  | NYT: Ukraine Update | Text   | 8         | 2     | Mar 15 2026 | [x]|
|  | Age of Exploration  | PDF    | 22        | 15    | Mar 10 2026 | [x]|
|  | Silk Road Routes    | Image  | 14        | 6     | Mar 05 2026 | [x]|
|  +-----------------------------------------------------------------------+
|                                                                         |
|  Showing 5 of 5 saved texts               [< Prev]  Page 1  [Next >]  |
|                                                                         |
|  Click any row to open the analysis view.                               |
+=========================================================================+
```

### Option C — Sidebar + Preview Layout

List of saved texts on the left; clicking one shows a preview on the right.

```
+=========================================================================+
|  Alexandria              [New Analysis]                        [jacob]  |
+=========================================================================+
|  [Reader] [My Library*]                                                 |
|                                                                         |
|  +-- Saved Texts --------+  +-- Preview --------------------------------+
|  | Search: [___________] |  |                                            |
|  |                        |  |  Les Miserables Ch.1                      |
|  | > Les Miserables Ch.1 |  |  Source: Pasted text                      |
|  |   Mar 20, 2026        |  |  Analyzed: Mar 20, 2026                   |
|  |   5 locs, 3 dates     |  |                                            |
|  |........................|  |  Locations found:                          |
|  |   Decline & Fall Ch12 |  |  Paris, Lyon, Marseille, Toulon, Digne    |
|  |   Mar 18, 2026        |  |                                            |
|  |   12 locs, 8 dates    |  |  Dates found:                             |
|  |........................|  |  1832, 1815, 1823                         |
|  |   NYT: Ukraine Update |  |                                            |
|  |   Mar 15, 2026        |  |  Text preview:                            |
|  |   8 locs, 2 dates     |  |  "In the summer of 1832, Paris was a     |
|  |........................|  |   city of barricades. The June Rebellion  |
|  |   Age of Exploration  |  |   drew thousands into the narrow..."     |
|  |   Mar 10, 2026        |  |                                            |
|  |   22 locs, 15 dates   |  |  [Open Full Analysis]        [Delete]     |
|  +------------------------+  +--------------------------------------------+
|                                                                         |
+=========================================================================+
```

---

## User Story 3: Admin — View All User Profiles

### Option A — Data Table with Inline Actions

Clean table of all registered users with key stats and actions.

```
+=========================================================================+
|  Alexandria Admin                                          [admin]      |
+=========================================================================+
|  [Dashboard] [Users*] [Texts & Analyses] [Datasets]                     |
|                                                                         |
|  All Users (47 registered)                     Search: [___________]    |
|  Filter: [All Roles v]                                                  |
|                                                                         |
|  +-----------------------------------------------------------------------+
|  | Name           | Email              | Role   | Texts | Joined      | |
|  |----------------+--------------------+--------+-------+-------------+-|
|  | Jane Smith     | jane@univ.edu      | Reader | 12    | Mar 01 2026 | |
|  | Carlos Ruiz    | cruiz@gmail.com    | Reader | 5     | Mar 05 2026 | |
|  | Aisha Patel    | aisha.p@school.edu | Reader | 23    | Feb 28 2026 | |
|  | Bob Admin      | bob@alexandria.app | Admin  | 0     | Feb 15 2026 | |
|  | Wei Zhang      | wzhang@uni.cn      | Reader | 8     | Mar 12 2026 | |
|  | Maria Lopez    | mlopez@yahoo.com   | Reader | 1     | Mar 20 2026 | |
|  +-----------------------------------------------------------------------+
|                                                                         |
|  Showing 1-6 of 47                         [< Prev]  Page 1  [Next >]  |
|                                                                         |
|  Click any row to view profile details.                                 |
+=========================================================================+
```

### Option B — Card Grid with Avatars

User profiles shown as visual cards with initials/avatars and summary stats.

```
+=========================================================================+
|  Alexandria Admin                                          [admin]      |
+=========================================================================+
|  [Dashboard] [Users*] [Texts & Analyses] [Datasets]                     |
|                                                                         |
|  All Users (47)              Search: [___________]  Filter: [All v]     |
|                                                                         |
|  +------------------------+  +------------------------+                  |
|  |  (JS)  Jane Smith      |  |  (CR)  Carlos Ruiz     |                 |
|  |  jane@univ.edu         |  |  cruiz@gmail.com       |                 |
|  |  Role: Reader           |  |  Role: Reader           |                |
|  |  Texts: 12              |  |  Texts: 5               |                |
|  |  Joined: Mar 01         |  |  Joined: Mar 05         |                |
|  |  Last active: Mar 23    |  |  Last active: Mar 19    |                |
|  |  [View] [Deactivate]   |  |  [View] [Deactivate]   |                 |
|  +------------------------+  +------------------------+                  |
|                                                                         |
|  +------------------------+  +------------------------+                  |
|  |  (AP)  Aisha Patel     |  |  (BA)  Bob Admin       |                 |
|  |  aisha.p@school.edu    |  |  bob@alexandria.app    |                 |
|  |  Role: Reader           |  |  Role: Admin            |                |
|  |  Texts: 23              |  |  Texts: 0               |                |
|  |  Joined: Feb 28         |  |  Joined: Feb 15         |                |
|  |  Last active: Mar 24    |  |  Last active: Mar 24    |                |
|  |  [View] [Deactivate]   |  |  [View] [Deactivate]   |                 |
|  +------------------------+  +------------------------+                  |
|                                                                         |
|  Showing 1-4 of 47                         [< Prev]  Page 1  [Next >]  |
+=========================================================================+
```

### Option C — Table with Slide-Out Detail Panel

Clicking a user row opens a detail panel on the right showing full profile info.

```
+=========================================================================+
|  Alexandria Admin                                          [admin]      |
+=========================================================================+
|  [Dashboard] [Users*] [Texts & Analyses] [Datasets]                     |
|                                                                         |
|  All Users (47)                                Search: [___________]    |
|                                                                         |
|  +--- User List ----------------+  +--- User Detail -----------------+  |
|  |                               |  |                                 |  |
|  |  Name            | Texts     |  |  Jane Smith                     |  |
|  |------------------+-----------|  |  jane@univ.edu                  |  |
|  | >Jane Smith      | 12        |  |                                 |  |
|  |  Carlos Ruiz     | 5         |  |  Role: Reader                   |  |
|  |  Aisha Patel     | 23        |  |  Joined: Mar 01, 2026           |  |
|  |  Bob Admin       | 0         |  |  Last active: Mar 23, 2026      |  |
|  |  Wei Zhang       | 8         |  |  Total texts: 12                |  |
|  |  Maria Lopez     | 1         |  |                                 |  |
|  |  Tom Brown       | 3         |  |  Recent Texts:                  |  |
|  |  Sara Kim        | 7         |  |  - Les Miserables Ch.1 (Mar 20) |  |
|  |  Raj Gupta       | 15        |  |  - Decline & Fall (Mar 18)      |  |
|  |  Lily Chen       | 4         |  |  - NYT: Ukraine (Mar 15)        |  |
|  |                               |  |                                 |  |
|  |                               |  |  [Change Role] [Deactivate]    |  |
|  +-------------------------------+  +---------------------------------+  |
|                                                                         |
|  Showing 1-10 of 47                        [< Prev]  Page 1  [Next >]  |
+=========================================================================+
```

---

## User Story 4: Admin — View All Submitted Texts and Analyses (Audit)

### Option A — Table with Expandable Rows

Each row is a document. Clicking expands to show extracted entities and accuracy info.

```
+=========================================================================+
|  Alexandria Admin                                          [admin]      |
+=========================================================================+
|  [Dashboard] [Users] [Texts & Analyses*] [Datasets]                     |
|                                                                         |
|  All Submitted Texts (128)                     Search: [___________]    |
|  Filter by: [All Users v]  [All Statuses v]  [All Sources v]           |
|                                                                         |
|  +-----------------------------------------------------------------------+
|  | Title               | User         | Source | Status | Entities |    |
|  |---------------------+--------------+--------+--------+----------+----|
|  | v Les Miserables    | Jane Smith   | Text   | Ready  | 8        |    |
|  |..................................................................    |
|  | | Extracted Entities:                                            |    |
|  | | LOC: Paris (matched, pop=774K), Lyon (matched, pop=150K),     |    |
|  | |      Toulon (matched), Digne (matched), Marseille (matched)   |    |
|  | | DATE: 1832, 1815, 1823                                        |    |
|  | |                                                                |    |
|  | | Annotations: 5 population lookups, 3 travel calculations      |    |
|  | | Unmatched candidates: "June", "Rebellion" (correctly rejected) |    |
|  | | [View Full Analysis]  [Flag for Review]  [Delete]             |    |
|  |..................................................................    |
|  |   Decline & Fall     | Aisha Patel  | PDF    | Ready  | 20       |    |
|  |   NYT: Ukraine       | Jane Smith   | Text   | Ready  | 10       |    |
|  |   Broken OCR test    | Carlos Ruiz  | Image  | Error  | 0        |    |
|  |   Silk Road Routes   | Wei Zhang    | Image  | Ready  | 20       |    |
|  +-----------------------------------------------------------------------+
|                                                                         |
|  Showing 1-5 of 128                       [< Prev]  Page 1  [Next >]   |
+=========================================================================+
```

### Option B — Split Panel (List Left, Audit Detail Right)

List of all texts on the left; selecting one shows full audit detail on the right.

```
+=========================================================================+
|  Alexandria Admin                                          [admin]      |
+=========================================================================+
|  [Dashboard] [Users] [Texts & Analyses*] [Datasets]                     |
|                                                                         |
|  +--- All Texts ----------------+  +--- Audit Detail -----------------+ |
|  | Search: [___________]        |  |                                   | |
|  | Filter: [All v] [Ready v]    |  |  Les Miserables Ch.1             | |
|  |                               |  |  Submitted by: Jane Smith        | |
|  | > Les Miserables   Ready     |  |  Source: Pasted text              | |
|  |   Decline & Fall   Ready     |  |  Status: Ready                    | |
|  |   NYT: Ukraine     Ready     |  |  Processed: Mar 20, 2026         | |
|  |   Broken OCR test  Error     |  |                                   | |
|  |   Silk Road Routes Ready     |  |  --- Extracted Entities ---       | |
|  |   Roman Empire     Processing|  |  Locations:                       | |
|  |   WWII Pacific     Ready     |  |   Paris     -> matched (774K)    | |
|  |   Cold War Berlin  Ready     |  |   Lyon      -> matched (150K)    | |
|  |                               |  |   Toulon    -> matched (18K)     | |
|  |                               |  |   Digne     -> matched (3K)      | |
|  |                               |  |   Marseille -> matched (145K)    | |
|  |                               |  |  Dates: 1832, 1815, 1823        | |
|  |                               |  |  Unmatched: "June", "Rebellion"  | |
|  |                               |  |                                   | |
|  |                               |  |  --- Travel Calculations ---     | |
|  |                               |  |  Paris<->Lyon: 292mi, 16-22d    | |
|  |                               |  |  Paris<->Marseille: 482mi       | |
|  |                               |  |                                   | |
|  |                               |  |  [Open as Reader] [Flag] [Delete]| |
|  +-------------------------------+  +-----------------------------------+ |
|                                                                         |
+=========================================================================+
```

### Option C — Dashboard Overview + Detailed Table

Top row shows aggregate stats; below is the full audit table.

```
+=========================================================================+
|  Alexandria Admin                                          [admin]      |
+=========================================================================+
|  [Dashboard] [Users] [Texts & Analyses*] [Datasets]                     |
|                                                                         |
|  +--- Summary Stats ------------------------------------------------+   |
|  |                                                                    |  |
|  |  Total Texts: 128   |  Ready: 119  |  Errors: 4  |  Processing: 5|  |
|  |  Total Entities Extracted: 1,847    |  Avg per text: 14.4          |  |
|  |  Unmatched Entity Rate: 12%        |  Flagged for Review: 3       |  |
|  +--------------------------------------------------------------------+  |
|                                                                         |
|  Search: [___________]  Filter: [All Users v]  [Status v]  [Date v]    |
|                                                                         |
|  +-----------------------------------------------------------------------+
|  | Title            | User        |Source|Status| Locs | Dates|Unmatched|
|  |------------------+-------------+------+------+------+------+---------|
|  | Les Miserables   | Jane Smith  | Text |Ready | 5    | 3    | 2      |
|  | Decline & Fall   | Aisha Patel | PDF  |Ready | 12   | 8    | 4      |
|  | NYT: Ukraine     | Jane Smith  | Text |Ready | 8    | 2    | 1      |
|  | Broken OCR test  | Carlos Ruiz | Img  |Error | 0    | 0    | --     |
|  | Silk Road Routes | Wei Zhang   | Img  |Ready | 14   | 6    | 3      |
|  | Roman Empire     | Raj Gupta   | PDF  |Proc. | --   | --   | --     |
|  | WWII Pacific     | Tom Brown   | PDF  |Ready | 18   | 11   | 5  [!] |
|  +-----------------------------------------------------------------------+
|                                                                         |
|  [!] = flagged for review       [< Prev]  Page 1 of 19  [Next >]      |
|                                                                         |
|  Click any row for full audit detail.                                   |
+=========================================================================+
```

---

## How to Use This Document

1. Review the 3 options (A, B, C) for each user story
2. Pick your preferred option for each (or mix elements from multiple)
3. Use the chosen ASCII wireframes as reference to build Balsamiq mockups
4. The wireframes can be adapted — they show layout and information hierarchy, not final visual design
