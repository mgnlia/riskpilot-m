from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from riskpilot_m.health_factor import evaluate_position, load_mock_positions


def run_demo_cli() -> None:
    console = Console()
    positions = load_mock_positions("data/mock_positions.json")

    table = Table(title="RiskPilot-M — Health Factor Overview")
    table.add_column("Wallet", style="cyan")
    table.add_column("Health Factor", justify="right")
    table.add_column("Risk Band", justify="right")
    table.add_column("Next Action")

    highest = None
    for p in positions:
        r = evaluate_position(p)
        if highest is None or r.health_factor < highest.health_factor:
            highest = r
        style = {
            "CRITICAL": "bold red",
            "HIGH": "yellow",
            "MEDIUM": "magenta",
            "LOW": "green",
        }.get(r.risk_band, "white")
        table.add_row(r.wallet, f"{r.health_factor:.2f}", f"[{style}]{r.risk_band}[/{style}]", r.next_action)

    console.print(table)
    if highest:
        console.print(
            Panel.fit(
                f"Priority wallet: [bold]{highest.wallet}[/bold]\n"
                f"HF: [bold]{highest.health_factor:.2f}[/bold] | Risk: [bold]{highest.risk_band}[/bold]\n"
                f"Action: {highest.next_action}",
                title="Immediate Operator Recommendation",
                border_style="red" if highest.risk_band in {"CRITICAL", "HIGH"} else "green",
            )
        )
