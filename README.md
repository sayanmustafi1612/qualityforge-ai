# QualityForge AI — Intelligent Test Automation & Quality Intelligence Platform

A portfolio-grade QA engineering platform: UI automation (Playwright), API
contract testing (Pytest + Pydantic), CI/CD quality gates (GitHub Actions),
and a **flaky-test intelligence dashboard** that scores every test's
reliability from historical run data — not just its last result.

Built against two stable public demo targets so it runs out of the box
with zero setup: [SauceDemo](https://www.saucedemo.com) for UI, and
[DummyJSON](https://dummyjson.com) for the REST API. Swap `QF_UI_BASE_URL`
/ `QF_API_BASE_URL` to point it at your own app.

## Why this exists

Most portfolio automation repos stop at "here are some Selenium tests."
This one answers the question a hiring manager actually cares about: *can
this person design a quality system, not just write test cases?* That
means: architecture that separates concerns (pages / api clients / core /
utils), a CI pipeline with real gating logic (smoke on every PR, full
regression nightly), and a feedback loop — the flakiness engine — that
turns raw pass/fail noise into an actionable signal.

## Architecture

```
GitHub PR → GitHub Actions CI
              ├─ static-checks (ruff, mypy)
              ├─ api-tests        (pytest -m api)
              ├─ ui-smoke-tests   (pytest -m smoke)
              └─ full-regression  (nightly / labeled PRs)
                     │
                     ▼
            results/history.db (SQLite)
                     │
              utils/failure_analyzer.py
                     │
              dashboard/app.py (Streamlit)
```

## Project layout

```
qualityforge-ai/
├── tests/
│   ├── ui/            UI tests (Playwright, via page objects)
│   ├── api/           API contract tests (schema + status validation)
│   ├── integration/   Cross-checks between UI and API
│   └── conftest.py    Fixtures + auto test-history recording
├── pages/             Page Object Model classes
├── api/clients/       REST client + Pydantic response schemas
├── core/              Config, logging, Playwright driver factory
├── utils/             SQLite results store + flakiness scoring engine
├── dashboard/         Streamlit quality dashboard
├── .github/workflows/ CI pipeline
├── Dockerfile / docker-compose.yml
└── requirements.txt
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Run everything
pytest

# Run just smoke tests (what CI runs on every PR)
pytest -m smoke

# Run API tests in parallel
pytest tests/api -m api -n auto

# Generate an Allure report
pytest --alluredir=results/allure
allure serve results/allure

# View the quality dashboard (after running some tests a few times)
streamlit run dashboard/app.py
```

Or via Docker:

```bash
docker compose run tests
docker compose up dashboard   # http://localhost:8501
```

## The flakiness engine (Phase 4)

Every test run — pass, fail, or skip — is appended to
`results/history.db` via a pytest hook in `conftest.py`. Run enough times
(locally or across CI runs) and `utils/failure_analyzer.py` computes a
per-test score blending two signals:

- **failure rate** — how often the test fails outright
- **transition rate** — how often it flips pass → fail → pass, which is
  the actual signature of flakiness (a test that fails every single time
  isn't flaky, it's just broken)

Tests are classified `STABLE`, `FLAKY`, `HIGH_FLAKINESS`, or `BROKEN`, and
the Streamlit dashboard surfaces this ranked, alongside average duration
and raw run history — so a reviewer can see automation health trends at a
glance instead of squinting at a wall of green/red CI badges.

## Roadmap

- [x] Phase 1 — Playwright + Pytest, Page Object Model, API client, fixtures, parallel execution
- [x] Phase 2 — Structured logging, screenshots on failure, retries, test tagging, Allure reporting
- [x] Phase 3 — GitHub Actions CI: PR smoke gate, nightly regression, artifact uploads
- [x] Phase 4 — Flaky-test intelligence engine + Streamlit dashboard
- [ ] Phase 5 — LLM-based failure summarization (feed `report.longrepr` from a failed test to an LLM and store a one-line root-cause guess alongside the failure)

