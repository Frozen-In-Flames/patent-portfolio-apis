import json
import os

import pytest

from ppa.models import from_ppubs

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def load(num):
    with open(os.path.join(FIX, f"fixture_{num}.json")) as fh:
        return from_ppubs(json.load(fh))


def test_ladar_patent_fields():
    p = load("10000000")
    assert p.number == "10000000"
    assert "LADAR" in p.title
    assert p.grant_date == "2018-06-19"
    assert p.filing_date == "2015-03-10"
    assert p.assignees == ["Raytheon Company"]
    assert p.inventors == ["Joseph Marron"]
    assert p.claim_count == 20
    assert len(p.claims) == 20
    assert p.claims[0]["number"] == 1
    assert "laser detection and ranging" in p.claims[0]["text"].lower()
    assert "G01S7/4865" in p.cpc_inventive
    assert p.abstract, "abstract must be non-empty"
    assert len(p.description) > 1000


def test_citations_parsed():
    p = load("10000000")
    assert len(p.citations) >= 3
    c0 = p.citations[0]
    assert c0.number == "5093563", c0
    assert c0.cited_by == "examiner"
    assert c0.country == "US"


def test_all_fixtures_parse():
    for num in ["10000000", "8725472", "4683202"]:
        p = load(num)
        assert p.number == num
        assert p.title
        assert p.claims
        assert p.to_dict()["number"] == num
