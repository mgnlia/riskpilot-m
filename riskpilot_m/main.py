from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from mistralai import Mistral

from riskpilot_m.health_factor import evaluate_position, load_mock_positions

SYSTEM_PROMPT = (
    "You are RiskPilot-M, a concise risk analysis copilot. "
    "Given an objective, identify top execution risks and mitigations."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "score_risk",
            "description": "Return a severity score (1-10) for a risk statement.",
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
            "description": "Return an immediate next action for a given blocker.",
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
    blocker = str(args.get("blocker", "Unknown blocker"))
    deadline = int(args.get("deadline_hours", 24))
    return {
        "blocker": blocker,
        "next_action": f"Assign owner now, execute within {deadline}h, and post proof artifact.",
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
    print("-" * 70)
    for p in positions:
        r = evaluate_position(p)
        print(f"{r.wallet:<12} {r.health_factor:>6.2f} {r.risk_band:>10}  {r.next_action}")


def run_basic(client: Mistral, model: str) -> None:
    user_prompt = (
        "We are entering a 48-hour critical registration window for a hackathon. "
        "List 5 execution risks and one mitigation for each."
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
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Assess this situation: registration requires a wallet verification and deadline is within 48h. "
                "Use tools to score key risks and propose immediate actions, then summarize in a short action plan."
            ),
        },
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

    print("Tool loop ended after max iterations without final assistant response.")


def _build_client_or_exit() -> tuple[Mistral, str]:
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY is not set. Add it to .env or environment.")
        sys.exit(1)
    return Mistral(api_key=api_key), model


def run() -> None:
    parser = argparse.ArgumentParser(description="RiskPilot-M baseline runner")
    parser.add_argument("--mode", choices=["basic", "tool-loop", "health-demo"], default="basic")
    args = parser.parse_args()

    if args.mode == "health-demo":
        run_health_demo()
        return

    client, model = _build_client_or_exit()
    if args.mode == "tool-loop":
        run_tool_loop(client, model)
    else:
        run_basic(client, model)


if __name__ == "__main__":
    run()
