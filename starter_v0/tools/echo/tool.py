from __future__ import annotations

from typing import Any


def echo(text: str = "") -> dict[str, Any]:
    """Simple echo tool used for testing and eval cases.

    Returns the provided text back in a structured dict so the agent can use it
    in further steps.
    """
    return {"tool": "echo", "status": "ok", "echoed": text}
