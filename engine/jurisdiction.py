"""Effective-dated rate lookup.

Not implemented in Week 1. This module will, in Week 2, load
config/rates.yaml and resolve the correct rate for a given rule_id,
jurisdiction, and as-of date (choosing the row whose effective_from/
effective_to window contains that date). Building this is explicitly a
Week 2 task (F3's jurisdiction-and-effective-date lookup); it is stubbed
here only so engine/rules modules have somewhere to import it from once
that work starts.
"""

from datetime import date

from engine.models.paystub import Jurisdiction


def rate_for(rule_id: str, jurisdiction: Jurisdiction, as_of: date) -> float:
    raise NotImplementedError(
        "Effective-dated rate lookup is a Week 2 deliverable. "
        "See docs/rules_register.csv and config/rates.yaml."
    )
