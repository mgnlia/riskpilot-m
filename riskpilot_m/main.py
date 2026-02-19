from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from mistralai import Mistral

from riskpilot_m.demo_cli import run_demo_cli
from riskpilot_m.health_factor import evaluate_position, load_mock_positions

SYSTEM_PROMPT = (
    "You are RiskPilot-M, a DeFi liquidation-risk copilot. "
    "Given wallet position context, produce concise, operator-ready mitigations."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "score_risk",
            "description": "Return a severity score (1-10) for a DeFi liquidation risk statement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "risk": {"type": "string", "description": "Risk statement"},
                    "impact": {"type": "integer", "minimum": 1, "maximum": 5},
                    "likelihood": {"type": "integer", "minimum": 1, "maximum": 5},
                },
                "required": ["risk", "impact", "likelihood"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_next_action",
            "description": "Return immediate DeFi mitigation actions for a risky position.",
            "parameters": {
                "type": "object",
                "properties": {
                    "blocker": {"type": "string"},
                    "deadline_hours": {"type": "integer", "minimum": 1},
                },
                "required": ["blocker", "deadline_hours"],
            },
        },
    },
]


def _score_risk(args: dict[str, Any]) -> dict[str, Any]:
    impact = int(args.get("impact", 3))
    likelihood = int(args.get("likelihood", 3))
    score = max(1, min(10, round((impact * likelihood) / 2.5)))
    return {"risk": args.get("risk", "unknown"), "score": score, "method": "impact*likelihood/2.5"}


def _suggest_next_action(args: dict[str, Any]) -> dict[str, Any]:
    blocker = str(args.get("blocker", "Unknown risk"))
    deadline = int(args.get("deadline_hours", 24))
    return {
        "blocker": blocker,
        "next_action": (
            f"Within {deadline}h: (1) repay debt or add collateral, "
            f"(2) reduce leverage, (3) set liquidation alert thresholds."
        ),
    }


def _run_local_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "score_risk":
        return _score_risk(args)
    if name == "suggest_next_action":
        return _suggest_next_action(args)
    return {"error": f"Unknown tool: {name}"}


def _extract_content(message: Any) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, list):
        return "\n".join(str(part) for part in content)
    return str(content)


def run_health_demo() -> None:
    print("RiskPilot-M D-7: health factor scoring demo (mock on-chain data)\n")
    positions = load_mock_positions("data/mock_positions.json")
    print(f"{'wallet':<12} {'HF':>6} {'risk':>10}  next_action")
    print("-" * 72)
    for p in positions:
        r = evaluate_position(p)
        print(f"{r.wallet:<12} {r.health_factor:>6.2f} {r.risk_band:>10}  {r.next_action}")


def run_basic(client: Mistral, model: str) -> None:
    user_prompt = (
        "Given a wallet with collateral=$4200, debt=$3900, liquidation_threshold=0.80, "
        "explain liquidation risk in 3 bullets and include one immediate mitigation."
    )
    response = client.chat.complete(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    print(_extract_content(response.choices[0].message))


def run_tool_loop(client: Mistral, model: str) -> None:
    # Use the riskiest mock position as the demo scenario.
    positions = load_mock_positions("data/mock_positions.json")
    scored = [evaluate_position(p) for p in positions]
    worst = sorted(scored, key=lambda x: x.health_factor)[0]

    user_content = (
        "Analyze this DeFi position and produce an operator action plan. "
        f"Wallet={worst.wallet}, health_factor={worst.health_factor:.2f}, "
        f"risk_band={worst.risk_band}, current_recommendation='{worst.next_action}'. "
        "Use tools to: (a) score liquidation severity, (b) propose immediate next action in <=24h, "
        "then output a concise 4-bullet runbook."
    )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    for _ in range(3):
        response = client.chat.complete(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )
        message = response.choices[0].message
        tool_calls = getattr(message, "tool_calls", None) or []

        if not tool_calls:
            print(_extract_content(message))
            return

        messages.append(
            {
                "role": "assistant",
                "content": _extract_content(message),
                "tool_calls": [
                    {
                        "id": getattr(tc, "id", None),
                        "type": getattr(tc, "type", "function"),
                        "function": {
                            "name": getattr(getattr(tc, "function", None), "name", ""),
                            "arguments": getattr(getattr(tc, "function", None), "arguments", "{}"),
                        },
                    }
                    for tc in tool_calls
                ],
            }
        )

        for tc in tool_calls:
            fn = getattr(tc, "function", None)
            name = getattr(fn, "name", "")
            raw_args = getattr(fn, "arguments", "{}") or "{}"
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
            except json.JSONDecodeError:
                args = {"raw": str(raw_args)}
            result = _run_local_tool(name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": getattr(tc, "id", ""),
                    "name": name,
                    "content": json.dumps(result),
                }
            )

    print(
        "Tool loop reached the 3-turn demo cap. This is expected in judge demos; rerun to continue iteration."
    )


def _build_client_or_exit() -> tuple[Mistral, str]:
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY is not set. Add it to .env or environment.")
        sys.exit(1)
    return Mistral(api_key=api_key), model


def run() -> None:
    parser = argparse.ArgumentParser(description="RiskPilot-M baseline runner")
    parser.add_argument("--mode", choices=["basic", "tool-loop", "health-demo", "demo-ui"], default="basic")
    args = parser.parse_args()

    if args.mode == "health-demo":
        run_health_demo()
        return

    if args.mode == "demo-ui":
        run_demo_cli()
        return

    client, model = _build_client_or_exit()
    if args.mode == "tool-loop":
        run_tool_loop(client, model)
    else:
        run_basic(client, model)


if __name__ == "__main__":
    run()
