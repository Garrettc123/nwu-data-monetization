"""Liquidity Bonds Engine

Manages data liquidity bonds for instant monetization.
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class BondStatus(Enum):
    """Bond lifecycle status."""
    PENDING = "pending"
    ACTIVE = "active"
    MATURED = "matured"
    REDEEMED = "redeemed"
    DEFAULTED = "defaulted"


@dataclass
class LiquidityBond:
    """Represents a data liquidity bond."""
    bond_id: str
    data_asset_id: str
    principal_amount: float
    interest_rate: float
    maturity_date: datetime
    status: BondStatus
    issuer: str
    holder: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def calculate_value(self) -> float:
        """Calculate current bond value with accrued interest."""
        if self.status in [BondStatus.REDEEMED, BondStatus.DEFAULTED]:
            return 0.0
        
        days_elapsed = (datetime.utcnow() - self.created_at).days
        days_total = (self.maturity_date - self.created_at).days
        
        if days_total == 0:
            return self.principal_amount
        
        accrued_interest = (self.principal_amount * self.interest_rate * 
                          days_elapsed / days_total)
        return self.principal_amount + accrued_interest
    
    def redeem(self) -> float:
        """Redeem bond and return final value."""
        if self.status != BondStatus.ACTIVE:
            raise ValueError(f"Cannot redeem bond in {self.status} status")
        
        final_value = self.calculate_value()
        self.status = BondStatus.REDEEMED
        return final_value


class LiquidityBondManager:
    """Manages liquidity bond lifecycle."""
    
    def __init__(self):
        self.bonds: Dict[str, LiquidityBond] = {}
    
    def create_bond(
        self,
        data_asset_id: str,
        principal_amount: float,
        interest_rate: float,
        maturity_days: int,
        issuer: str
    ) -> LiquidityBond:
        """Create new liquidity bond."""
        bond_id = f"LB-{data_asset_id}-{datetime.utcnow().timestamp()}"
        maturity_date = datetime.utcnow()
        
        bond = LiquidityBond(
            bond_id=bond_id,
            data_asset_id=data_asset_id,
            principal_amount=principal_amount,
            interest_rate=interest_rate,
            maturity_date=maturity_date,
            status=BondStatus.ACTIVE,
            issuer=issuer
        )
        
        self.bonds[bond_id] = bond
        return bond
    
    def get_bond(self, bond_id: str) -> Optional[LiquidityBond]:
        """Retrieve bond by ID."""
        return self.bonds.get(bond_id)
    
    def list_bonds(self, status: Optional[BondStatus] = None) -> List[LiquidityBond]:
        """List all bonds, optionally filtered by status."""
        if status:
            return [b for b in self.bonds.values() if b.status == status]
        return list(self.bonds.values())
    
    def calculate_total_value(self) -> float:
        """Calculate total value of all active bonds."""
        return sum(
            bond.calculate_value() 
            for bond in self.bonds.values() 
            if bond.status == BondStatus.ACTIVE
        )
