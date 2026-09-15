# Index-first slice specification

Status: **active scope for review**. This document specifies the next slice only. No implementation begins until the user reviews it.

The broader [`SPEC.md`](./SPEC.md) remains the product reference and is parked, not abandoned. Its price collection, comparison, basket-value, and modeling work are explicitly out of scope here. This slice preserves the item-location relationship needed to add observed prices later without redesigning the index.

## Outcome

Answer the first product question well:

> Where can I find an ingredient or grocery item, including everyday staples, specialty products, seasonal goods, and brand alternatives?

A search should return plausible Manhattan places, explain why each place appears, distinguish evidence from inference, and make weak coverage visible rather than inventing certainty.

## Boundaries

In scope:

- canonical grocery vocabulary
- profiles for the 366 existing locations
- item-to-location availability evidence
- search, filters, map/list results, and coverage reporting for discovery
- schema seams for a later price layer

Out of scope:

- collecting, modeling, ranking, or comparing prices
- chain price priors, BLS price baselines, basket savings, or travel-value calculations
- public crowd intake
- account-based sources
- automated use of retailer sites whose terms or robots rules prohibit it
- claims of live inventory or complete assortment

All source work follows the existing collector policy in `SPEC.md`: public and unauthenticated only; terms checked before onboarding; slow, documented and source-specific; facts only; stop on blocks, robots denial, challenge, login redirect, throttle, or publisher request; no alternate route after a barrier.

## 1. Item taxonomy

### Purpose

The taxonomy is the vocabulary shared by search, store profiles, availability records, and future prices. It covers generic needs first, then aliases and branded products.

### Category spine

1. Produce
2. Meat and poultry
3. Seafood
4. Dairy and eggs
5. Bakery and bread
6. Pantry and dry goods
7. Canned and jarred goods
8. Frozen food
9. Beverages
10. Snacks and sweets
11. Prepared food and deli
12. International and specialty
13. Dietary and wellness
14. Household and personal care
15. Seasonal and holiday

Categories may have nested subcategories, but every item has one primary category. Secondary tags support cross-category needs without duplicating the item.

### Canonical item record

```json
{
  "id": "item.gochujang",
  "name": "Gochujang",
  "kind": "generic_item",
  "primary_category": "international_and_specialty.korean",
  "aliases": ["Korean red pepper paste", "Korean chili paste"],
  "forms": ["paste"],
  "dietary_tags": ["vegetarian"],
  "seasonality": null,
  "brand_ids": [],
  "source": "curated_taxonomy",
  "reviewed_at": "YYYY-MM-DD"
}
```

`kind` is one of `generic_item`, `category_need`, or `branded_product`. Generic needs and branded products remain separate but can be linked. Forms that are not interchangeable remain separate or carry explicit relationships, for example fresh basil versus dried basil.

### Initial breadth

The first reviewed release targets 400-600 canonical entries:

- 150-200 everyday staples
- 150-250 international, dietary, and specialty items
- 50-100 seasonal/holiday items and categories
- aliases sufficient for common spellings, languages, and shopper terms

Breadth is less important than clean definitions. Unsupported dietary, origin, or ingredient attributes stay null.

### Seasonal handling

Seasonal entries carry named windows or event tags, not assumed availability:

```json
{"seasonality":{"type":"calendar_window","start_month":6,"end_month":9,"label":"summer"}}
```

A seasonal flag affects ranking and explanatory copy. It never turns an expected item into confirmed stock.

## 2. Store profiles

Every current location receives a profile that describes what kind of place it is and which departments it likely supports.

### Location profile

```json
{
  "location_id": "nys-123",
  "operator": "H Mart",
  "chain_id": "chain.h_mart",
  "format": "international_supermarket",
  "specialties": ["korean", "east_asian"],
  "departments": {
    "produce": "confirmed",
    "seafood_counter": "confirmed",
    "butcher": "expected",
    "bakery": "unknown",
    "prepared_food": "confirmed"
  },
  "snap_authorized": true,
  "profile_sources": [],
  "profile_confidence": "medium",
  "reviewed_at": "YYYY-MM-DD"
}
```

