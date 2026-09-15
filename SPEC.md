# Manhattan Grocery Index - v1 specification

## Product goal

Answer two questions for grocery shopping in Manhattan:

1. Where can I find an ingredient or grocery item, including everyday staples, specialty products, seasonal goods, and brand alternatives?
2. What does it cost, where is the best observed price, and when are the savings worth a longer trip?

The product is a source-linked index, not an inventory guarantee. Every availability and price statement carries its source, observation time, and evidence type.

## v1 experience

The site ships as a fast, mobile-first map and search interface on GitHub Pages.

A user can:

- Search a generic item, brand, product name, category, or specialty term.
- See stores and markets that carry, advertise, or are expected to offer the item.
- Filter by neighborhood, price range, distance, store type, brand, dietary tags, package size, price type, and freshness.
- Sort results by neighborhood, price from low to high or high to low, distance, and freshness.
- Compare like-for-like unit prices while retaining the original package and offer details.
- Switch between map and list views.
- See the cheapest current observed option, the cheapest nearby option, and the savings available farther away.
- See why each result exists: the source link, observed date, validity window, and confidence.
- Browse current farmers-market vendors and seasonal product categories.

## Architecture

### Static application

- GitHub Pages hosts HTML, CSS, JavaScript, map assets, and prebuilt search indexes.
- No application server is required for v1.
- The browser performs local filtering, sorting, and distance calculations against versioned static data files.
- The repository is the database and audit trail.

### Scheduled collection

GitHub Actions runs source-specific collectors on conservative schedules:

- Government locations: monthly, plus a manual refresh option.
- Farmers-market schedules: weekly in season and monthly off-season.
- Current market/vendor pages: once per market operating cycle where practical.
- Official circulars: once per published weekly cycle.
- Open product and price datasets: weekly.
- USDA benchmarks: weekly.

Each collector writes raw source snapshots, normalized records, validation reports, and a manifest. Collection failures preserve the last known valid data and mark it stale rather than replacing it with blanks.

### Repository layout

```text
/
  app/                      # Static site source
  data/
    raw/                    # Immutable source snapshots by source/date
    normalized/
      locations.json
      products.json
      offers.json
      availability.json
      benchmarks.json
    manifests/              # Run time, source URL, hashes, counts, status
  schemas/                  # JSON Schema definitions
  collectors/               # Source-specific collection and parsing code
  pipeline/                 # Normalization, matching, validation, build steps
  public/data/              # Compact files and indexes served by Pages
  tests/                    # Parser fixtures, schema and regression tests
  docs/                     # Source notes and data dictionary
```

## Data layers

### 1. Locations

One canonical record per store, market, or seasonal retail location:

- stable internal ID
- name and normalized chain/operator
- location type: supermarket, grocery, specialty, farmers market, farmstand, seasonal shop
- address, latitude, longitude, ZIP, neighborhood, community district
- public hours and seasonal dates when available
- source URL, source record ID, observed time, last verified time

Primary sources:

- New York State Retail Food Stores open dataset
- NYC Farmers Markets open dataset
- USDA Local Food Portal as a supplemental directory
- official store and market location pages for validation

### 2. Products

A canonical product entity supports both packaged goods and generic foods:

- product ID
- canonical name
- brand and sub-brand
- category and aliases
- barcode when available
- package quantity, unit, and normalized base quantity
- dietary, organic, origin, and specialty tags where sourced

Open Food Facts seeds packaged-product identity, brand, barcode, package, ingredient, and category fields. Generic produce, meat, seafood, bulk goods, and market categories use a controlled taxonomy maintained in the repository.

### 3. Offers and prices

Every price is an observation, never an eternal product attribute:

- location ID and product ID
- observed price and currency
- package quantity and normalized unit price
- regular/reference price only when explicitly published
- offer start and end dates
- membership, quantity, coupon, deposit, or other conditions
- source URL and captured time
- evidence type and confidence

Price evidence types:

- `advertised_sale`: official store circular or sales page
- `online_price`: public first-party product page
- `receipt_paid`: actual price paid on a dated receipt
- `crowdsourced`: Open Prices record with proof and quality checks
- `benchmark`: USDA regional advertised-price reference

The UI never collapses these into an unlabeled price. Benchmarks are context, not store offers.

### 4. Availability

Availability evidence is also typed:

- `directory_listing`: location exists, with no product claim
- `catalog_carries`: item appears in a public catalog
- `advertised_this_week`: item appears in a current circular
- `expected_vendor`: a current market roster lists a producer/category
- `receipt_observed`: item was purchased there on the receipt date

The UI uses plain labels such as "advertised through Sep 17" or "expected Sunday," not "in stock," unless a clean source explicitly provides current inventory.

### 5. Benchmarks and travel value

For comparable offers, v1 computes:

