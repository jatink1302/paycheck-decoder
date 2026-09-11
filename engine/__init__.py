"""Paycheck Decoder rules engine.

Pure, Streamlit-independent package: typed models (engine.models) plus
rule functions (engine.rules) that take a PayStub/PayPeriodSeries and the
effective rates for its period and return Finding objects. No numeric
tax/wage constants live in this package -- they are read from
config/rates.yaml, which is itself only populated from a verified
rules register entry.
"""
