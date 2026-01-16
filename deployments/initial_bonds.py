"""Initial Liquidity Bond Deployment Script.

Deploys first production bonds for enterprise customers.
"""

import asyncio
from datetime import datetime, timedelta
from src.core.liquidity_bonds import LiquidityBondManager, BondStatus
from src.core.data_valuation import DataValuationEngine, DataAsset, DataQuality
from src.api.monetization_api import MonetizationAPI


class ProductionBondDeployment:
    """Manages production bond deployment."""
    
    def __init__(self):
        self.bond_manager = LiquidityBondManager()
        self.valuation_engine = DataValuationEngine()
        self.api = MonetizationAPI(self.bond_manager, self.valuation_engine)
    
    def deploy_enterprise_bonds(self) -> dict:
        """Deploy initial enterprise liquidity bonds.
        
        Returns:
            Deployment summary with bond details
        """
        bonds = []
        
        # Bond 1: Enterprise Customer Data
        asset1 = DataAsset(
            asset_id="ENT-DATA-001",
            name="Enterprise Customer Profiles",
            description="High-quality B2B customer data with enrichment",
            data_type="structured",
            volume=50000,
            quality=DataQuality.PREMIUM,
            uniqueness_score=0.92,
            market_demand=0.95
        )
        self.valuation_engine.register_asset(asset1)
        
        bond1 = self.bond_manager.create_bond(
            data_asset_id="ENT-DATA-001",
            principal_amount=250000.00,
            interest_rate=0.08,  # 8% annual
            maturity_days=180,
            issuer="Enterprise-Alpha"
        )
        bonds.append(bond1)
        
        # Bond 2: Transaction Analytics Data
        asset2 = DataAsset(
            asset_id="TXN-DATA-002",
            name="E-commerce Transaction Analytics",
            description="Real-time transaction data with behavioral patterns",
            data_type="time-series",
            volume=1000000,
            quality=DataQuality.HIGH,
            uniqueness_score=0.88,
            market_demand=0.90
        )
        self.valuation_engine.register_asset(asset2)
        
        bond2 = self.bond_manager.create_bond(
            data_asset_id="TXN-DATA-002",
            principal_amount=500000.00,
            interest_rate=0.07,  # 7% annual
            maturity_days=365,
            issuer="Enterprise-Beta"
        )
        bonds.append(bond2)
        
        # Bond 3: User Behavior Intelligence
        asset3 = DataAsset(
            asset_id="UBI-DATA-003",
            name="User Behavior Intelligence",
            description="ML-enriched user behavior patterns and predictions",
            data_type="events",
            volume=2500000,
            quality=DataQuality.PREMIUM,
            uniqueness_score=0.95,
            market_demand=0.93
        )
        self.valuation_engine.register_asset(asset3)
        
        bond3 = self.bond_manager.create_bond(
            data_asset_id="UBI-DATA-003",
            principal_amount=750000.00,
            interest_rate=0.09,  # 9% annual
            maturity_days=270,
            issuer="Enterprise-Gamma"
        )
        bonds.append(bond3)
        
        # Bond 4: Financial Services Data
        asset4 = DataAsset(
            asset_id="FIN-DATA-004",
            name="Financial Services Analytics",
            description="Anonymized financial transaction and credit data",
            data_type="structured",
            volume=100000,
            quality=DataQuality.PREMIUM,
            uniqueness_score=0.97,
            market_demand=0.98
        )
        self.valuation_engine.register_asset(asset4)
        
        bond4 = self.bond_manager.create_bond(
            data_asset_id="FIN-DATA-004",
            principal_amount=1000000.00,
            interest_rate=0.10,  # 10% annual
            maturity_days=365,
            issuer="Enterprise-Delta"
        )
        bonds.append(bond4)
        
        # Bond 5: Healthcare Analytics (HIPAA-compliant)
        asset5 = DataAsset(
            asset_id="HLT-DATA-005",
            name="Healthcare Analytics Data",
            description="De-identified healthcare outcomes and treatment data",
            data_type="structured",
            volume=75000,
            quality=DataQuality.PREMIUM,
            uniqueness_score=0.99,
            market_demand=0.96
        )
        self.valuation_engine.register_asset(asset5)
        
        bond5 = self.bond_manager.create_bond(
            data_asset_id="HLT-DATA-005",
            principal_amount=850000.00,
            interest_rate=0.11,  # 11% annual
            maturity_days=180,
            issuer="Enterprise-Epsilon"
        )
        bonds.append(bond5)
        
        # Calculate portfolio metrics
        total_principal = sum(bond.principal_amount for bond in bonds)
        total_value = self.bond_manager.calculate_total_value()
        
        return {
            "deployment_date": datetime.utcnow().isoformat(),
            "total_bonds": len(bonds),
            "total_principal": total_principal,
            "current_portfolio_value": total_value,
            "bonds": [
                {
                    "bond_id": bond.bond_id,
                    "asset_id": bond.data_asset_id,
                    "principal": bond.principal_amount,
                    "interest_rate": bond.interest_rate,
                    "maturity_days": (bond.maturity_date - datetime.utcnow()).days,
                    "issuer": bond.issuer,
                    "current_value": bond.calculate_value()
                }
                for bond in bonds
            ],
            "status": "deployed"
        }


if __name__ == "__main__":
    deployment = ProductionBondDeployment()
    result = deployment.deploy_enterprise_bonds()
    
    print("="*60)
    print("LIQUIDITY BOND DEPLOYMENT - PRODUCTION LAUNCH")
    print("="*60)
    print(f"Deployment Date: {result['deployment_date']}")
    print(f"Total Bonds Issued: {result['total_bonds']}")
    print(f"Total Principal: ${result['total_principal']:,.2f}")
    print(f"Portfolio Value: ${result['current_portfolio_value']:,.2f}")
    print("\nBond Details:")
    print("-"*60)
    
    for i, bond in enumerate(result['bonds'], 1):
        print(f"\nBond #{i}")
        print(f"  ID: {bond['bond_id']}")
        print(f"  Asset: {bond['asset_id']}")
        print(f"  Principal: ${bond['principal']:,.2f}")
        print(f"  Rate: {bond['interest_rate']*100:.1f}%")
        print(f"  Maturity: {bond['maturity_days']} days")
        print(f"  Issuer: {bond['issuer']}")
        print(f"  Current Value: ${bond['current_value']:,.2f}")
    
    print("\n" + "="*60)
    print("STATUS: PRODUCTION DEPLOYMENT SUCCESSFUL")
    print("="*60)