- unit price
- savings against the best nearby observation
- savings against the Manhattan median for the same normalized item/size class
- USDA regional comparison where compatible
- extra distance from a chosen neighborhood or map point
- minimum basket quantity needed for a farther trip to save money

Default travel value is factual rather than prescriptive:

```text
trip savings = nearby basket total - destination basket total
net trip value = trip savings - optional user-entered travel cost
```

The interface shows savings, extra distance, and data freshness separately. It does not invent a dollar value for the user's time.

## Source onboarding order

### Phase A - location and taxonomy spine

1. New York State Retail Food Stores
2. NYC Farmers Markets
3. neighborhood assignment from geographic boundaries
4. Open Food Facts product normalization
5. USDA Local Food Portal supplemental locations

Deliverable: searchable Manhattan store/market map with categories and source provenance.

### Phase B - current clean price observations

1. Key Food family store-specific circulars
2. CTown
3. Associated
4. Food Bazaar East 125th
5. Gristedes weekly specials
6. Morton Williams weekly specials
7. Fairway weekly circulars
8. Whole Foods store-specific sales flyers
9. Lidl Harlem and ALDI East Harlem weekly deals

Each source begins with one store and one fixture-backed parser. Expand only after the parser handles validity dates, package size, membership conditions, and source links correctly.

### Phase C - specialty and seasonal discovery

1. GrowNYC market pages and expected producer/category rosters
2. public first-party specialty catalogs with clear product and price pages
3. USDA Local Food Portal validation
4. user receipt imports for historical observations

Deliverable: specialty search, seasonal market view, and more brand alternatives.

### Phase D - comparison and quality

1. Open Prices observations with proof and anomaly screening
2. USDA AMS weekly advertised-price benchmarks
3. item-matching review queue
4. travel-value and basket comparison

## Matching and normalization

The central rule is to preserve the source record while linking it to a canonical item.

Matching priority:

1. exact barcode
2. brand + normalized product name + package quantity
3. controlled generic-food taxonomy + grade/organic/form attributes
4. cautious fuzzy match that requires review below a confidence threshold

Unit conversion supports mass, volume, count, and common produce sale units. It never compares incompatible forms without an explicit relationship, such as fresh basil versus dried basil or whole tomatoes versus canned tomatoes.

Brand alternatives appear under a shared generic need while remaining separate products. Store brands are treated as real brands, not generic placeholders.

## Data quality and provenance

Every build validates:

- schema conformance
- duplicate locations and products
- impossible prices and unit quantities
- expired offers
- abrupt price changes
- unmatched source records
- source freshness
- parser yield changes against prior runs

Records that fail validation are quarantined from the public build and listed in a run report. Missing values remain null. A failed collector cannot turn missing data into zero price or unavailable inventory.

Confidence levels:

- `high`: direct official/open record with exact location and product match
- `medium`: direct record with a category-level or inferred product link
- `low`: crowdsourced or fuzzy-matched observation awaiting stronger confirmation

Every result links to its original source where a stable URL exists.

## v1 scope

v1 ships:

- public GitHub Pages site
- Manhattan map with neighborhood and price filters, plus neighborhood and price sorting
- store, specialty-store, farmers-market, and seasonal-location directory
- item/category/brand search
- official advertised-price observations from the first supported circular sources
- normalized unit prices and offer conditions
- current market/vendor category discovery
- source links, observation dates, validity windows, freshness, and confidence
- nearby-versus-farther savings comparison
- static data pipeline, schemas, tests, manifests, and scheduled refreshes

v1 does not claim:

- complete shelf-price coverage
- guaranteed real-time inventory
- perfect same-item matching
- that an advertised deal is available at every branch
- that a regional benchmark is a Manhattan store price

## Later product work

After the MVP is accurate and useful:

- saved shopping lists and multi-item basket optimization
- user-selected starting point and transit/walking travel estimates
- price-history charts and sale-cycle detection
- receipt upload and correction workflow
- community corrections with moderation and evidence
- substitution suggestions across brands, sizes, and dietary needs
- alerts for watched products, markets, and neighborhoods
- broader borough coverage

## Success measures

- location coverage: share of licensed Manhattan food retailers correctly mapped
- freshness: share of active offers within their validity window
- provenance: share of public records with a working source link and timestamp
- normalization: share of offers with valid unit prices and canonical product links
- accuracy: reviewed sample precision for location, product match, conditions, and price
- usefulness: search success for a test set of staples, brands, and specialty ingredients
- resilience: scheduled runs that fail safely without corrupting the published index

## First implementation milestone

A thin vertical slice should include:

1. the two government location datasets
2. neighborhood assignment
3. one official store-specific circular source
4. one GrowNYC Manhattan market page
5. Open Food Facts normalization for packaged items
6. a static map/search UI
7. source, freshness, and confidence displayed on every result
8. tests proving expired offers disappear and failed collection preserves prior valid data

That slice tests the hardest parts early: source provenance, item matching, schedule-aware availability, and honest price labels.
