import json
import os

import pytest

fastapi_testclient = pytest.importorskip("fastapi.testclient")

from ppa import api_gen, ontology
from ppa.models import from_ppubs

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def build_data():
    patents = []
    for num in ["10000000", "8725472", "4683202"]:
        with open(os.path.join(FIX, f"fixture_{num}.json")) as fh:
            patents.append(from_ppubs(json.load(fh)))
    onto = ontology.build_ontology(patents)
    return {
        "meta": {"title": "Test Portfolio", "version": "0.1.0",
                 "patent_count": len(patents),
                 "numbers": [p.number for p in patents]},
        "patents": [p.to_dict() for p in patents],
        "ontology": onto,
    }


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    out = str(tmp_path_factory.mktemp("portfolio"))
    paths = api_gen.generate(out, build_data())
    assert os.path.exists(paths["openapi"])
    from fastapi.testclient import TestClient
    import importlib.util
    spec = importlib.util.spec_from_file_location("portfolio_api_test",
                                                  paths["app"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return TestClient(module.app)


def test_portfolio_root(client):
    r = client.get("/api/v1/portfolio")
    assert r.status_code == 200
    assert len(r.json()["patents"]) == 3


def test_patent_endpoints(client):
    for endpoint in ["", "/claims", "/abstract", "/citations",
                     "/classifications", "/parties"]:
        r = client.get(f"/api/v1/patents/10000000{endpoint}")
        assert r.status_code == 200, endpoint
    r = client.get("/api/v1/patents/10000000/claims")
    assert r.json()["claim_count"] == 20
    r = client.get("/api/v1/patents/99999999")
    assert r.status_code == 404


def test_ontology_endpoints(client):
    r = client.get("/api/v1/portfolio/ontology/summary")
    assert r.status_code == 200
    assert r.json()["portfolio_size"] == 3
    r = client.get("/api/v1/portfolio/ontology/concepts?limit=5")
    assert len(r.json()) == 5


def test_search(client):
    r = client.get("/api/v1/search", params={"q": "ladar"})
    assert r.status_code == 200
    assert any(h["number"] == "10000000" for h in r.json())
