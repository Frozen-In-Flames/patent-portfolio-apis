import json
import os

import pytest

from ppa import api_gen, merge, ontology
from ppa.models import from_ppubs, patent_from_dict

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def portfolio_data(numbers, title):
    patents = []
    for num in numbers:
        with open(os.path.join(FIX, f"fixture_{num}.json")) as fh:
            patents.append(from_ppubs(json.load(fh)))
    onto = ontology.build_ontology(patents)
    return {
        "meta": {"title": title, "version": "0.2.0",
                 "patent_count": len(patents),
                 "numbers": [p.number for p in patents]},
        "patents": [p.to_dict() for p in patents],
        "ontology": onto,
    }


def test_compare_structure():
    da = portfolio_data(["10000000"], "OpticsCo")
    db = portfolio_data(["8725472", "4683202"], "BioTech")
    c = merge.compare(da, db)
    assert c["a"]["title"] == "OpticsCo"
    assert c["b"]["patent_count"] == 2
    assert isinstance(c["concept_overlap"], list)
    assert isinstance(c["redundant_pairs"], list)
    # every overlap entry names patents on both sides
    for o in c["concept_overlap"]:
        assert o["a_patents"] and o["b_patents"]


def test_patent_from_dict_roundtrip():
    da = portfolio_data(["10000000"], "X")
    p = patent_from_dict(da["patents"][0])
    assert p.number == "10000000"
    assert p.claim_count == 20
    assert p.citations and p.citations[0].number == "5093563"
    assert "G01S7/4865" in p.cpc_inventive


def test_merge_endpoints(tmp_path):
    da = portfolio_data(["10000000"], "OpticsCo")
    db = portfolio_data(["8725472", "4683202"], "BioTech")
    comparison = merge.compare(da, db)
    patents = da["patents"] + db["patents"]
    objs = [patent_from_dict(p) for p in patents]
    data = {
        "meta": {"title": "Merged", "version": "0.2.0",
                 "patent_count": len(patents),
                 "numbers": [p["number"] for p in patents],
                 "merged_from": ["OpticsCo", "BioTech"]},
        "patents": patents,
        "ontology": ontology.build_ontology(objs),
        "merge": comparison,
    }
    out = str(tmp_path / "merged")
    api_gen.generate(out, data)
    assert os.path.exists(os.path.join(out, "portfolio_api.py"))

    from fastapi.testclient import TestClient
    import importlib.util
    spec = importlib.util.spec_from_file_location("portfolio_api_merge",
                                                  os.path.join(out, "portfolio_api.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    client = TestClient(module.app)
    r = client.get("/api/v1/merge/summary")
    assert r.status_code == 200
    assert r.json()["a"]["title"] == "OpticsCo"
    for ep in ["/api/v1/merge/concept-overlap",
               "/api/v1/merge/redundant-pairs",
               "/api/v1/merge/gaps"]:
        assert client.get(ep).status_code == 200, ep
    # non-merged portfolio must 404 on merge endpoints
    out2 = str(tmp_path / "plain")
    api_gen.generate(out2, {"meta": data["meta"], "patents": data["patents"],
                            "ontology": data["ontology"]})
    spec2 = importlib.util.spec_from_file_location(
        "portfolio_api_plain", os.path.join(out2, "portfolio_api.py"))
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)
    assert TestClient(mod2.app).get("/api/v1/merge/summary").status_code == 404
