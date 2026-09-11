from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field, NonNegativeFloat, model_validator

from engine.models.deductions import Deduction, DeductionCategory
from engine.models.earnings import Earnings
from engine.models.tax import TaxWithholding
from engine.models.w4 import ILW4Answers, W4Answers
from engine.models.ytd import YearToDate


class PayFrequency(StrEnum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    SEMIMONTHLY = "semimonthly"
    MONTHLY = "monthly"


class Jurisdiction(StrEnum):
    """Drives which wage floor applies (Appendix B). illinois_other
    covers any Illinois work location outside Chicago and Cook County.
    """

    CHICAGO = "chicago"
    COOK_COUNTY = "cook_county"
    ILLINOIS_OTHER = "illinois_other"


class PayStub(BaseModel):
    """Canonical schema v0 for one pay period, per Appendix B of the
    project brief. This model validates structure and plausible ranges
    only -- it does not check the numbers against any wage or tax rule.
    That is the rules engine's job (Week 2 onward), operating on the
    rates loaded from config/rates.yaml for this stub's period.
    """

    worker_id: str = Field(description="Stable identifier; synthetic in all test data.")

    period_start: date
    period_end: date
    pay_date: date
    pay_frequency: PayFrequency
    jurisdiction: Jurisdiction

    earnings: Earnings
    gross_pay: NonNegativeFloat

    deductions: list[Deduction] = Field(default_factory=list)

    tax: TaxWithholding
    net_pay: NonNegativeFloat

    ytd: YearToDate = Field(default_factory=YearToDate)

    w4: W4Answers | None = Field(
        default=None, description="Entered once; may be omitted if not yet collected."
    )
    il_w4: ILW4Answers | None = None

    is_tipped: bool = False
    is_youth: bool = False

    @property
    def pretax_deductions(self) -> list[Deduction]:
        return [d for d in self.deductions if d.category is DeductionCategory.PRETAX]

    @property
    def posttax_deductions(self) -> list[Deduction]:
        return [d for d in self.deductions if d.category is DeductionCategory.POSTTAX]

    @model_validator(mode="after")
    def _dates_in_order(self) -> "PayStub":
        if self.period_end < self.period_start:
            raise ValueError(
                "The pay period end date is before the start date. "
                "Check the dates on the stub and try again."
            )
        if self.pay_date < self.period_start:
            raise ValueError(
                "The pay date is before the pay period even starts. "
                "Check the dates on the stub and try again."
            )
        return self
