# User-supplied price intake

This is the clean intake path for newsletters the user personally receives and circular/receipt photos the user sends.

## Workflow

1. Keep the original email or image private. Do not commit it or a retrievable image URL.
2. Read only factual fields: store, address, item, brand, size, price, conditions, validity dates and observed date. Discard descriptions, slogans, photos and layout.
3. Create a JSON intake file using the format below. `evidence_ref` is a private message/attachment ID used only to derive a non-reversible public fingerprint.
4. Validate with `python3 intake.py intake.json --check`.
5. Merge with `python3 intake.py intake.json --locations locations.json`.
6. Review the diff. Confirm the store match, every fact against the private evidence, no image/copy entered the repository, and validity/conditions are accurate. Then commit the changed `locations.json`.

```json
{
  "source_type": "receipt",
  "evidence_ref": "private-message-or-attachment-id",
  "store": {"name": "55 FULTON MARKET", "address": "55 Fulton St, New York, NY 10038"},
  "offers": [{
    "product": "Hass avocados",
    "brand": "",
    "size": "each",
    "price": 0.99,
    "currency": "USD",
    "unit": "each",
    "conditions": "",
    "valid_from": "",
    "valid_through": "",
    "observed": "2026-09-15",
    "evidence_type": "receipt_paid"
  }]
}
```

`source_type` is `receipt`, `mailer`, or `newsletter`. Receipts require `receipt_paid`; mailers and newsletters require `advertised_sale`. A failed validation or ambiguous store match stops the import. Missing fields stay missing; never infer price, size, dates, location or conditions.
