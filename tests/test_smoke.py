"""Placeholder/smoke tests (Week 1): prove the package is importable and
the project structure works. Not a test of any payroll rule -- there
are no rules yet.
"""

import importlib


def test_engine_package_imports():
    engine = importlib.import_module("engine")
    assert engine is not None


def test_engine_models_import():
    models = importlib.import_module("engine.models")
    assert models.PayStub is not None
    assert models.PayPeriodSeries is not None


def test_engine_findings_imports():
    findings = importlib.import_module("engine.findings")
    assert findings.Finding is not None


def test_rates_config_is_valid_yaml():
    import yaml

    with open("config/rates.yaml") as f:
        data = yaml.safe_load(f)
    assert "rules" in data
    assert len(data["rules"]) > 0
