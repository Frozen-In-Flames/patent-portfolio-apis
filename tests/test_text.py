from ppa.models import from_ppubs
from ppa.text import split_claims, strip_html


def test_subscript_markup_cleaned():
    assert strip_html("CO.SUB.2 .refrigeration") == "CO2 .refrigeration"
    assert strip_html("H.SUP.2 .O") == "H2 .O"


def test_br_separates_claims():
    html = "1. First claim text.<br>2. Second claim text.<br>3. Third."
    claims = split_claims(html)
    assert [n for n, _ in claims] == [1, 2, 3]
    assert claims[1][1] == "Second claim text."


def test_text_not_available_title():
    p = from_ppubs({"publicationReferenceDocumentNumber": "1128416",
                    "inventionTitle": "TEXT NOT AVAILABLE"})
    assert p.title == ""
    assert p.number == "1128416"
