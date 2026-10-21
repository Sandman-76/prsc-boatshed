# Deploying the boat-shed model to a website

The app is **static files** (HTML + JS + GLB models). It's hosted on **GitHub Pages**, the
**member data lives in a Google Sheet**, and the club website shows it with a one-line `<iframe>`.

```
 Club website  ──<iframe …?data=SHEET_CSV>──►  GitHub Pages (app + models)  ──fetch──►  Google Sheet (CSV)
  (unlisted)                                      (public repo, no names)                 (real member data)
```

**Privacy:** the public repo contains **no member names and no link to them**. The real data,
and the link to it, exist only in the Google Sheet and in the club-page embed (both unlisted).

---

## 1. Google Sheet (the data)

1. Create a new Google Sheet. Make **two tabs**, named exactly **`slots`** and **`classes`**.
2. **`slots` tab** — first row must be these headers (copy from `slots.csv`):
   `Bay Id, Tier, Owner, Boat Name, Boat Class, Boat No, Status, Racing, Notes`
   Paste the real member data beneath (your copy is at `..\_boatshed-real-slots.csv`).
3. **`classes` tab** — headers: `class, display_name, colour, notes` (copy from `classes.csv`).
4. Publish each tab as CSV: **File → Share → Publish to web**:
   - "Link" → choose the **`slots`** tab → **Comma-separated values (.csv)** → **Publish**. Copy the URL.
   - Repeat for the **`classes`** tab. Copy that URL.
   You now have two links like
   `https://docs.google.com/spreadsheets/d/e/2PACX-…/pub?gid=0&single=true&output=csv`.

*Status values:* `Paid`, `Club`, `Unknown`, `vacant`, `NA`. *Racing:* `Y`/`N`.
Editing the sheet updates the site on the next refresh (Google may cache a few minutes).

## 2. GitHub Pages (the app)

1. Create a **public** repo, e.g. `prsc-boatshed`.
2. Upload the **contents of this `boatshed-model` folder** (index.html, lib/, models/, models.js,
   sample-data.js, slots.csv, classes.csv, glb-viewer.html, README.md). The committed data is the
   anonymised template — that's intentional.
3. **Settings → Pages → Source: Deploy from a branch → `main` / root → Save.**
4. After ~1 minute your app is at **`https://sandman-76.github.io/prsc-boatshed/`**.

Opening that URL directly shows the **anonymised demo** (no real names) — that's expected; the real
data only appears when the `?data=` link is supplied by the club-page embed (next step).

## 3. Club website (the embed)

Add **one** of these to the admin page (both have the real Sheet links baked in and URL-encoded).
Use the iframe if the HTML block allows it; otherwise use the link.

Iframe:
```html
<iframe
  src="https://sandman-76.github.io/prsc-boatshed/?data=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2Fe%2F2PACX-1vRL-FgwE59vvsJx5S7ecXEb4AbVZNMAnQCLC0EqWQWbmR8UM3zjNshmCZNkfoD01g_dlpZ3ju7eT0zN%2Fpub%3Fgid%3D0%26single%3Dtrue%26output%3Dcsv&classes=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2Fe%2F2PACX-1vRL-FgwE59vvsJx5S7ecXEb4AbVZNMAnQCLC0EqWQWbmR8UM3zjNshmCZNkfoD01g_dlpZ3ju7eT0zN%2Fpub%3Fgid%3D396608392%26single%3Dtrue%26output%3Dcsv"
  style="width:100%;height:80vh;border:0" title="Boat storage register"></iframe>
```

Link (fallback if iframes are stripped):
```html
<a href="https://sandman-76.github.io/prsc-boatshed/?data=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2Fe%2F2PACX-1vRL-FgwE59vvsJx5S7ecXEb4AbVZNMAnQCLC0EqWQWbmR8UM3zjNshmCZNkfoD01g_dlpZ3ju7eT0zN%2Fpub%3Fgid%3D0%26single%3Dtrue%26output%3Dcsv&classes=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2Fe%2F2PACX-1vRL-FgwE59vvsJx5S7ecXEb4AbVZNMAnQCLC0EqWQWbmR8UM3zjNshmCZNkfoD01g_dlpZ3ju7eT0zN%2Fpub%3Fgid%3D396608392%26single%3Dtrue%26output%3Dcsv"
   target="_blank">▶ Open the boat-storage map</a>
```

That one tag is the only thing on the club site. Everything else lives on GitHub Pages + the Sheet.

---

## Updating things later
- **Owners / boats / status** → edit the **Google Sheet**. Nothing else.
- **Rack layout / colours / app behaviour** → edit files here, push to GitHub (Pages redeploys).
- **Changed a `.glb`** → run `python embed_glb.py` (refreshes `models.js`), then push.
- **Changed the template `slots.csv`** → run `python embed_slots.py` (refreshes `sample-data.js`), then push.

## Local / offline use
Double-click `index.html` — it runs with the anonymised sample data (GLBs are embedded in
`models.js`, so they work on `file://`). To view your real data locally, use the **Load slots.csv**
button and pick `..\_boatshed-real-slots.csv`.
