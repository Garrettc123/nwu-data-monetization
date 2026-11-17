"""REST API for Data Monetization Engine

Provides endpoints for asset management and bond operations.
"""

from typing import Dict, List, Optional
from datetime import datetime
from math import isfinite
from src.core.data_valuation import DataAsset, DataQuality


class MonetizationAPI:
    """API interface for monetization operations."""
    
    def __init__(self, bond_manager, valuation_engine):
        self.bond_manager = bond_manager
        self.valuation_engine = valuation_engine
    
    def create_asset(self, asset_data: Dict) -> Dict:
        """Validate and register a data asset in the in-memory valuation engine.

        Registration is not marketplace listing, rights verification, payment,
        bond issuance, or revenue realization.
        """
        required = (
            "asset_id", "name", "description", "data_type", "volume",
            "quality", "uniqueness_score", "market_demand",
        )
        missing = [key for key in required if key not in asset_data]
        if missing:
            raise ValueError(f"Missing asset fields: {', '.join(missing)}")

        asset_id = asset_data["asset_id"]
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise ValueError("asset_id must be a nonempty string")
        if asset_id in self.valuation_engine.assets:
            raise ValueError(f"Asset already registered: {asset_id}")

        for field in ("name", "description", "data_type"):
            if not isinstance(asset_data[field], str) or not asset_data[field].strip():
                raise ValueError(f"{field} must be a nonempty string")

        volume = asset_data["volume"]
        if isinstance(volume, bool) or not isinstance(volume, int) or volume <= 0:
            raise ValueError("volume must be a positive integer")

        quality = asset_data["quality"]
        if isinstance(quality, str):
            try:
                quality = DataQuality[quality.upper()]
            except KeyError as exc:
                raise ValueError("quality must be LOW, MEDIUM, HIGH or PREMIUM") from exc
        if not isinstance(quality, DataQuality):
            raise ValueError("quality must be a DataQuality value or name")

        for field in ("uniqueness_score", "market_demand"):
            value = asset_data[field]
            if isinstance(value, bool) or not isinstance(value, (float, int)):
                raise ValueError(f"{field} must be between 0 and 1")
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{field} must be between 0 and 1")

        asset = DataAsset(
            asset_id=asset_id,
            name=asset_data["name"],
            description=asset_data["description"],
            data_type=asset_data["data_type"],
            volume=volume,
            quality=quality,
            uniqueness_score=float(asset_data["uniqueness_score"]),
            market_demand=float(asset_data["market_demand"]),
        )
        self.valuation_engine.register_asset(asset)
        return {
            "status": "success",
            "asset_id": asset_id,
            "message": "Asset registered in valuation engine; not listed, sold or verified",
        }

    def issue_bond(self, bond_params: Dict) -> Dict:
        """Issue new liquidity bond for data asset.
        
        Args:
            bond_params: Bond configuration
            
        Returns:
            Bond details
        """
        bond = self.bond_manager.create_bond(
            data_asset_id=bond_params["asset_id"],
            principal_amount=bond_params["amount"],
            interest_rate=bond_params.get("interest_rate", 0.05),
            maturity_days=bond_params.get("maturity_days", 90),
            issuer=bond_params["issuer"]
        )
        
        return {
            "status": "success",
            "bond_id": bond.bond_id,
            "principal": bond.principal_amount,
            "interest_rate": bond.interest_rate,
            "maturity_date": bond.maturity_date.isoformat()
        }
    
    def get_asset_value(self, asset_id: str) -> Dict:
        """Get current valuation of data asset.
        
        Args:
            asset_id: Asset identifier
            
        Returns:
            Valuation details
        """
        return self.valuation_engine.get_monetization_potential(asset_id)
    
    def list_active_bonds(self) -> List[Dict]:
        """List all active liquidity bonds.
        
        Returns:
            List of active bonds
        """
        from src.core.liquidity_bonds import BondStatus
        bonds = self.bond_manager.list_bonds(status=BondStatus.ACTIVE)
        
        return [
            {
                "bond_id": bond.bond_id,
                "asset_id": bond.data_asset_id,
                "current_value": bond.calculate_value(),
                "status": bond.status.value
            }
            for bond in bonds
        ]
    
    def get_portfolio_summary(self) -> Dict:
        """Get summary of entire monetization portfolio.
        
        Returns:
            Portfolio metrics
        """
        total_bond_value = self.bond_manager.calculate_total_value()
        
        return {
            "total_assets": len(self.valuation_engine.assets),
            "total_bonds": len(self.bond_manager.bonds),
            "portfolio_value": total_bond_value,
            "timestamp": datetime.utcnow().isoformat()
        }
