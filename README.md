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

### 5) Run D-7 health-factor demo (mock on-chain data)
```bash
uv run python -m riskpilot_m.main --mode health-demo
```

## Current scope
- Minimal Mistral chat baseline
- Tool-calling spike with two local functions:
  - `score_risk`
  - `suggest_next_action`
- **D-7 artifact:** health-factor scoring engine over mock on-chain positions

## Project layout
- `riskpilot_m/main.py` — CLI entrypoint and Mistral loops
- `riskpilot_m/health_factor.py` — risk/health scoring logic
- `data/mock_positions.json` — sample position data for demo
- `docs/strategy-prize-matrix-correction.md` — corrected target prioritization
- `docs/feb25-briefing-plan.md` — briefing checklist

## Next milestone
- D-6: lightweight demo UI (Streamlit or rich CLI) for score + next action panels.
