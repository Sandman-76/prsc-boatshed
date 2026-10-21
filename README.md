# PRSC Boat Shed — interactive model (proof-of-concept)

Interactive 3D + top-down model of the member boat storage shed. Each storage slot
is clickable and shows the assigned owner/boat, pulled from a separate editable file.
Runs in any web browser — **no CAD software needed**.

## How to view
- **Double-click `index.html`** → opens in your browser with the built-in sample data.
  Drag to orbit, scroll to zoom, click a slot. "Plan view" gives a top-down layout.
- Works fully offline (three.js is bundled in `lib/`; the GLB boat hulls are embedded in
  `models.js` as base64, so they show even on `file://` double-click — browsers block loading
  `.glb` files directly over `file://`, which is why embedding is required).

## The data file (assign owners here)
Owners live in **`slots.csv`** — open it in Excel/Sheets. Columns:

| column | meaning |
|---|---|
| `slot_id` | the painted slot number/ID |
| `rack` | which rack, `1`–`3` (front-to-back finger racks) |
| `pos` | position along the rack, `1` = back/marina end → front/door end |
| `tier` | `lower` or `upper` |
| `owner`, `boat_name`, `boat_class`, `boat_no`, `notes` | free text |
| `racing` | `Y` / `N` (shown in the info panel) |
| `status` | `Paid` / `Club` / `Unknown` / `vacant` / `NA` (sets the colour) |

Status meanings:
- **Paid** (green), **Club** boat (blue), **Unknown** (amber) → bay holds a boat (hull shown).
- **vacant** (grey) → empty bay, available.
- **NA** → bay is **not available in the current rack configuration** (e.g. neighbouring
  classes are wider than the painted bay). Rendered with **diagonal yellow/black hazard stripes**,
  no boat.

The real data uses the schema `Bay Id,Tier,Owner,Boat Name,Boat Class,Boat No,Status,Racing,Notes`;
`rack`/`pos` are derived automatically from `Bay Id` (headers are case/spacing-insensitive).
`boat_class` **Other** (or left blank on an occupied bay) draws a generic default hull/colour.

After editing, open `index.html`, click **Load slots.csv**, pick your file.
(If you serve the folder over http, it loads `slots.csv` automatically.)

### Class metadata — `classes.csv`
A second file holds per-class info, linked to `slots.csv` by the `boat_class` value:

| class | display_name | colour | notes |
|---|---|---|---|
| Sabre | Sabre | `#4e79a7` | … |
| Optimist | Optimist | `#76b7b2` | … |
| Other | Other | `#8a8f98` | default for unknown classes |

- `display_name` shows in the click-info panel; `colour` is the hull colour in **Class** mode.
- The **Colour: Status / Class** toggle (top-right) switches between status colours (Paid/Club/Unknown/…)
  and these class colours; the legend updates to match.
- Loaded automatically when served, or via **Load classes.csv**. Built-in defaults exist for the known
  classes, so it's optional. (Keeping `slots` and `classes` as two tabs in one Excel file, each exported
  to CSV, works fine — the app reads them as separate CSVs.)

## Shed orientation & layout (confirmed with the club)
- **North** = along the long axis, toward the **rear/far end** (model +X). A red ground
  north-arrow shows this and rotates with the model.
- **East = road** (George Robertson Dr) = model +Z. **2 roller doors on the east wall:
  Door 1 is the main boat door; Door 2 is NOT used for sailing boats** (access/other).
  **West = marina/water** (−Z). Each rack has a `bow` direction in `RACKS` (R3 bows north toward Door 1).
- **Rack layout (confirmed from the club's marked plan):** an **L of racks + a middle cross-rack**,
  all **2-tier, same depth**, boats stored **side-by-side across the depth, bows facing out**:
  - **R1** — rear rack along the **North wall**, runs **E–W**
  - **R2** — side rack along the **West/marina wall**, runs **N–S** (northern half)
  - **R3** — **middle** cross-rack, runs **E–W**
  Rack geometry is the `RACKS` array in `index.html` (`axis`, centre `x/z`, `half`-length, `n` slots/tier).
- **Slot numbers (confirmed, 32 slots):** lower tier = odd, upper = even. **R1 = 1–10** (1/2 at the
  NE corner → west), **R2 = 11–20** (north → south), **R3 = 21–32** (west → east). `slot_id` in
  `slots.csv` holds the real number. Still to fill: `owner` / `boat_name` / `boat_class` per slot.
- **Photo reference point:** photographer stands at the road-side front, shooting toward the
  far/rear corner.

## Tuning the building
Dimensions are at the top of `index.html` in the `DIMS` block (metres):
footprint **23.5 × 15.4**, eaves **3.8**, ridge **4.6**, **8** bays/side, 2 tiers.
Edit and reload to match reality.

## Status: proof-of-concept — still approximate
- **Slot IDs + owners are sample data** — replace with the real painted numbers and members.
- **Layout is inferred** (8 bays/side, bow-in both walls). Needs the real bay count/arrangement.
- **Heights estimated** from street view.
- **Plan view** currently overlaps the two tiers (upper hides lower) — can be split.

## Boat hulls
Each occupied slot shows a hull coloured by status. By class:
- **Real GLB hulls** (`models/`): **Sabre, Pacer, Laser, Opti, Fireball, Impulse** — loaded from `models/<class>.glb`.
- **Procedural hulls**: every other class (Heron, Mirror, Sabot, …) is generated to its
  class length/beam from the `CLASS_DIMS` table in `index.html`.

Per-class source & accuracy:
- **Pacer, Impulse** — official class-rules offset tables → accurate.
- **Laser, Opti** — supplied 3D models (rig/foils stripped, scaled to class) → accurate.
- **Fireball** — profile + dims from a WoodenBoat article → good approximation (snub bow captured).
- **Sabre** — build manual only (no offsets) → approximation.

To add a real hull for another class: drop `models/<name>.glb` in and add one line to
`CLASS_GLB` in `index.html` (`ClassName:'models/<name>.glb'`). The shed auto-recolours it
by status, orients it bow-out, and fits it to the slot — the GLB's own colours/textures are ignored.

GLB accuracy depends on the source: a class **measurement-rules offset table** (Pacer) or a
**3D model** (Laser, Opti) gives an accurate hull; a build manual or spec sheet (Sabre, Heron)
gives only an approximation.

## Files
- `index.html` — the app (open this)
- `slots.csv` — editable owner/slot data
- `sample-data.js` — built-in fallback data so it works on double-click
- `lib/three.min.js`, `lib/GLTFLoader.js` — 3D engine + GLB loader (bundled, r128)
- `models/*.glb` — per-class hull models (source files; used when served over http)
- `models.js` — the same GLB hulls embedded as base64 so double-click (`file://`) works.
  **Regenerate after changing any `.glb`:** `python embed_glb.py` (base64-encodes `models/*.glb`).
- `glb-viewer.html` — standalone viewer for a single GLB (`?m=models/pacer.glb`)
