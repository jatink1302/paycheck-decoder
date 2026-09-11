# Open questions

Recorded rather than guessed, per the fellowship's working rules. Each
entry says what's unresolved, why it matters, and who needs to weigh in
(Benjamin / an authoritative source / a later-week design decision).
Update this file as questions get resolved -- don't just accept a
default silently.

## 1. Workweek vs. pay period for overtime eligibility (blocks F3, A1)

FLSA overtime is calculated **per workweek**, not per pay period. But a
biweekly, semimonthly, or monthly stub reports `regular_hours` and
`overtime_hours` as single totals for the whole period (Appendix B). For
a biweekly stub, 84 total hours could be 42+42 (both workweeks over 40,
overtime owed both weeks) or 50+34 (overtime owed one week only) or even
44+40 (overtime owed one week, not the other) -- and the schema as
specified cannot distinguish these from the totals alone.

**Why it matters:** F3's acceptance test explicitly says "flag hours
over 40 in a workweek without an overtime line." As specified, the
canonical schema (Appendix B) has no field that captures workweek
boundaries within a pay period, so the engine cannot actually do a
workweek-level check from Appendix B fields alone for anything more
frequent... anything *less* frequent than weekly.

**Not resolved here.** Options I see, none implemented:
- (a) Extend the schema with a per-workweek hours breakdown, required
  for biweekly/semimonthly/monthly stubs (most accurate, most burden on
  the guided-entry form and the column mapper).
- (b) Treat pay-period totals as an approximation and say so explicitly
  in the finding's plain-language text (matches brief scope better, but
  weakens the F3 acceptance test's precision for non-weekly pay).
- (c) Only run the workweek-level check when `pay_frequency == weekly`,
  and for other frequencies flag a softer "we can't fully check overtime
  from a period total -- see this worksheet" message.

**Needs:** Benjamin's call at a Friday check-in per Section 7 of the
brief, before Week 2 implements F3.

## 2. Chicago's 4-or-more-employee threshold isn't in the canonical schema

Chicago's minimum wage ordinance rate depends on employer size (4+
employees pay the higher rate; the brief's rate snapshot doesn't specify
the sub-4 rate). Appendix B's schema has no `employer_size` or
equivalent field, only `jurisdiction`.

**Why it matters:** Without this field, the engine cannot pick the
correct Chicago wage floor for a small employer, and F3's Chicago
scenarios can't be fully tested.

**Needs:** Either add a field (e.g. `employer_employee_count` or a
boolean `employer_has_4_or_more_employees`) to the schema, or document
that the tool always assumes the 4+ rate applies and say so on screen.
Not decided.

## 3. Youth minimum wage's 650-hours-per-year threshold isn't derivable

Illinois's youth minimum wage applies under 18 and under 650 hours in a
year. The schema has `is_youth: boolean` but no YTD *hours* field --
only YTD dollar totals (`ytd_gross`, `ytd_federal`, etc., per Appendix
B). Whether a worker has crossed 650 hours for the year can't be checked
from the data the schema currently captures.

**Why it matters:** F3's youth-wage variant can't be fully automated
without this; today it would have to rely entirely on the user's
`is_youth` self-report with no cross-check.

**Needs:** Decide whether to add a YTD-hours field, accept the
limitation and disclose it in the finding text, or drop automatic
tracking of the 650-hour cutoff (self-report only). Not decided.

## 4. Rate selection when a pay period spans an effective-date change

Chicago's minimum wage changes every July 1; federal/Illinois change
January 1. A pay period can straddle one of these dates (e.g. a biweekly
period from June 25 to July 8). `config/rates.yaml` rows are
effective-dated by single date ranges, but it's not decided which date
on the `PayStub` (`period_start`, `period_end`, or `pay_date`) selects
the applicable rate, or whether a straddling period should be prorated.

**Needs:** A decision before `engine/jurisdiction.py`'s lookup logic is
implemented in Week 2. Likely candidate: use `period_start` and flag
straddling periods for manual review rather than prorate, but this is a
guess, not a decision -- raise it at a Friday check-in.

## 5. W-4 / IL-W-4 answers are modeled as a single snapshot per worker

Appendix B says W-4 answers are "entered once and applied to all
periods." Real workers can submit a new W-4 mid-year. The current
schema (`PayStub.w4`, `PayStub.il_w4`) puts these answers *on each
stub*, which technically allows different periods in a `PayPeriodSeries`
to carry different W-4 answers if the upload data has them -- but
nothing validates that a change is intentional versus a mapping error,
and the multi-period upload path (Week 5) hasn't decided how it wants to
surface a mid-year W-4 change if one appears in the data.

**Needs:** Revisit when Week 5's column mapper is built.

## 6. Net-pay arithmetic check: model validator or Finding, not both

F1 asks for "net pay equals gross minus taxes and deductions within one
cent" as guided-form validation; Appendix C's rule A12 asks for
essentially the same check as a cross-period anomaly Finding. I
deliberately did **not** add a hard pydantic validator for this on
`PayStub` in Week 1, so that a stub whose numbers don't add up can still
be constructed and handed to the rules engine to produce an A12/F1
Finding for the user to see -- a hard validator would make that finding
unreachable (construction would raise before any rule ever ran).

This is a decision, not an open question, but it's recorded here since
it affects how Week 2/3 wire up F1's "under one cent" check: as a
rule-engine `Finding` like A12, or as separate form-level validation in
`app/` before a `PayStub` is even constructed. Leaning toward "same
mechanism as A12, reused for the single-stub case," but not decided.

## 7. Deduction pretax/posttax classification on upload

The canonical schema requires each `Deduction` to carry a
`category` (pretax/posttax). A guided-entry form can ask directly, but a
CSV/XLSX export (Week 5) may not label this explicitly per column, and
the same deduction code (e.g. "401k") is almost always pretax while
others (e.g. "union_dues") are almost always posttax -- but "almost
always" isn't a source-backed rule. Whether the column mapper should
infer category from `docs/glossary.yaml` aliases, require the user to
confirm each mapped deduction's category, or something else, isn't
decided.

**Needs:** Week 5 design decision when the column mapper is built.

## 8. Ownership terms and LICENSE file not yet set

Section 8.1 of the project brief states the *default* position (ChiEAC
owns the product; fellow retains portfolio/attribution rights; core
engine may be open-sourced with fellow credited as author) but
explicitly says "Benjamin to confirm the exact terms at kickoff and
record them in the repository LICENSE and README." No `LICENSE` file
has been added and the README does not state ownership terms, since
this is Benjamin's decision to confirm, not mine to assume.

**Needs:** Benjamin's confirmation at kickoff, then a `LICENSE` file and
a README ownership section reflecting whatever was agreed.

## 9. GitHub repository visibility

Step 5.3 of the brief says "public repository unless Benjamin decides
otherwise at kickoff." No remote has been created and no visibility
decision has been made yet.

**Needs:** Confirm at kickoff, then create the GitHub remote
accordingly.
