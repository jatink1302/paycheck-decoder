from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    """Maps to the three-group UI in Step 4.3 of the project brief."""

    LOOKS_RIGHT = "looks_right"
    WORTH_A_QUESTION = "worth_a_question"
    NEEDS_ATTENTION = "needs_attention"


class Finding(BaseModel):
    """One result from a rule function. Rule functions (Week 2 onward)
    are pure: (PayStub | PayPeriodSeries, rates) -> list[Finding].

    This model has no logic of its own -- it is the shared shape every
    rule family (F3-F6, F9) reports through, so the app layer can render
    all of them the same way regardless of which rule produced them.
    """

    code: str = Field(description="Stable rule id, e.g. 'A1' or 'F5'.")
    severity: Severity
    message: str = Field(description="Plain-language explanation for the worker.")
    evidence: dict = Field(
        default_factory=dict,
        description="The numbers behind the flag, e.g. {'regular_hours': 45, 'overtime_hours': 0}.",
    )
    periods: list[date] = Field(
        default_factory=list,
        description="period_start date(s) this finding is about, for multi-period findings.",
    )
    next_step: str = Field(description="What the worker can do about it, in plain language.")
