"""Regenerate sample-data.js from slots.csv so the double-click (file://) fallback matches the real data.
Browsers block fetch('slots.csv') over file://, so the embedded sample-data.js is what shows on double-click.
Run from the boatshed-model folder after editing slots.csv:  python embed_slots.py
"""
import csv, json, os

d = os.path.dirname(os.path.abspath(__file__))

def rackpos(num):
    num = int(num); odd = num % 2 == 1
    if num <= 10: return 1, ((11 - num) if odd else (12 - num)) // 2
    if num <= 20: return 2, ((21 - num) if odd else (22 - num)) // 2
    return 3, ((num - 19) if odd else (num - 20)) // 2

HDR = {"bay id": "slot_id", "tier": "tier", "owner": "owner", "boat name": "boat_name",
       "boat class": "boat_class", "boat no": "boat_no", "status": "status",
       "racing": "racing", "notes": "notes"}

rows = []
with open(os.path.join(d, "slots.csv"), newline="") as f:
    for raw in csv.DictReader(f):
        o = {}
        for k, v in raw.items():
            if k is None: continue
            o[HDR.get(k.strip().lower(), k.strip().lower())] = (v or "").strip()
        o["status"] = o.get("status", "").lower()
        r, p = rackpos(o["slot_id"]); o["rack"] = r; o["pos"] = p
        rows.append({k: o.get(k, "") for k in
                     ["slot_id", "rack", "pos", "tier", "owner", "boat_name",
                      "boat_class", "boat_no", "status", "racing", "notes"]})

with open(os.path.join(d, "sample-data.js"), "w") as f:
    f.write("window.SAMPLE_SLOTS = [\n")
    f.write(",\n".join(json.dumps(r) for r in rows))
    f.write("\n];\n")

print(f"sample-data.js: {len(rows)} slots regenerated from slots.csv")