### Controlled formats

- supermarket
- discount_supermarket
- international_supermarket
- gourmet_market
- specialty_store
- natural_food_store
- grocery
- bodega_or_convenience
- farmers_market
- farmstand
- seasonal_market
- unknown

A chain does not force one format across all branches. Store-level evidence wins.

### Departments

The first controlled department set includes produce, meat, butcher counter, seafood, seafood counter, dairy, bakery, deli, prepared food, frozen, bulk foods, beer, wine, household, personal care, and pharmacy. Each value is `confirmed`, `expected`, `absent`, or `unknown`.

`absent` requires direct evidence. Lack of evidence is `unknown`, never `absent`.

### Clean sources and precedence

1. Existing New York/NYC open records for identity and location
2. OpenStreetMap public tags for shop type and explicit departments/features
3. USDA SNAP retailer list for SNAP authorization and retailer classification
4. Public, unauthenticated government or openly licensed directories
5. Maintained chain-format rules for broad defaults, recorded as inference rather than source fact

"Chain format knowledge" is encoded as a reviewed rule with date and rationale, not free-form model memory. Example: a Korean supermarket may imply a high prior for Korean pantry items, but it does not confirm a seafood counter at a particular branch.

Every factual profile field has source URL/record ID, observed date, license/terms check, and confidence. Conflicts are retained for review; newer data does not silently erase stronger evidence.

## 3. Availability model

Availability is an item-location relationship, not a property of either item or store alone.

```json
{
  "item_id": "item.gochujang",
  "location_id": "nys-123",
  "status": "expected",
  "evidence_type": "format_inference",
  "evidence_ref": "rule.international_supermarket.korean_pantry",
  "observed_at": null,
  "valid_through": null,
  "confidence": "medium",
  "explanation": "Expected from Korean supermarket profile",
  "price_observations": []
}
```

### Public labels

- **Confirmed**: direct real-world evidence connects the item/category to that place, such as a user receipt, private shelf-tag evidence normalized into facts, a permitted public catalog record, a current market roster, or an openly licensed source.
- **Expected**: a versioned rule inferred from format, specialty, department, season, or vendor category.
- **Unknown**: no useful evidence. Unknown results are not returned as matches by default.
- **Previously confirmed**: direct evidence is outside its freshness window but remains useful historical context.

Never use "in stock" unless a permitted source explicitly proves current inventory.

### Evidence precedence

1. Current direct confirmation
2. Current category/vendor confirmation
3. Recent historical confirmation
4. Store-specific department inference
5. Chain/format/specialty inference

Direct evidence may override an inference. Contradictions enter a review queue instead of being averaged away.

### Expected-match rules

Rules are data, not hidden code:

```json
{
  "id": "rule.international_supermarket.korean_pantry",
  "when": {"format":"international_supermarket","specialties_any":["korean"]},
  "items_or_categories": ["item.gochujang","category.korean_pantry"],
  "confidence": "medium",
  "explanation_template": "Expected from {specialty} supermarket profile",
  "version": 1,
  "reviewed_at": "YYYY-MM-DD"
}
```

Rules should prefer category coverage over long unsupported SKU lists. Negative rules are rare and require evidence; a bodega profile should usually produce low/unknown confidence for specialty items, not assert absence.

### Freshness

- receipts and shelf observations: confirmed on the observation date, then previously confirmed after a configurable window
- market rosters: valid for the published market season or roster date
- permitted catalogs: valid while the source record remains current
- store-profile expectations: re-evaluated whenever the profile or rule version changes

The UI shows the date and evidence type for confirmed matches and the reasoning for expected matches.

## 4. Price-ready schema, price work parked

Prices attach to the same item-location relation:

```json
{
  "price_observations": [{
    "amount": 4.99,
    "currency": "USD",
    "package_quantity": 16,
    "package_unit": "oz",
    "unit_price": 0.3119,
    "unit_basis": "oz",
    "price_type": "receipt_paid",
    "conditions": null,
    "observed_at": "YYYY-MM-DD",
    "valid_through": null,
    "source_ref": "..."
  }]
}
```

