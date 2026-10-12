---
title: Patent Portfolio APIs
emoji: 📜
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Patent Portfolio APIs — live demo

This Space runs a generated **patent portfolio API**: every USPTO patent in the
demo portfolio is its own REST API, plus portfolio-wide ontology endpoints.

**New in v0.2.0 — M&A portfolio merge demo.** This build compares two
3-patent LiDAR portfolios side by side: shared technical concepts, the most
redundant cross-portfolio patent pairs (ranked), and coverage gaps on each
side. This is the due-diligence workflow the tool is built for.

- Browse UI: `/`
- Interactive API docs: `/docs`
- Merge summary: `/api/v1/merge/summary`
- Shared concepts: `/api/v1/merge/concept-overlap`
- Redundant pairs: `/api/v1/merge/redundant-pairs`
- Coverage gaps: `/api/v1/merge/gaps`
- Example: `/api/v1/patents/10000000/claims`
- Ontology summary: `/api/v1/portfolio/ontology/summary`

Build your own portfolio from the source (no API key needed — it reads the
public USPTO Patent Public Search API):

**GitHub:** https://github.com/Frozen-In-Flames/patent-portfolio-apis

```bash
python cli.py build 10000000 4683202 --out ./my-portfolio
python cli.py serve ./my-portfolio
```
