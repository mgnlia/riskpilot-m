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
uv run python -m riskpilot_m.main
```

## Notes
- Uses `uv` for dependency management and execution.
- Keeps the baseline intentionally small for rapid iteration.
- Next milestone: tool-calling loop + domain-specific risk scoring prompt pack.
