#!/usr/bin/env python3
"""Patent Portfolio APIs — command line interface.

Build a portfolio from USPTO patent numbers (or an inventor search), turn
every patent into REST API endpoints, and summarize the portfolio ontology.

    python cli.py build 10000000 8725472 --out ./my-portfolio
    python cli.py build --inventor "Marron, Joseph" --limit 10 --out ./x
    python cli.py build --fixtures --out ./demo        # offline demo
    python cli.py serve ./my-portfolio --port 8000
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "src"))

from ppa import __version__  # noqa: E402
from ppa import api_gen, ontology, report  # noqa: E402
from ppa.models import Patent, from_ppubs  # noqa: E402
from ppa.uspto import PPUBSClient, USPTOError  # noqa: E402


def _load_fixtures() -> list[Patent]:
    fixdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "tests", "fixtures")
    patents = []
    for fn in sorted(os.listdir(fixdir)):
        if fn.endswith(".json"):
            with open(os.path.join(fixdir, fn)) as fh:
                patents.append(from_ppubs(json.load(fh)))
    return patents


def cmd_build(args: argparse.Namespace) -> int:
    if args.fixtures:
        patents = _load_fixtures()
        print(f"loaded {len(patents)} fixture patents (offline)")
    else:
        client = PPUBSClient()
        patents = []
        try:
            if args.inventor:
                hits = client.search_by_inventor(args.inventor,
                                                 limit=args.limit)
                numbers = []
                for h in hits:
                    num = (h.get("publicationReferenceDocumentNumber")
                           or h.get("publicationReferenceDocumentNumber1")
                           or "")
                    if num:
                        numbers.append(str(num))
                print(f"inventor search: {len(numbers)} patents found")
            else:
                numbers = args.patents
            for n in numbers:
                print(f"fetching US {n} ...")
                try:
                    doc = client.fetch_patent(n)
                except USPTOError as exc:
                    print(f"  !! {exc}")
                    continue
                patents.append(from_ppubs(doc))
        finally:
            client.close()
    for p in patents:
        if not p.title and not p.claims:
            print(f"  note: US {p.number} has no machine-readable text "
                  f"(very old grant); ontology will skip it")
    if not patents:
        print("no patents — nothing to build")
        return 1

    print("building ontology ...")
    onto = ontology.build_ontology(patents)

    data = {
        "meta": {
            "title": args.title,
            "version": __version__,
            "patent_count": len(patents),
            "numbers": [p.number for p in patents],
        },
        "patents": [p.to_dict() for p in patents],
        "ontology": onto,
    }

    print("generating API server ...")
    paths = api_gen.generate(args.out, data)

    md = report.markdown_report(args.title, patents, onto)
    with open(os.path.join(args.out, "ONTOLOGY.md"), "w") as fh:
        fh.write(md)
    with open(os.path.join(args.out, "ontology.html"), "w") as fh:
        fh.write(report.html_report(args.title, patents, onto))
    with open(os.path.join(args.out, "ontology.json"), "w") as fh:
        json.dump(onto, fh, indent=1)

    print(f"\nbuilt portfolio '{args.title}' -> {args.out}")
    print(f"  patents      : {len(patents)}")
    print(f"  concepts     : {len(onto['concepts'])}")
    print(f"  graph nodes  : {len(onto['graph']['nodes'])}")
    print(f"  server       : {paths['app']}")
    print(f"  openapi spec : {paths['openapi']}")
    print(f"  report       : {args.out}/ONTOLOGY.md")
    print(f"\nserve it:  python cli.py serve {args.out}")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn
    app_path = os.path.join(args.dir, "portfolio_api.py")
    if not os.path.exists(app_path):
        print(f"no generated API in {args.dir} — run build first")
        return 1
    print(f"serving {args.dir} on http://127.0.0.1:{args.port}  (Ctrl-C to stop)")
    uvicorn.run("portfolio_api:app",
                host="127.0.0.1", port=args.port, app_dir=args.dir)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Turn a USPTO patent portfolio into per-patent APIs + ontology.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="fetch patents and generate the portfolio API")
    b.add_argument("patents", nargs="*", help="USPTO patent numbers")
    b.add_argument("--inventor", help='inventor name search, e.g. "Musk"')
    b.add_argument("--limit", type=int, default=25,
                   help="max patents for inventor search")
    b.add_argument("--fixtures", action="store_true",
                   help="use offline test fixtures instead of the network")
    b.add_argument("--out", required=True, help="output directory")
    b.add_argument("--title", default="Patent Portfolio",
                   help="portfolio title")
    b.set_defaults(func=cmd_build)

    s = sub.add_parser("serve", help="serve a built portfolio API locally")
    s.add_argument("dir", help="output directory from build")
    s.add_argument("--port", type=int, default=8000)
    s.set_defaults(func=cmd_serve)

    args = ap.parse_args()
    if args.cmd == "build" and not args.fixtures \
            and not args.patents and not args.inventor:
        ap.error("build needs patent numbers, --inventor, or --fixtures")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
