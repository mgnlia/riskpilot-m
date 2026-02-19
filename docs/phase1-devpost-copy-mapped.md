# RiskPilot-M — Devpost Copy (Mapped to Judging Criteria)

## Project Title
RiskPilot-M

## Tagline
A Mistral-powered DeFi liquidation risk copilot that converts wallet health signals into immediate mitigation actions.

## Elevator Pitch
RiskPilot-M helps DeFi users and operators prevent liquidations by combining deterministic health-factor scoring with Mistral tool-calling recommendations. Instead of scanning fragmented dashboards, users get a prioritized risk queue and concrete next steps in seconds.

---

## 1) Problem & Importance (Judge criterion: relevance / pain point)
Liquidations happen fast. Many users only notice danger when collateral ratios are already near threshold. Existing tooling often surfaces metrics, not decisions.

**Why this matters:** delayed response directly causes avoidable losses.

## 2) Solution Quality (Judge criterion: clarity / usability / execution)
RiskPilot-M provides a simple operational flow:
- ingest position data
- compute health factor and risk band
- rank wallets by urgency
- output immediate mitigation actions

The result is a judge-friendly and operator-friendly workflow focused on “what to do now.”

## 3) Technical Implementation (Judge criterion: technical depth)
- Deterministic engine for health factor and risk classification
- Mistral-driven tool-calling loop for context-aware action recommendations
- Multi-surface demo: static web view + CLI triage + AI loop
- 8-wallet dataset coverage for richer scenario realism

## 4) Use of Mistral (Judge criterion: platform leverage)
Mistral is used as the decision-support layer on top of deterministic risk tools:
- interprets scored risk context
- generates concise, actionable recommendations
- supports fast operator triage in time-sensitive conditions

## 5) Innovation / Differentiation (Judge criterion: originality)
RiskPilot-M is not just a dashboard. It is a **risk-action copilot** optimized for decision velocity:
- immediate wallet prioritization
- actionable mitigations, not just metrics
- clear bridge from risk detection to operator execution

## 6) Impact & Next Steps (Judge criterion: real-world potential)
Near-term roadmap:
- on-chain data adapters
- alert integrations (Discord/Telegram/webhooks)
- what-if simulation (repay/add-collateral scenarios)

Potential impact: reduce avoidable liquidation losses for active DeFi participants.

---

## Demo Links (to fill)
- GitHub Repository: https://github.com/mgnlia/riskpilot-m
- Live Demo (Vercel): [PENDING VERSEL URL]
- Backup Live Demo: https://raw.githack.com/mgnlia/riskpilot-m/main/index.html
- Demo Video: [PENDING VIDEO URL]
