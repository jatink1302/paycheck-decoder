from pydantic import BaseModel, NonNegativeFloat


class TaxWithholding(BaseModel):
    """Taxes actually withheld on the stub, as reported -- not recomputed.

    The rules engine (Week 2) recomputes each of these from taxable
    wages and compares against these reported values to produce
    Findings (F4, F5, F6). This model only holds what the stub says.
    """

    federal_income_tax: NonNegativeFloat
    social_security: NonNegativeFloat
    medicare: NonNegativeFloat
    illinois_income_tax: NonNegativeFloat
