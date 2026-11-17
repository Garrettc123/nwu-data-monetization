"""Registration must change valuation state; no fabricated success."""
import pytest

from src.api.monetization_api import MonetizationAPI
from src.core.data_valuation import DataValuationEngine


@pytest.fixture
def api():
    return MonetizationAPI(bond_manager=None, valuation_engine=DataValuationEngine())


@pytest.fixture
def asset_payload():
    return {
        "asset_id": "DATA-REAL-001",
        "name": "Licensed Dataset",
        "description": "Valuation-only registration",
        "data_type": "structured",
        "volume": 100,
        "quality": "HIGH",
        "uniqueness_score": 0.5,
        "market_demand": 0.6,
    }


def test_registration_changes_underlying_valuation_state(api, asset_payload):
    result = api.create_asset(asset_payload)
    assert result["status"] == "success"
    assert result["asset_id"] == asset_payload["asset_id"]
    assert asset_payload["asset_id"] in api.valuation_engine.assets
    assert api.get_asset_value(asset_payload["asset_id"])["current_value"] > 0
    assert "not listed, sold or verified" in result["message"]


def test_duplicate_asset_rejected(api, asset_payload):
    api.create_asset(asset_payload)
    with pytest.raises(ValueError, match="already registered"):
        api.create_asset(asset_payload)


def test_missing_fields_rejected_without_registration(api, asset_payload):
    del asset_payload["quality"]
    with pytest.raises(ValueError, match="Missing asset fields"):
        api.create_asset(asset_payload)
    assert api.valuation_engine.assets == {}


@pytest.mark.parametrize(
    "field,value",
    [
        ("asset_id", ""),
        ("volume", 0),
        ("volume", -1),
        ("volume", True),
        ("quality", "UNVERIFIED"),
        ("uniqueness_score", -0.1),
        ("uniqueness_score", float("nan")),
        ("market_demand", 1.1),
        ("market_demand", float("inf")),
    ],
)
def test_invalid_payload_does_not_register(api, asset_payload, field, value):
    asset_payload[field] = value
    with pytest.raises(ValueError):
        api.create_asset(asset_payload)
    assert api.valuation_engine.assets == {}
