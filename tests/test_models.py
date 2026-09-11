"""Basic model validation tests for the canonical schema v0 (Week 1).

These check structural validation only (types, ranges, date ordering) --
none of these numbers are asserted as a "correct" payroll outcome. Rule
correctness tests come in Week 2 and must be built from agency-published
examples, not from values the implementation itself produces.
"""

from datetime import date

import pytest
from pydantic import ValidationError

from engine.findings import Finding, Severity
from engine.models import (
    Deduction,
    DeductionCategory,
    Earnings,
    FilingStatus,
    Jurisdiction,
    PayFrequency,
    PayPeriodSeries,
    PayStub,
    TaxWithholding,
    W4Answers,
)


def _make_paystub(**overrides) -> PayStub:
    defaults = dict(
        worker_id="synthetic-worker-1",
        period_start=date(2026, 1, 1),
        period_end=date(2026, 1, 14),
        pay_date=date(2026, 1, 20),
        pay_frequency=PayFrequency.BIWEEKLY,
        jurisdiction=Jurisdiction.CHICAGO,
        earnings=Earnings(regular_hours=80, regular_rate=20.0),
        gross_pay=1600.0,
        deductions=[Deduction(code="401k", amount=50.0, category=DeductionCategory.PRETAX)],
        tax=TaxWithholding(
            federal_income_tax=150.0,
            social_security=99.2,
            medicare=23.2,
            illinois_income_tax=76.7,
        ),
        net_pay=1201.0,
        w4=W4Answers(filing_status=FilingStatus.SINGLE_OR_MARRIED_FILING_SEPARATELY),
    )
    defaults.update(overrides)
    return PayStub(**defaults)


def test_valid_paystub_constructs():
    stub = _make_paystub()
    assert stub.worker_id == "synthetic-worker-1"
    assert stub.pretax_deductions[0].code == "401k"
    assert stub.posttax_deductions == []


def test_negative_hours_rejected():
    with pytest.raises(ValidationError):
        Earnings(regular_hours=-1, regular_rate=20.0)


def test_negative_gross_pay_rejected():
    with pytest.raises(ValidationError):
        _make_paystub(gross_pay=-100.0)


def test_period_end_before_start_rejected():
    with pytest.raises(ValidationError):
        _make_paystub(period_start=date(2026, 1, 14), period_end=date(2026, 1, 1))


def test_pay_date_before_period_start_rejected():
    with pytest.raises(ValidationError):
        _make_paystub(pay_date=date(2025, 12, 1))


def test_pay_period_series_requires_matching_worker_id():
    stub_a = _make_paystub(worker_id="worker-a")
    stub_b = _make_paystub(worker_id="worker-b")
    with pytest.raises(ValidationError):
        PayPeriodSeries(worker_id="worker-a", periods=[stub_a, stub_b])


def test_pay_period_series_sorts_periods():
    later = _make_paystub(
        period_start=date(2026, 2, 1), period_end=date(2026, 2, 14), pay_date=date(2026, 2, 20)
    )
    earlier = _make_paystub()
    series = PayPeriodSeries(worker_id="synthetic-worker-1", periods=[later, earlier])
    assert series.sorted_periods[0].period_start == date(2026, 1, 1)


def test_finding_requires_message_and_next_step():
    finding = Finding(
        code="A1",
        severity=Severity.NEEDS_ATTENTION,
        message="You worked more than 40 hours but no overtime appears.",
        next_step="Ask payroll; keep your own hours record.",
    )
    assert finding.severity is Severity.NEEDS_ATTENTION
    with pytest.raises(ValidationError):
        Finding(code="A1", severity=Severity.NEEDS_ATTENTION)