This array remains empty in the index-first build except for already valid observations. Search and availability must not depend on it. Later price code can aggregate observations without changing item IDs, location IDs, or availability evidence.

No study-based estimate or BLS prior is added in this slice. The prior price scope in `SPEC.md` stays parked for later review.

## 5. Search UX for item discovery

### Search behavior

The search box resolves:

- canonical items
- aliases and common misspellings
- brands linked to generic needs
- categories and dietary/specialty tags
- stores and markets

Autocomplete groups suggestions by Items, Categories, Brands, and Places. An item selection opens item-discovery results rather than inserting an opaque string filter.

### Result hierarchy

For an item query:

1. Confirmed matches, newest/strongest evidence first
2. Expected matches, ranked by confidence and proximity
3. Previously confirmed matches, clearly dated

Each card answers:

- where is it?
- confirmed, expected, or previously confirmed?
- why is this result shown?
- how fresh is the evidence?
- what store format/departments are relevant?

Example:

```text
H Mart - East Village
Expected · medium confidence
Expected from Korean supermarket profile
International supermarket · Korean/East Asian · seafood counter confirmed
```

### Filters

- evidence: confirmed / expected / previously confirmed
- distance or neighborhood
- store format
- department
- specialty/cuisine
- open/seasonal status when supported
- SNAP authorized

Map pins visually distinguish confirmed from expected results. Result counts show both totals, for example "3 confirmed · 12 expected."

### Coverage dashboard

The index reports its limits:

- locations profiled / 366
- profiles by confidence and format
- taxonomy items by category
- items with at least one confirmed match
- items with expected matches only
- stale confirmations
- unknown/ambiguous store profiles
- source freshness and failed/stopped source checks

No percentage is described as assortment coverage unless the denominator is defensible.

### Empty and weak states

- No confirmed results: "No confirmed locations yet. Showing places where this item is expected based on store type."
- No expected results: offer category/alias corrections and nearby specialty formats, not invented matches.
- Ambiguous query: ask the user to select the form, such as fresh vs dried or generic vs brand.

## 6. Build artifacts

Planned files after review:

```text
data/normalized/items.json
data/normalized/store_profiles.json
data/normalized/availability.json
data/normalized/availability_rules.json
schemas/item.schema.json
schemas/store_profile.schema.json
schemas/availability.schema.json
docs/taxonomy.md
docs/store-profile-sources.md
public/data/item_search_index.json
```

The existing `locations.json` remains the location spine during migration. IDs must be stable and redirects recorded if records merge.

## 7. Validation and review gates

A build fails when:

- an item lacks a primary category or stable ID
- aliases collide across incompatible items without a disambiguation rule
- a profile factual field lacks provenance
- `absent` is inferred from missing evidence
- an expected availability lacks a versioned rule and explanation
- a confirmed availability lacks direct evidence and a date/window
- retailer-site data enters from an unapproved or blocked source
- marketing text or source images enter normalized public data
- price estimates appear in the index-first output

Manual review queues cover ambiguous chains/formats, conflicting departments, low-confidence taxonomy matches, and rule changes that alter many results.

## 8. Acceptance criteria

The slice is ready when:

- all 366 locations have a profile, including explicit `unknown` fields where evidence is missing
- 400-600 reviewed taxonomy entries search by canonical name and alias
- every returned item-location match is labeled confirmed, expected, or previously confirmed
- every expected match exposes its rule/explanation
- every confirmed match exposes evidence type and date
- mobile autocomplete and Map/List views work for item searches
- coverage dashboard numbers reconcile with built files
- no price-layer prior, model, ranking, or new price collection is present
- source/collector legal controls from `SPEC.md` remain enforced

## 9. Review decisions before implementation

The user should review:

1. initial taxonomy breadth and category names
2. whether household/personal care belongs in the grocery index
3. expected-match confidence thresholds and freshness windows
4. which specialty/cuisine tags matter first
5. whether SNAP authorization belongs in the first UI release
6. whether expected results appear by default or behind a toggle

No build beyond this specification starts until that review is complete.
