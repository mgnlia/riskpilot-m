# RiskPilot-M — 60s Demo Script + Shot List (Phase-1)

## Narrative spine
**From risk confusion to one clear action in under a minute.**

## Total runtime: 60 seconds

### 0:00–0:08 — Hook (Problem)
**Voiceover:** “In DeFi, wallets get liquidated because risk signals arrive fast but decisions are slow.”
**Shot:** Title slide + one sentence overlay: *RiskPilot-M: liquidation risk copilot*.

### 0:08–0:20 — Scoring credibility
**Voiceover:** “RiskPilot-M computes health factors deterministically and classifies each wallet by urgency.”
**Shot:** Terminal run of `uv run python -m riskpilot_m.main --mode health-demo` showing risk bands.

### 0:20–0:36 — Operator clarity
**Voiceover:** “The interface ranks wallets and highlights the single highest-priority position first.”
**Shot:** Web demo table (`index.html`) or `--mode demo-ui`; zoom on top-priority wallet row.

### 0:36–0:50 — AI action layer
**Voiceover:** “Then Mistral generates immediate mitigation actions—repay debt, add collateral, or reduce leverage—based on tool outputs.”
**Shot:** `uv run python -m riskpilot_m.main --mode tool-loop`; highlight recommended next action text.

### 0:50–1:00 — Close
**Voiceover:** “RiskPilot-M gives DeFi operators decision velocity: identify risk early, act clearly, and reduce liquidation exposure.”
**Shot:** End card with repo URL + live demo URL.

## Capture checklist
- 1080p recording, terminal font >=16pt
- Keep command outputs visible (no cuts during key results)
- Add subtitles for commands and final recommendation
- Export MP4, upload unlisted, add URL to README
