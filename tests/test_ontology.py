import json
import os

import pytest

from ppa.models import from_ppubs
from ppa.ontology import (build_ontology, extract_acronyms, extract_concepts,
                          parse_cpc)

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def patents():
    out = []
    for num in ["10000000", "8725472", "4683202"]:
        with open(os.path.join(FIX, f"fixture_{num}.json")) as fh:
            out.append(from_ppubs(json.load(fh)))
    return out


def test_parse_cpc():
    p = parse_cpc("G01S7/4865")
    assert p["section"] == "G"
    assert p["class"] == "G01"
    assert p["subclass"] == "G01S"


def test_acronyms():
    ps = patents()
    texts = [p.claims[0]["text"] for p in ps if p.claims]
    acros = extract_acronyms(texts)
    assert acros.get("LADAR") == "laser detection and ranging"


def test_concepts_extracted():
    ps = patents()
    concepts = extract_concepts(ps)
    assert len(concepts) > 10
    labels = [c.label for c in concepts]
    assert any("ladar" in lb.lower() for lb in labels), labels[:15]
    # every concept references real patents
    for c in concepts[:10]:
        assert c.patents
        assert c.score > 0


def test_full_ontology():
    ps = patents()
    onto = build_ontology(ps)
    assert set(onto) == {"concepts", "cpc_taxonomy", "graph", "summary"}
    s = onto["summary"]
    assert s["portfolio_size"] == 3
    assert s["cpc_sections"], "CPC sections must be populated"
    assert s["top_concepts"]
    assert s["technology_domains"]
    assert len(onto["graph"]["nodes"]) > len(onto["graph"]["edges"]) // 4
    # JSON-serializable
    json.dumps(onto)
