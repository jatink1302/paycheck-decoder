from enum import StrEnum

from pydantic import BaseModel, Field, NonNegativeFloat


class DeductionCategory(StrEnum):
    """Illinois requires written consent for most deductions from wages;
    pre- vs. post-tax matters for taxable-wage math (F5/F6)."""

    PRETAX = "pretax"
    POSTTAX = "posttax"


class Deduction(BaseModel):
    """One line item, e.g. {"code": "401k", "amount": 85.00}."""

    code: str = Field(description="Deduction code or label as it appears on the stub.")
    amount: NonNegativeFloat
    category: DeductionCategory
