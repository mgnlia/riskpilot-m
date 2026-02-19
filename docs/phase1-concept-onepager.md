# RiskPilot-M — 1-Page Concept (Phase-1)

## Title
**RiskPilot-M: A Mistral-Powered Liquidation Risk Copilot for DeFi Wallet Operators**

## One-line concept
RiskPilot-M turns noisy DeFi position data into a clear, prioritized action queue so users can prevent liquidations before they happen.

## Problem
Liquidation risk is time-sensitive, but most DeFi users and operators still rely on fragmented dashboards and manual interpretation. By the time risk becomes obvious, response windows are often too small.

## Solution
RiskPilot-M combines deterministic risk scoring with Mistral reasoning to produce immediate, explainable next actions:
1. Read wallet positions (collateral, debt, liquidation threshold)
2. Compute health factor and classify risk (CRITICAL/HIGH/MEDIUM/LOW)
3. Prioritize wallets by urgency
4. Generate concrete mitigation actions (repay debt, add collateral, reduce leverage)

## Why this matters
- **Faster response:** High-risk wallets are surfaced instantly
- **Operational clarity:** Judges and users get one obvious “what to do next” recommendation
- **Explainability:** Deterministic health-factor math is visible and auditable

## Product surface shown to judges
- **Web demo (`index.html`)**: static, no setup, immediate risk table and top-priority wallet
- **CLI demo (`--mode demo-ui`)**: operator-facing prioritization workflow
- **AI loop (`--mode tool-loop`)**: Mistral-guided mitigation recommendations grounded in tool outputs

## Mistral usage
- Tool-calling orchestration for risk scoring and recommendation generation
- Concise, action-first narrative suitable for incident-like decision windows

## Technical approach
- `riskpilot_m/health_factor.py` — deterministic HF scoring
- `riskpilot_m/main.py` — Mistral loop and tool orchestration
- `riskpilot_m/demo_cli.py` — terminal triage UI
- `data/mock_positions.json` + synced `index.html` dataset — 8-wallet scenario coverage

## Differentiation
Unlike generic analytics dashboards, RiskPilot-M is built around **decision velocity**: who is at risk *now* and what action reduces liquidation probability fastest.

## Scope for hackathon phase
- MVP complete for deterministic scoring + AI-guided actioning
- Public demo endpoint + source repo
- Submission copy aligned to judging criteria

## Next steps
- Replace mock ingestion with on-chain adapters
- Add alert channels (Discord/Telegram/webhooks)
- Add scenario simulation ("If I repay X, HF becomes Y")
