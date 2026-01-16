"""Real-time Bond Portfolio Dashboard."""

from typing import Dict, Any, List
from datetime import datetime
from src.core.liquidity_bonds import LiquidityBondManager, BondStatus
from src.core.data_valuation import DataValuationEngine


class BondDashboard:
    """Dashboard for monitoring liquidity bond portfolio."""
    
    def __init__(self, bond_manager: LiquidityBondManager, valuation_engine: DataValuationEngine):
        self.bond_manager = bond_manager
        self.valuation_engine = valuation_engine
    
    def get_portfolio_metrics(self) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics."""
        all_bonds = self.bond_manager.list_bonds()
        active_bonds = self.bond_manager.list_bonds(status=BondStatus.ACTIVE)
        
        total_principal = sum(bond.principal_amount for bond in all_bonds)
        active_value = sum(bond.calculate_value() for bond in active_bonds)
        
        # Calculate returns
        total_interest = active_value - sum(bond.principal_amount for bond in active_bonds)
        roi = (total_interest / total_principal * 100) if total_principal > 0 else 0
        
        # Status breakdown
        status_counts = {}
        for status in BondStatus:
            count = len(self.bond_manager.list_bonds(status=status))
            status_counts[status.value] = count
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_bonds": len(all_bonds),
            "active_bonds": len(active_bonds),
            "total_principal": total_principal,
            "portfolio_value": active_value,
            "accrued_interest": total_interest,
            "roi_percentage": roi,
            "status_breakdown": status_counts,
            "average_bond_size": total_principal / len(all_bonds) if all_bonds else 0
        }
    
    def get_top_performing_bonds(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing bonds by current value."""
        active_bonds = self.bond_manager.list_bonds(status=BondStatus.ACTIVE)
        
        bond_performance = [
            {
                "bond_id": bond.bond_id,
                "asset_id": bond.data_asset_id,
                "principal": bond.principal_amount,
                "current_value": bond.calculate_value(),
                "interest_earned": bond.calculate_value() - bond.principal_amount,
                "roi": ((bond.calculate_value() - bond.principal_amount) / bond.principal_amount * 100),
                "issuer": bond.issuer
            }
            for bond in active_bonds
        ]
        
        # Sort by ROI descending
        bond_performance.sort(key=lambda x: x['roi'], reverse=True)
        return bond_performance[:limit]
    
    def get_maturity_schedule(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get bonds grouped by maturity timeframe."""
        active_bonds = self.bond_manager.list_bonds(status=BondStatus.ACTIVE)
        now = datetime.utcnow()
        
        schedule = {
            "next_30_days": [],
            "next_90_days": [],
            "next_180_days": [],
            "beyond_180_days": []
        }
        
        for bond in active_bonds:
            days_to_maturity = (bond.maturity_date - now).days
            
            bond_info = {
                "bond_id": bond.bond_id,
                "maturity_date": bond.maturity_date.isoformat(),
                "days_remaining": days_to_maturity,
                "principal": bond.principal_amount,
                "expected_value": bond.calculate_value()
            }
            
            if days_to_maturity <= 30:
                schedule["next_30_days"].append(bond_info)
            elif days_to_maturity <= 90:
                schedule["next_90_days"].append(bond_info)
            elif days_to_maturity <= 180:
                schedule["next_180_days"].append(bond_info)
            else:
                schedule["beyond_180_days"].append(bond_info)
        
        return schedule
    
    def generate_report(self) -> str:
        """Generate formatted portfolio report."""
        metrics = self.get_portfolio_metrics()
        top_bonds = self.get_top_performing_bonds()
        schedule = self.get_maturity_schedule()
        
        report = []
        report.append("="*70)
        report.append("LIQUIDITY BOND PORTFOLIO REPORT")
        report.append("="*70)
        report.append(f"Generated: {metrics['timestamp']}")
        report.append("")
        
        report.append("PORTFOLIO SUMMARY")
        report.append("-"*70)
        report.append(f"Total Bonds: {metrics['total_bonds']}")
        report.append(f"Active Bonds: {metrics['active_bonds']}")
        report.append(f"Total Principal: ${metrics['total_principal']:,.2f}")
        report.append(f"Portfolio Value: ${metrics['portfolio_value']:,.2f}")
        report.append(f"Accrued Interest: ${metrics['accrued_interest']:,.2f}")
        report.append(f"Portfolio ROI: {metrics['roi_percentage']:.2f}%")
        report.append("")
        
        report.append("TOP PERFORMING BONDS")
        report.append("-"*70)
        for i, bond in enumerate(top_bonds, 1):
            report.append(f"{i}. {bond['bond_id']}")
            report.append(f"   Principal: ${bond['principal']:,.2f}")
            report.append(f"   Current Value: ${bond['current_value']:,.2f}")
            report.append(f"   Interest Earned: ${bond['interest_earned']:,.2f}")
            report.append(f"   ROI: {bond['roi']:.2f}%")
            report.append("")
        
        report.append("MATURITY SCHEDULE")
        report.append("-"*70)
        for timeframe, bonds in schedule.items():
            if bonds:
                report.append(f"{timeframe.replace('_', ' ').title()}: {len(bonds)} bonds")
                total_value = sum(b['expected_value'] for b in bonds)
                report.append(f"  Expected Value: ${total_value:,.2f}")
        
        report.append("")
        report.append("="*70)
        
        return "\n".join(report)
