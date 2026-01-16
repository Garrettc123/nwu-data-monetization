"""Tests for data valuation engine."""

import pytest
from src.core.data_valuation import (
    DataAsset,
    DataQuality,
    DataValuationEngine
)


def test_asset_valuation():
    """Test basic data asset valuation."""
    asset = DataAsset(
        asset_id="ASSET-001",
        name="Customer Data",
        description="High-quality customer profiles",
        data_type="structured",
        volume=10000,
        quality=DataQuality.HIGH,
        uniqueness_score=0.8,
        market_demand=0.9
    )
    
    value = asset.calculate_base_value()
    assert value > 0


def test_valuation_engine():
    """Test valuation engine registration and calculation."""
    engine = DataValuationEngine()
    
    asset = DataAsset(
        asset_id="ASSET-002",
        name="Transaction Data",
        description="E-commerce transactions",
        data_type="time-series",
        volume=50000,
        quality=DataQuality.PREMIUM,
        uniqueness_score=0.9,
        market_demand=0.95
    )
    
    engine.register_asset(asset)
    value = engine.valuate_asset("ASSET-002")
    assert value > 0


def test_monetization_potential():
    """Test monetization potential calculation."""
    engine = DataValuationEngine()
    
    asset = DataAsset(
        asset_id="ASSET-003",
        name="User Behavior Data",
        description="Behavioral analytics",
        data_type="events",
        volume=100000,
        quality=DataQuality.HIGH,
        uniqueness_score=0.7,
        market_demand=0.85
    )
    
    engine.register_asset(asset)
    potential = engine.get_monetization_potential("ASSET-003")
    
    assert "current_value" in potential
    assert "monthly_revenue_potential" in potential
    assert "annual_revenue_potential" in potential
    assert potential["current_value"] > 0
