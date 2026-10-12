# Show HN draft — Patent Portfolio APIs v0.2.0 (M&A merge)

Status: ON HOLD as of Oct 12, 2026 — Aries said "skip anything you don't have." No HN account on file and browser is not signed in, so the post is parked until he provides HN credentials. Quick-start fix is pushed to main and live on the demo.

## Title

Show HN: Patent Portfolio APIs: turn USPTO patents into queryable APIs, now with M&A merge analysis

## Body

I built a tool that converts any inventor's USPTO patent portfolio into per-patent REST APIs plus a portfolio-wide ontology summary.

Give it patent numbers or an inventor name. It pulls full records from USPTO's public search API (no key needed), parses the claims, citations, and CPC classification codes, expands acronyms in the language, and generates a runnable FastAPI server plus Markdown/HTML reports.

v0.2.0 adds the use case I care about most: M&A portfolio merge. Feed it two portfolios and it shows the shared technical concepts, ranked redundant patent pairs across the two sides, and coverage gaps on each side. The demo merges two 3-patent LiDAR portfolios and flags, for example, a Toshiba LiDAR device overlapping a DJI scanning optical assembly.

The pitch: M&A IP due diligence currently takes weeks of billable hours just to answer "where do these portfolios overlap, where are the gaps, what are we double-holding?" This answers the technical half of that in one run. Price it against legal bills, not software.

Free, Apache-2.0, runs locally. GitHub: https://github.com/Frozen-In-Flames/patent-portfolio-apis
itch.io (free download): https://frozen-in-flames.itch.io/patent-portfolio-apis
Live demo: https://frozen-in-flames.github.io/patent-portfolio-apis/ (live static demo; Hugging Face Space follows once the token is refreshed)

Happy to take questions or feature requests. If you have done IP due diligence in a real deal, I would especially like to hear where this falls short.
