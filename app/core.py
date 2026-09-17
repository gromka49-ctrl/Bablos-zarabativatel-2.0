from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .memory import LeadMemory
from .safety import SafetyResult, check_action, check_message
from .sales import SalesEngine, SalesStage


class Action(str, Enum):
    RESEARCH = "research"
    DRAFT_FIRST_OUTREACH = "first_outreach"
    SEND = "send"
    REPLY = "reply"
    DISCOUNT = "discount"
    FINAL_PRICE = "final_price"
    CONTRACT = "contract"
    REFUND = "refund"
    LEGAL = "legal_or_complaint"


@dataclass
class Evidence:
    source: str
    claim: str
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentContext:
    lead_id: str
    stage: SalesStage = SalesStage.NEW
    memory: LeadMemory = field(default_factory=lambda: LeadMemory(lead_id=""))
    evidence: list[Evidence] = field(default_factory=list)


class ClaimGuard:
    """Prevents the agent from presenting unsupported research as fact."""

    def verify(self, claim: str, evidence: list[Evidence]) -> bool:
        normalized = claim.strip().lower()
        return any(normalized in item.claim.lower() for item in evidence if item.confidence >= 0.6)


class SalesOrchestrator:
    """Own decision layer: policy first, LLM second."""

    def __init__(self, engine: SalesEngine | None = None) -> None:
        self.engine = engine or SalesEngine()
        self.claim_guard = ClaimGuard()

    def gate(self, action: str, text: str = "") -> SafetyResult:
        message_check = check_message(text) if text else SafetyResult(True, False, "no message")
        if not message_check.allowed:
            return message_check
        return check_action(action)

    def next_step(self, ctx: AgentContext, action: str, text: str = "") -> dict[str, Any]:
        safety = self.gate(action, text)
        if not safety.allowed:
            ctx.stage = SalesStage.SUPPRESSED
            return {"decision": "stop", "reason": safety.reason, "stage": ctx.stage.value}
        if safety.needs_human:
            ctx.stage = SalesStage.ESCALATED
            return {"decision": "human_approval", "reason": safety.reason, "stage": ctx.stage.value}
        return {"decision": "continue", "reason": safety.reason, "stage": ctx.stage.value}
