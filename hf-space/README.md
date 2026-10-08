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

- Browse UI: `/`
- Interactive API docs: `/docs`
- Example: `/api/v1/patents/10000000/claims`
- Ontology summary: `/api/v1/portfolio/ontology/summary`

Build your own portfolio from the source (no API key needed — it reads the
public USPTO Patent Public Search API):

**GitHub:** https://github.com/AriesConsulting/patent-portfolio-apis

```bash
python cli.py build 10000000 4683202 --out ./my-portfolio
python cli.py serve ./my-portfolio
```
