"""Live USPTO test — run with:  pytest -m live"""
import pytest

from ppa.models import from_ppubs
from ppa.uspto import PPUBSClient

pytestmark = pytest.mark.live


def test_fetch_patent_live():
    client = PPUBSClient()
    try:
        doc = client.fetch_patent("10000000")
    finally:
        client.close()
    p = from_ppubs(doc)
    assert p.number == "10000000"
    assert "LADAR" in p.title
    assert len(p.claims) == 20
