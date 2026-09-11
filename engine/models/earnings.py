from pydantic import BaseModel, Field, NonNegativeFloat


class Earnings(BaseModel):
    """Hours and rates as they appear on a single pay stub.

    Overtime here is whatever the stub itself reports. Whether
    regular_hours over 40 *should* have produced overtime is a rules-
    engine question (F3 / Appendix C rule A1), not something this model
    decides -- see docs/open_questions.md for the pay-period-vs-workweek
    caveat that check depends on.
    """

    regular_hours: NonNegativeFloat = Field(
        description="Hours paid at the regular rate this pay period."
    )
    regular_rate: NonNegativeFloat = Field(
        description="Promised hourly rate for regular hours, in dollars."
    )
    overtime_hours: NonNegativeFloat = Field(
        default=0,
        description="Hours paid at the overtime rate this pay period, if any.",
    )
    overtime_rate: NonNegativeFloat | None = Field(
        default=None,
        description="Hourly overtime rate, in dollars. Absent if no overtime was paid.",
    )
    other_earnings: NonNegativeFloat = Field(
        default=0,
        description="Bonuses, tips, or commissions not covered by regular/overtime pay.",
    )
