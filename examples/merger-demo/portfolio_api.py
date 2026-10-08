"""Generated Patent Portfolio API — do not edit by hand.

Regenerate with:  python cli.py build <patent numbers> --out <dir>
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "portfolio_data.json")) as fh:
    DATA: Dict[str, Any] = json.load(fh)

PATENTS: Dict[str, Dict[str, Any]] = {p["number"]: p for p in DATA["patents"]}
ONTOLOGY: Dict[str, Any] = DATA["ontology"]

app = FastAPI(
    title=DATA["meta"]["title"],
    description="Per-patent REST APIs plus portfolio ontology for a USPTO patent portfolio.",
    version=DATA["meta"]["version"],
)


def _patent_or_404(number: str) -> Dict[str, Any]:
    p = PATENTS.get(number)
    if not p:
        raise HTTPException(status_code=404, detail=f"patent {{number}} not in portfolio")
    return p


@app.get("/api/v1/portfolio", tags=["portfolio"])
def get_portfolio() -> Dict[str, Any]:
    """Portfolio metadata and patent list."""
    return {"meta": DATA["meta"],
            "patents": [{"number": p["number"], "title": p["title"],
                         "grant_date": p["grant_date"],
                         "assignees": p["assignees"]} for p in DATA["patents"]]}


@app.get("/api/v1/patents", tags=["patents"])
def list_patents() -> List[Dict[str, Any]]:
    """List every patent in the portfolio (full records)."""
    return DATA["patents"]


@app.get("/api/v1/patents/{number}", tags=["patents"])
def get_patent(number: str) -> Dict[str, Any]:
    """Full record for one patent — its API root."""
    return _patent_or_404(number)


@app.get("/api/v1/patents/{number}/claims", tags=["patents"])
def get_claims(number: str) -> Dict[str, Any]:
    p = _patent_or_404(number)
    return {"number": number, "claim_count": p["claim_count"], "claims": p["claims"]}


@app.get("/api/v1/patents/{number}/abstract", tags=["patents"])
def get_abstract(number: str) -> Dict[str, str]:
    p = _patent_or_404(number)
    return {"number": number, "abstract": p["abstract"]}


@app.get("/api/v1/patents/{number}/description", tags=["patents"])
def get_description(number: str) -> Dict[str, str]:
    p = _patent_or_404(number)
    return {"number": number, "description": p["description"]}


@app.get("/api/v1/patents/{number}/citations", tags=["patents"])
def get_citations(number: str) -> Dict[str, Any]:
    p = _patent_or_404(number)
    return {"number": number, "citations": p["citations"],
            "foreign_citations": p["foreign_citations"]}


@app.get("/api/v1/patents/{number}/classifications", tags=["patents"])
def get_classifications(number: str) -> Dict[str, Any]:
    p = _patent_or_404(number)
    return {"number": number, "cpc_inventive": p["cpc_inventive"],
            "cpc_additional": p["cpc_additional"], "ipc": p["ipc"],
            "us_classes": p["us_classes"]}


@app.get("/api/v1/patents/{number}/parties", tags=["patents"])
def get_parties(number: str) -> Dict[str, Any]:
    p = _patent_or_404(number)
    return {"number": number, "inventors": p["inventors"],
            "assignees": p["assignees"], "applicants": p["applicants"],
            "examiner": p["examiner"]}


@app.get("/api/v1/portfolio/ontology", tags=["ontology"])
def get_ontology() -> Dict[str, Any]:
    """Full portfolio ontology: concepts, CPC taxonomy, knowledge graph."""
    return ONTOLOGY


@app.get("/api/v1/portfolio/ontology/summary", tags=["ontology"])
def get_ontology_summary() -> Dict[str, Any]:
    """Human-readable summary of the portfolio ontology."""
    return ONTOLOGY["summary"]


@app.get("/api/v1/portfolio/ontology/concepts", tags=["ontology"])
def list_concepts(limit: int = Query(30, ge=1, le=500)) -> List[Dict[str, Any]]:
    return ONTOLOGY["concepts"][:limit]


@app.get("/api/v1/search", tags=["portfolio"])
def search(q: str = Query(..., min_length=2)) -> List[Dict[str, Any]]:
    """Full-text search across the portfolio (title, abstract, claims)."""
    needle = q.lower()
    hits = []
    for p in DATA["patents"]:
        hay = " ".join([p["title"], p["abstract"]] +
                       [c["text"] for c in p["claims"]]).lower()
        if needle in hay:
            hits.append({"number": p["number"], "title": p["title"]})
    return hits


@app.get("/api/v1/merge/summary", tags=["merge"])
def merge_summary() -> Dict[str, Any]:
    """M&A comparison summary (only present on merged portfolios)."""
    m = DATA.get("merge")
    if not m:
        raise HTTPException(status_code=404, detail="not a merged portfolio")
    return {"a": m["a"], "b": m["b"],
            "overlap_concept_count": m["overlap_concept_count"],
            "unique_a_count": m["unique_a_count"],
            "unique_b_count": m["unique_b_count"],
            "cpc_overlap": m["cpc_overlap"]}


@app.get("/api/v1/merge/concept-overlap", tags=["merge"])
def merge_concept_overlap() -> List[Dict[str, Any]]:
    m = DATA.get("merge")
    if not m:
        raise HTTPException(status_code=404, detail="not a merged portfolio")
    return m["concept_overlap"]


@app.get("/api/v1/merge/redundant-pairs", tags=["merge"])
def merge_redundant_pairs(limit: int = Query(10, ge=1, le=25)) -> List[Dict[str, Any]]:
    m = DATA.get("merge")
    if not m:
        raise HTTPException(status_code=404, detail="not a merged portfolio")
    return m["redundant_pairs"][:limit]


@app.get("/api/v1/merge/gaps", tags=["merge"])
def merge_gaps() -> Dict[str, Any]:
    """Concepts and CPC classes unique to each side."""
    m = DATA.get("merge")
    if not m:
        raise HTTPException(status_code=404, detail="not a merged portfolio")
    return {"unique_to_a": m["concepts_unique_to_a"],
            "unique_to_b": m["concepts_unique_to_b"],
            "cpc_unique_to_a": m["cpc_unique_to_a"],
            "cpc_unique_to_b": m["cpc_unique_to_b"]}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index() -> str:
    path = os.path.join(HERE, "index.html")
    with open(path) as fh:
        return fh.read()
