# Architecture

Status: Week 1 foundation. This describes the structure being built
toward, not functionality that exists yet -- see the repository root
README for current scope.

## System boundaries

Paycheck Decoder has two independent halves:

- **`engine/`** -- a plain Python package with no Streamlit import
  anywhere in it. Typed pydantic models (`engine/models/`) define the
  canonical payroll schema; pure functions in `engine/rules/` (starting
  Week 2) take a `PayStub` or `PayPeriodSeries` plus the effective rates
  for its period and return a `list[engine.findings.Finding]`. Every
  rule function is testable in isolation with no UI, no file I/O beyond
  reading `config/rates.yaml`, and no network access.
- **`app/`** -- Streamlit only. It collects input (the guided form or an
  uploaded CSV/XLSX), maps it into `engine.models` objects, calls
  `engine.rules` functions, and renders the `Finding`s it gets back. It
  contains no payroll math of its own.

This split exists so the rules engine -- the part where a bug does real
harm to a worker's trust in the tool -- can be tested exhaustively
against agency-published examples without a browser or a UI framework
in the loop, and so a different front end could replace Streamlit later
without touching the engine.

## Why the engine is independent of Streamlit

Two concrete reasons, both from the project brief:

1. Gate 1 (Week 2) requires the rules engine to pass agency-derived test
   cases *before* any UI work starts. That is only possible if the
   engine has no UI dependency to stand up first.
2. F5-F7's acceptance tests compare engine output against external
   oracles (IRS Tax Withholding Estimator, published worksheets) to
   within a dollar. Those comparisons run in pytest, not in a browser.

## Data flow (target shape)

```
Guided form  ──┐
               ├─▶ engine.models.PayStub / PayPeriodSeries
CSV/XLSX      ──┘         │
upload + mapper           ▼
                  engine.rules.* (pure functions)
                           │
                           ▼
                  list[engine.findings.Finding]
                           │
                           ▼
                  app/ renders: looks right / worth a
                  question / needs attention groups,
                  plus the year-end projection panel
                  and the exportable report (F10)
```

Nothing in this path writes input data to disk, logs it, or puts it in
a URL -- see the Privacy section below and F12.

## Rules and configuration

`config/rates.yaml` holds every effective-dated rate the engine uses:
`rule_id`, `jurisdiction`, `value`, `unit`, `effective_from`,
`effective_to`, `source_name`, `source_url`, `section_or_table`,
`verified_on`. Rule *functions* in `engine/rules/` contain no numeric
tax/wage constants of their own -- they look up the value they need for
a given jurisdiction and as-of date (via `engine/jurisdiction.py`,
stubbed as of Week 1) and stay pure otherwise.

`docs/rules_register.csv` is the human-editable superset this file is
generated from: every row has the same fields plus room to work through
verification before anything is promoted into `config/rates.yaml`. See
that file's header and Step 2 of the project brief for the verification
workflow. `config/rates.yaml` should only ever contain values that have
a `verified_on` date -- a `null` value there means "not yet verified,"
not "assumed zero" or "not applicable."

## How findings flow from engine to UI

A `Finding` (`engine/findings.py`) is the only object that crosses the
engine/app boundary in the output direction. It carries a stable `code`
(e.g. `A1`, `F5`), a `severity` that maps directly onto the three-group
UI ("looks right" / "worth a question" / "needs attention"), a
plain-language `message`, the `evidence` numbers behind the flag, which
`periods` it concerns (for cross-period rules), and a `next_step`. The
app never re-derives or re-explains a finding; it renders what the
engine gives it.

## How CSV/XLSX uploads will map into the canonical model (Week 5)

Not built yet. The intended shape, per Step 5.2 of the project brief:
read the file with `pandas`/`openpyxl`, detect the header row, offer a
column-mapping step (with fuzzy suggestions from the glossary's
`aliases`) that pairs each source column to a field on
`engine.models.PayStub`, validate the mapped result against that model
(so the same validation errors a single-stub entry would raise apply
here too), and construct one `PayPeriodSeries` per worker.

## Privacy

No pay data -- real or, outside `data/synthetic/`, even synthetic -- is
ever written to disk, logged, or included in a URL or analytics event.
`app/` processes everything in memory for the session only.
`scripts/check_data_dir.py` (wired as a pre-commit hook, see README)
refuses to let any file under `data/` other than `data/synthetic/` be
committed. See F12 and Section 6 (privacy review checklist) of the
project brief for the full requirement.
