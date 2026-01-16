"""Tests for liquidity bonds functionality."""

import pytest
from datetime import datetime, timedelta
from src.core.liquidity_bonds import (
    LiquidityBond,
    LiquidityBondManager,
    BondStatus
)


def test_bond_creation():
    """Test creating a new liquidity bond."""
    manager = LiquidityBondManager()
    
    bond = manager.create_bond(
        data_asset_id="DATA-001",
        principal_amount=10000.0,
        interest_rate=0.05,
        maturity_days=90,
        issuer="test-issuer"
    )
    
    assert bond.principal_amount == 10000.0
    assert bond.status == BondStatus.ACTIVE
    assert bond.bond_id.startswith("LB-DATA-001")


def test_bond_value_calculation():
    """Test bond value calculation with accrued interest."""
    bond = LiquidityBond(
        bond_id="TEST-BOND",
        data_asset_id="DATA-001",
        principal_amount=10000.0,
        interest_rate=0.10,
        maturity_date=datetime.utcnow() + timedelta(days=365),
        status=BondStatus.ACTIVE,
        issuer="test-issuer"
    )
    
    value = bond.calculate_value()
    assert value >= bond.principal_amount


def test_bond_redemption():
    """Test bond redemption."""
    bond = LiquidityBond(
        bond_id="TEST-BOND",
        data_asset_id="DATA-001",
        principal_amount=10000.0,
        interest_rate=0.05,
        maturity_date=datetime.utcnow() + timedelta(days=90),
        status=BondStatus.ACTIVE,
        issuer="test-issuer"
    )
    
    final_value = bond.redeem()
    assert final_value > 0
    assert bond.status == BondStatus.REDEEMED


def test_portfolio_total_value():
    """Test calculating total portfolio value."""
    manager = LiquidityBondManager()
    
    manager.create_bond("DATA-001", 10000.0, 0.05, 90, "issuer-1")
    manager.create_bond("DATA-002", 15000.0, 0.05, 90, "issuer-2")
    
    total = manager.calculate_total_value()
    assert total >= 25000.0
