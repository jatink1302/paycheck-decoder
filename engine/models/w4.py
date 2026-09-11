from enum import StrEnum

from pydantic import BaseModel, Field, NonNegativeFloat


class FilingStatus(StrEnum):
    """The three Step 1(c) options on the current-design Form W-4."""

    SINGLE_OR_MARRIED_FILING_SEPARATELY = "single_or_married_filing_separately"
    MARRIED_FILING_JOINTLY = "married_filing_jointly"
    HEAD_OF_HOUSEHOLD = "head_of_household"


class W4Answers(BaseModel):
    """A worker's federal Form W-4 answers, entered once and applied to
    every period (per Appendix B). Field names mirror the form's own
    step numbers so the Step 1A percentage-method implementation (Week 2)
    can map onto them directly -- no computation happens here.
    """

    filing_status: FilingStatus
    step2_checkbox: bool = Field(
        default=False,
        description="Step 2(c): multiple jobs or spouse works checkbox.",
    )
    step3_credits: NonNegativeFloat = Field(
        default=0, description="Step 3: total claimed dependent/other credits, in dollars."
    )
    step4a_other_income: NonNegativeFloat = Field(
        default=0, description="Step 4(a): other income (not from jobs), in dollars."
    )
    step4b_deductions: NonNegativeFloat = Field(
        default=0, description="Step 4(b): deductions beyond the standard deduction, in dollars."
    )
    step4c_extra_withholding: NonNegativeFloat = Field(
        default=0, description="Step 4(c): extra withholding per pay period, in dollars."
    )


class ILW4Answers(BaseModel):
    """A worker's Illinois Form IL-W-4 answers."""

    exemptions: int = Field(ge=0, description="Total exemptions claimed on the IL-W-4.")
