# RiskPilot-M — Submission Draft (D-4)

## One-liner
RiskPilot-M is a Mistral-powered liquidation-risk copilot that turns wallet position health into immediate, prioritized mitigation actions.

## Problem
DeFi users and operators often react too late to liquidation risk because on-chain risk signals are noisy, fragmented, and difficult to operationalize quickly.

## Solution
RiskPilot-M combines deterministic health-factor scoring with Mistral-driven action planning:
1. Ingest wallet position data (mock now, on-chain adapters next)
2. Compute health factor and risk band (CRITICAL/HIGH/MEDIUM/LOW)
3. Generate actionable next-step recommendations with tool-assisted reasoning
4. Surface the highest-priority wallet in a minimal operator UI

## Why Mistral
- Fast, concise reasoning for operational triage
- Tool-calling support for structured risk scoring workflows
- Strong fit for lightweight, hackathon-speed iteration

## Demo flow (3 minutes)
1. Run health demo (`--mode health-demo`) to show deterministic scoring.
2. Run rich dashboard (`--mode demo-ui`) for operator-facing prioritization.
3. Run Mistral tool loop (`--mode tool-loop`) to show AI-generated immediate mitigation plan.

## Technical architecture
- `riskpilot_m/health_factor.py`: deterministic risk calculations
- `riskpilot_m/demo_cli.py`: lightweight terminal UI
- `riskpilot_m/main.py`: execution modes + Mistral chat/tool loop
- `data/mock_positions.json`: sample portfolio data

## Next steps
- Replace mock positions with on-chain adapters
- Add alerting hooks (webhook/Discord)
- Add scenario simulation for collateral/debt changes
