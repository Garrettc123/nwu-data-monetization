# NWU Data Monetization Engine

Python valuation and liquidity-bond prototype. The repository contains a `DataValuationEngine`, `LiquidityBondManager`, and a class-level `MonetizationAPI`; its architecture describes REST endpoints as planned. A Python method returning a value is **not** evidence that an HTTP API, commercial listing, blockchain settlement, or real customer revenue exists.

## Source-of-truth boundaries

| Concern | Existing repository | Status |
| --- | --- | --- |
| Asset valuation and in-memory registration | This repository | Implementation source; no marketplace rights verification |
| Scenario forecast and React dashboard | [nwu-cashflow-model](https://github.com/Garrettc123/nwu-cashflow-model) | Model assumptions, not payment receipts |
| NWU smart contracts and signed mesh-health integration | [nwu-protocol](https://github.com/Garrettc123/nwu-protocol) | Independent code and approval gates; verify deployment receipts |
| Actual customer payments, fulfillment and governed outbound | [garcar-revenue-os](https://github.com/Garrettc123/garcar-revenue-os) | Authoritative revenue/evidence boundary |

**No automatic cashflow sync is currently claimed.** Only confirmed Stripe/ledger receipts can be counted as collected revenue. Calculated data value, bond principal, token issuance, prospective yields, and simulated royalties cannot be treated as payments or booked cash.

## Development

```bash
python -m pytest tests/
```

The registration adapter accepts a complete data-asset payload, validates it, and registers the asset in the valuation engine. Registration is not a market listing or evidence of lawful resale rights. Additional licensing/privacy/compliance controls are required before commercial ingestion or bond activity.

## Identity collision

The cashflow README uses *New World Upperclass* for NWU; the `nwu-protocol` README currently uses *Neural Workflow Unification*. A separate NWU implementation in `garcar-autonomous-wealth-system` uses *Network-Wide Unit*. Treat these as distinct interfaces until explicitly mapped and proven compatible.
