from pydantic import BaseModel, NonNegativeFloat


class YearToDate(BaseModel):
    """Running totals since January 1, as reported on the stub.

    All fields are optional at the model level (a single stub may not
    show YTD figures), but strongly recommended -- without them,
    reconciliation rule A9 and the year-end projection (F7) cannot run.
    """

    ytd_gross: NonNegativeFloat | None = None
    ytd_federal: NonNegativeFloat | None = None
    ytd_social_security: NonNegativeFloat | None = None
    ytd_medicare: NonNegativeFloat | None = None
    ytd_illinois: NonNegativeFloat | None = None
