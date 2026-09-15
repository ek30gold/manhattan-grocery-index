#!/usr/bin/env python3
"""Validate user-supplied receipt/circular facts and merge them into locations.json.

Input is JSON produced after a human/assistant reads a user-owned newsletter,
receipt, or circular image. Source images remain private and are never copied
into the public repository.
"""
import argparse, datetime as dt, hashlib, json, pathlib, sys

ALLOWED_SOURCE_TYPES = {"receipt", "mailer", "newsletter"}
ALLOWED_EVIDENCE_TYPES = {"receipt_paid", "advertised_sale"}
REQUIRED_OFFER = {"product", "price", "currency", "unit", "observed", "evidence_type"}

def fail(msg): raise ValueError(msg)
def date(s, field):
    try: return dt.date.fromisoformat(s)
    except Exception: fail(f"{field} must be YYYY-MM-DD")
def validate(doc):
    if doc.get("source_type") not in ALLOWED_SOURCE_TYPES: fail("source_type must be receipt, mailer, or newsletter")
    if not doc.get("store", {}).get("name") or not doc["store"].get("address"): fail("store name and address are required")
    if not doc.get("evidence_ref"): fail("private evidence_ref is required")
    if "image" in doc or "image_url" in doc or "marketing_copy" in doc: fail("images and marketing copy must not enter the public record")
    if not isinstance(doc.get("offers"), list) or not doc["offers"]: fail("at least one offer is required")
    seen=set()
    for i,o in enumerate(doc["offers"]):
        missing=REQUIRED_OFFER-set(o)
        if missing: fail(f"offer {i}: missing {', '.join(sorted(missing))}")
        if o["evidence_type"] not in ALLOWED_EVIDENCE_TYPES: fail(f"offer {i}: invalid evidence_type")
        if doc["source_type"]=="receipt" and o["evidence_type"]!="receipt_paid": fail(f"offer {i}: receipts require receipt_paid")
        if doc["source_type"] in {"mailer","newsletter"} and o["evidence_type"]!="advertised_sale": fail(f"offer {i}: circulars/newsletters require advertised_sale")
        if not isinstance(o["price"],(int,float)) or o["price"]<=0: fail(f"offer {i}: price must be positive")
        observed=date(o["observed"],f"offer {i} observed")
        if o.get("valid_from"): date(o["valid_from"],f"offer {i} valid_from")
        if o.get("valid_through"):
            end=date(o["valid_through"],f"offer {i} valid_through")
            if o.get("valid_from") and end<date(o["valid_from"],"valid_from"): fail(f"offer {i}: validity dates reversed")
        key=(o["product"].strip().lower(),o.get("brand",""),o.get("size",""),o["price"],o["observed"])
        if key in seen: fail(f"offer {i}: duplicate")
        seen.add(key)
    return doc

def store_match(stores, wanted):
    norm=lambda s:' '.join(s.lower().split())
    hits=[s for s in stores if norm(s.get("name",""))==norm(wanted["name"]) and norm(s.get("address",""))==norm(wanted["address"])]
    if len(hits)!=1: fail(f"store match must be unique; found {len(hits)}")
    return hits[0]

def merge(doc, locations):
    target=store_match(locations,doc["store"]); target.setdefault("offers",[])
    for o in doc["offers"]:
        clean={k:o[k] for k in ("product","brand","size","price","currency","unit","conditions","valid_from","valid_through","observed","evidence_type") if o.get(k) not in (None,"")}
        clean["source"]="user-supplied:"+doc["source_type"]+":"+hashlib.sha256(doc["evidence_ref"].encode()).hexdigest()[:12]
        clean["confidence"]="high" if doc["source_type"]=="receipt" else "medium"
        target["offers"].append(clean)
    return target["id"],len(doc["offers"])

def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("--locations",default="locations.json"); p.add_argument("--check",action="store_true"); a=p.parse_args()
    doc=validate(json.loads(pathlib.Path(a.input).read_text()))
    if a.check: print(f"valid: {len(doc['offers'])} offers"); return
    path=pathlib.Path(a.locations); locations=json.loads(path.read_text()); sid,n=merge(doc,locations)
    path.write_text(json.dumps(locations,indent=2)+"\n"); print(f"merged {n} offers into {sid}")
if __name__=="__main__":
    try: main()
    except (ValueError,KeyError,json.JSONDecodeError) as e: print(f"intake error: {e}",file=sys.stderr); raise SystemExit(2)
