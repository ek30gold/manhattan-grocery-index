# Store profile sources and inference

All 366 profiles retain their public identity/location source from `locations.json`. Farmers-market SNAP facts come from the NYC public record already present in that file. Other SNAP values are `null` until a clean public match is available.

`rule.profile_name_v1` is a dated, versioned inference from operator names to broad format, chain, and the seven approved specialties. It is not direct evidence. Store departments are either `expected` from that broad format or `unknown`; this build never infers `absent`.

Source precedence and stop conditions remain those in `SPEC.md` and `INDEX_FIRST_SPEC.md`. No authenticated retailer source, blocked source, or private account data was added.
