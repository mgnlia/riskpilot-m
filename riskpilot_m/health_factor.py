from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Position:
    wallet: str
    collateral_usd: float
    debt_usd: float
    liquidation_threshold: float  # 0..1


@dataclass
class HealthResult:
    wallet: str
    health_factor: float
    risk_band: str
    next_action: str


def compute_health_factor(collateral_usd: float, debt_usd: float, liquidation_threshold: float) -> float:
    if debt_usd <= 0:
        return 999.0
    return (collateral_usd * liquidation_threshold) / debt_usd


def classify_risk(health_factor: float) -> tuple[str, str]:
    if health_factor < 1.0:
        return "CRITICAL", "Repay debt or add collateral immediately."
    if health_factor < 1.2:
        return "HIGH", "Reduce leverage now; monitor every block interval."
    if health_factor < 1.5:
        return "MEDIUM", "Set alerts and prepare top-up collateral."
    return "LOW", "Maintain position; periodic monitoring only."


def evaluate_position(p: Position) -> HealthResult:
    hf = compute_health_factor(p.collateral_usd, p.debt_usd, p.liquidation_threshold)
    band, action = classify_risk(hf)
    return HealthResult(wallet=p.wallet, health_factor=hf, risk_band=band, next_action=action)


def load_mock_positions(path: str | Path) -> list[Position]:
    payload: list[dict[str, Any]] = json.loads(Path(path).read_text())
    out: list[Position] = []
    for item in payload:
        out.append(
            Position(
                wallet=item["wallet"],
                collateral_usd=float(item["collateral_usd"]),
                debt_usd=float(item["debt_usd"]),
                liquidation_threshold=float(item.get("liquidation_threshold", 0.8)),
            )
        )
    return out
