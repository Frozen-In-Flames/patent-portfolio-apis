# Distribution channels — Patent Portfolio APIs ($0 budget)

Status: RESEARCH — nothing posted or submitted. Each needs Aries's go-ahead.

## 1. Hacker News "Show HN" — ready to post
- Cost: $0. Audience: developers, founders, some IP-curious. Best for open-source tools.
- Draft at: distribution/show-hn-draft.md. Post timing: weekday morning US time.
- Needs: Aries's approval of the draft text (it posts under his name/account).

## 2. Inventor communities (Reddit) — ready to post
- r/patents, r/inventors: inventors asking portfolio questions are the end users.
- Angle: "I built a free tool that turns your USPTO portfolio into APIs and shows where two portfolios overlap (M&A use case)" with the demo link.
- Needs: Aries's approval; each sub has its own self-promotion rules, check before posting.

## 3. Live demo on GitHub Pages — one setting to flip
- Static demo BUILT and tested (Oct 8): docs/index.html + docs/merge.json render the real
  v0.2.0 merger run (OpticsCo x Photonix: 19 shared concepts, 9 redundant pairs, Toshiba 12748190
  x DJI 12754414 top pair at score 22) with no backend. The old examples/merger-demo/index.html
  needs a live FastAPI server, so the static docs/ page is the one Pages should serve.
- Enabling GitHub Pages = 3 clicks, no token needed: repo Settings -> Pages -> Deploy from a
  branch -> master -> /docs. URL becomes https://ariesconsulting.github.io/patent-portfolio-apis/
- Why it matters: Patent-Lint (a comparable open-source patent tool) distributes exactly this way — live demo site + GitHub repo.
- Needs: Aries's approval (committed locally, NOT pushed; nothing public changes until he says go).

## 4. Hugging Face Space — blocked on his token
- Package at hf-space/ is refreshed to v0.2.0 and committed locally; deploys in one step once the stored HF token is refreshed (reconnect card already sent to him).
- Needs: only his fresh token. No nudge sent — he was already looped in.

## 5. Dev-tool / AI-tool directories — submit later
- Free listings (e.g., tool directories) come after the live demo is up; a repo with no running demo converts poorly.

## What NOT to do without him
- No direct outreach to IP law firms or M&A advisors yet: that is a sales motion, and any terms or commitments need his eyes first per the distribution directive.
