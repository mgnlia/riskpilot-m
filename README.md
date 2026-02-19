# RiskPilot-M

Baseline scaffold for the Mistral AI Worldwide Hackathon 2026.

## Objective
Build a risk-focused agent prototype using Mistral APIs with a runnable local loop before the hackathon start.

## Quickstart

### 1) Install dependencies
```bash
uv sync
```

### 2) Configure environment
```bash
cp .env.example .env
# then set MISTRAL_API_KEY
```

### 3) Run baseline Mistral loop
```bash
uv run python -m riskpilot_m.main --mode basic
```

### 4) Run tool-calling spike loop
```bash
uv run python -m riskpilot_m.main --mode tool-loop
```

## Current scope
- Minimal Mistral chat baseline
- Tool-calling spike with two local functions:
  - `score_risk`
  - `suggest_next_action`

## Next milestone
- Expand toolset for domain-specific risk scoring and timeline simulation.
