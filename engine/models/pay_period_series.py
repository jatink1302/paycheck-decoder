from pydantic import BaseModel, Field, model_validator

from engine.models.paystub import PayStub


class PayPeriodSeries(BaseModel):
    """One worker's pay stubs across multiple periods -- the shape a
    multi-period CSV/XLSX upload (F8) is mapped into. Cross-period
    anomaly rules (Appendix C) operate on this, not on a single PayStub.
    """

    worker_id: str
    periods: list[PayStub] = Field(default_factory=list)

    @model_validator(mode="after")
    def _periods_belong_to_worker(self) -> "PayPeriodSeries":
        mismatched = [p for p in self.periods if p.worker_id != self.worker_id]
        if mismatched:
            raise ValueError(
                "Every pay period in a series must belong to the same worker. "
                f"Found {len(mismatched)} period(s) with a different worker_id."
            )
        return self

    @property
    def sorted_periods(self) -> list[PayStub]:
        return sorted(self.periods, key=lambda p: p.period_start)
