# Paycheck Decoder and Wage Check

A plain-language pay stub explainer with minimum wage, overtime, and
withholding checks for Illinois W-2 workers, built as an eight-week
ChiEAC Fellows Program project.

## What it is

A guided form walks a worker through one pay stub, or an upload accepts
a CSV/XLSX payroll export covering several pay periods. In both cases
the tool will explain every line in plain language, check hours and
gross pay against the applicable federal, Illinois, Cook County, and
Chicago minimum wage and overtime rules, flag withholding that looks off
given the worker's W-4 answers, and project a year-end federal and
Illinois refund or balance due. Across several periods it will surface
patterns a single stub can't show: unpaid overtime, shrinking hours, and
unexplained new deductions.

## Educational purpose

This tool is educational. It is not tax, legal, or financial advice, and
it says so on every screen and in every report it produces.

## Current scope: Week 1 of 8

This repository currently contains the **Week 1 foundation only**:
repository scaffold, the canonical payroll data schema (typed, not yet
wired to any calculation), a `Finding` model rules will eventually
report through, an effective-dated rates configuration schema (values
unverified/placeholder), a starter rules register, and test/lint/CI
infrastructure with placeholder and basic model-validation tests.

**No payroll calculation exists yet.** There is no wage-floor check,
overtime check, FICA check, federal or Illinois withholding check,
year-end projection, anomaly detection, file upload, or Streamlit UI.
Those are later-week deliverables -- see the project brief for the
full week-by-week plan and `docs/open_questions.md` for unresolved
design questions that need answers before some of them can be built.

### Explicit non-goals (out of scope for this whole project)

- Any state other than Illinois; Illinois has no local income taxes.
- 1099 contractors, self-employment tax, estimated payments.
- PDF or image parsing of pay stubs (a stretch item only, and only if
  earlier weeks finish early).
- Direct integrations with ADP, Paychex, Gusto, QuickBooks, or any
  payroll API.
- Garnishment/child-support order calculations beyond a plain-language
  note.
- Tax filing or individualized legal/tax advice.
- Native mobile apps (the web app must work in a phone browser).

## Architecture

`engine/` is a plain Python package -- typed pydantic models plus (from
Week 2 onward) pure rule functions -- with no Streamlit dependency, so
the rules engine can be tested and reused independently of the UI.
`app/` will be Streamlit-only and will contain no payroll math of its
own. See [`docs/architecture.md`](docs/architecture.md) for the full
data flow and rationale.

```
engine/
  models/        canonical payroll schema (PayStub, PayPeriodSeries, ...)
  rules/         rule functions -- empty until Week 2
  findings.py    the Finding model every rule reports through
  jurisdiction.py effective-dated rate lookup -- stubbed until Week 2
app/             Streamlit UI -- not built yet
config/
  rates.yaml     effective-dated rates -- schema only, values unverified
  brand.yaml     white-label config (F11)
data/synthetic/  synthetic data only; real pay data is never committed
docs/            architecture, open questions, rules register, glossary
tests/           pytest suite
```

## Development setup

Requires Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/install_hooks.sh   # installs the data/ privacy pre-commit guard
```

## Running tests

```bash
pytest
ruff check .
ruff format --check .
```

CI (`.github/workflows/ci.yml`) runs both on every push.

## Privacy principles

- Real pay data is never committed to this repository, logged, put in a
  URL, or persisted by the application -- only synthetic data is used
  for development and demos.
- `data/` is git-ignored except `data/synthetic/`, and
  `scripts/check_data_dir.py` (wired as a local pre-commit hook) refuses
  to let any other file under `data/` be committed.
- No analytics, telemetry, or database. Everything the app will do runs
  in the visitor's session only.

## Rules and rates

Every wage/tax rate the engine will use must trace to an authoritative
source, recorded in [`docs/rules_register.csv`](docs/rules_register.csv)
with its source URL, effective dates, and the date it was verified.
`config/rates.yaml` is meant to be generated from register rows only
after they're verified -- see that file's header comment. No rule
function may contain a hard-coded numeric tax/wage constant.

## Project phase

Week 1 of 8: repository scaffold and canonical schema. Not deployed. No
calculations implemented yet.
