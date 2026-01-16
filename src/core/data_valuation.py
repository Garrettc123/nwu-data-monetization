"""Data Valuation Engine

Assesses data value based on quality, uniqueness, and market demand.
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class DataQuality(Enum):
    """Data quality tiers."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PREMIUM = 4


@dataclass
class DataAsset:
    """Represents a monetizable data asset."""
    asset_id: str
    name: str
    description: str
    data_type: str
    volume: int  # Records/GB
    quality: DataQuality
    uniqueness_score: float  # 0-1
    market_demand: float  # 0-1
    
    def calculate_base_value(self) -> float:
        """Calculate base monetary value of data asset."""
        # Base rate per unit based on quality
        quality_multiplier = {
            DataQuality.LOW: 0.01,
            DataQuality.MEDIUM: 0.05,
            DataQuality.HIGH: 0.15,
            DataQuality.PREMIUM: 0.50
        }
        
        base_rate = quality_multiplier[self.quality]
        volume_value = self.volume * base_rate
        
        # Apply uniqueness and demand multipliers
        uniqueness_bonus = 1 + (self.uniqueness_score * 2)
        demand_bonus = 1 + (self.market_demand * 3)
        
        return volume_value * uniqueness_bonus * demand_bonus


class DataValuationEngine:
    """Engine for valuating and monetizing data assets."""
    
    def __init__(self):
        self.assets: Dict[str, DataAsset] = {}
        self.market_rates: Dict[str, float] = {}
    
    def register_asset(self, asset: DataAsset) -> None:
        """Register new data asset for monetization."""
        self.assets[asset.asset_id] = asset
    
    def valuate_asset(self, asset_id: str) -> float:
        """Calculate current market value of asset."""
        asset = self.assets.get(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        return asset.calculate_base_value()
    
    def get_monetization_potential(self, asset_id: str) -> Dict[str, float]:
        """Calculate monetization potential and ROI."""
        value = self.valuate_asset(asset_id)
        asset = self.assets[asset_id]
        
        return {
            "current_value": value,
            "monthly_revenue_potential": value * 0.05,
            "annual_revenue_potential": value * 0.60,
            "roi_percentage": asset.market_demand * 100
        }
    
    def list_high_value_assets(self, min_value: float = 1000) -> List[DataAsset]:
        """List assets with value above threshold."""
        return [
            asset for asset in self.assets.values()
            if asset.calculate_base_value() >= min_value
        ]
