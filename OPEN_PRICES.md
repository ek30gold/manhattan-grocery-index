# Open Prices read-back policy

Open Prices is an optional read-only source for this index. No Open Prices contribution account or proof upload is part of the default pipeline.

## License and publication

Open Prices data is licensed under the Open Database License (ODbL). Any build containing an Open Prices record must:

- credit "Open Prices contributors" and link to https://prices.openfoodfacts.org/
- retain the exact Open Prices record/proof/location identifier and retrieval date
- mark its source and evidence type explicitly; never relabel it as a first-party store price
- publish the adapted public database under ODbL and make the machine-readable data available
- include only other source data that may legally be redistributed in that open database
- keep Open Prices proof images out of this repository and UI; link to proof where permitted rather than copying it

The public repository is the machine-readable share-alike distribution. A release containing Open Prices data must include an ODbL notice alongside the generated data and must not combine it with restricted chain-site data.

## Safe read path

Use only Open Prices' documented public read API or published dumps:

- API docs: https://prices.openfoodfacts.org/api/docs
- data access: https://openfoodfacts.github.io/open-prices/guides/data/

Record terms/license check date, endpoint, response status, retrieval time, parser version and source record IDs in the manifest. Follow published rate guidance and the project's normal stop-on-block behavior. Read access must remain anonymous; endpoints that require authentication are out of scope.

## Contribution is a separate decision

Open Prices requires an Open Food Facts account to contribute. Receipt contribution also uploads a proof photo under CC BY-SA 4.0. That conflicts with this project's default no-account rule and private-image intake. Do not create an account or upload a receipt unless the user makes a case-specific exception after reviewing both points. If approved, redact personal information before upload and record the user's exact scope.
