from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyResult:
    allowed: bool
    needs_human: bool
    reason: str


STOP_WORDS = {"stop", "unsubscribe", "remove me", "do not contact", "не пишите"}
SENSITIVE_ACTIONS = {"contract", "refund", "final_price", "discount", "legal_or_complaint"}


def check_message(text: str) -> SafetyResult:
    normalized = " ".join(text.lower().split())
    if any(word in normalized for word in STOP_WORDS):
        return SafetyResult(False, False, "opt-out detected")
    return SafetyResult(True, False, "routine message")


def check_action(action: str) -> SafetyResult:
    if action in SENSITIVE_ACTIONS:
        return SafetyResult(True, True, "human approval required")
    return SafetyResult(True, False, "routine action")
