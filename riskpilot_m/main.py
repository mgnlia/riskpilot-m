from __future__ import annotations

import os
import sys
from dotenv import load_dotenv
from mistralai import Mistral

SYSTEM_PROMPT = (
    "You are RiskPilot-M, a concise risk analysis copilot. "
    "Given an objective, identify top risks and mitigations."
)


def run() -> None:
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    if not api_key:
        print("ERROR: MISTRAL_API_KEY is not set. Add it to .env or environment.")
        sys.exit(1)

    client = Mistral(api_key=api_key)

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

    content = response.choices[0].message.content
    if isinstance(content, list):
        print("\n".join(str(part) for part in content))
    else:
        print(content)


if __name__ == "__main__":
    run()
