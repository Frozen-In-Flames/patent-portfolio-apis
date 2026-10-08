# Patent Portfolio APIs

Turn **any inventor's USPTO patent portfolio** into live REST APIs — one API
per patent — plus a **portfolio-wide ontology summary** (key concepts, CPC
technology taxonomy, knowledge graph, technology clusters).

Built for inventors who already hold USPTO patents and want their portfolio
to be machine-readable: license it, search it, plug it into products.

## What it does

Given USPTO patent numbers (or an inventor name), it:

1. **Fetches** each patent's full record from the USPTO Patent Public Search
   API — title, abstract, numbered claims, description, inventors, assignees,
   CPC/IPC classifications, backward citations, family data. No API key needed.
2. **Generates a runnable FastAPI server** where every patent is its own API:
   - `GET /api/v1/patents/{number}` — full record (the patent's API root)
   - `GET /api/v1/patents/{number}/claims|abstract|description|citations|classifications|parties`
   - `GET /api/v1/portfolio/ontology` — concepts, CPC taxonomy, knowledge graph
   - `GET /api/v1/portfolio/ontology/summary` — human-readable summary
   - `GET /api/v1/search?q=...` — full-text search across the portfolio
   - Interactive docs at `/docs`, a browse UI at `/`, OpenAPI spec included.
3. **Summarizes the portfolio ontology**: TF-IDF concept extraction over
   claims/abstracts (with acronym expansion, e.g. LADAR → laser detection and
   ranging), CPC section/class/subclass taxonomy, a patent–concept–citation
   knowledge graph, and technology-domain clustering — rendered as
   `ONTOLOGY.md`, `ontology.html`, and `ontology.json`.

## Quick start

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt

# Build from patent numbers
.venv/bin/python cli.py build 10000000 4683202 --out ./my-portfolio --title "My Portfolio"

# Build from an inventor search
.venv/bin/python cli.py build --inventor "Mullis" --limit 10 --out ./mullis

# Offline demo (no network)
.venv/bin/python cli.py build --fixtures --out ./demo

# Serve it
.venv/bin/python cli.py serve ./my-portfolio --port 8000
# open http://127.0.0.1:8000  — UI, /docs — interactive API
```

## M&A portfolio merging (v0.2.0)

Build two portfolios, then merge them to see overlap, redundancies, and gaps —
the technical half of patent due diligence when two firms combine:

```bash
.venv/bin/python cli.py build 10000000 12748198 --out ./optics-co --title "OpticsCo"
.venv/bin/python cli.py build 12754414 12748194 --out ./photonix --title "Photonix"
.venv/bin/python cli.py merge ./optics-co ./photonix --out ./merged --title "OpticsCo + Photonix"
.venv/bin/python cli.py serve ./merged
```

The merge produces:

- `MERGER.md` — shared concepts, most redundant cross-portfolio patent pairs
  (ranked), and concepts unique to each side
- `/api/v1/merge/summary` — overlap counts and shared CPC classes
- `/api/v1/merge/concept-overlap` — every concept held by both sides
- `/api/v1/merge/redundant-pairs` — patent pairs across the two portfolios,
  ranked by shared concepts and CPC classes
- `/api/v1/merge/gaps` — concepts and CPC classes unique to each side

## Layout

```
cli.py                  # build / serve commands
src/ppa/
  uspto.py              # USPTO Patent Public Search client (session + search + full doc)
  models.py             # normalized Patent record (claims, citations, CPC, parties)
  text.py               # HTML cleanup, claim splitting
  ontology.py           # concept extraction, CPC taxonomy, knowledge graph, summary
  api_gen.py            # FastAPI app + OpenAPI generator (each patent becomes endpoints)
  report.py             # Markdown + HTML ontology reports
tests/
  fixtures/             # three real USPTO patent documents (offline tests)
examples/demo-portfolio # generated example: server, spec, reports
```

## Tests

```bash
.venv/bin/python -m pytest tests/ -m "not live"   # offline suite
.venv/bin/python -m pytest tests/ -m live          # hits the live USPTO API
```

## Notes

- Data comes from the public USPTO Patent Public Search web API; behavior was
  verified against it in October 2026. If USPTO changes the API, `uspto.py`
  is the one file to update.
- Very old grants (pre-OCR, "TEXT NOT AVAILABLE") are included in the API
  with a note; the ontology skips their missing text.
- Generated servers are self-contained: `portfolio_api.py` +
  `portfolio_data.json` run anywhere with `fastapi` and `uvicorn`.
