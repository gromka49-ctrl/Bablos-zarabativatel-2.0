from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SalesStage(StrEnum):
    NEW = "new"
    RESEARCHED = "researched"
    QUALIFIED = "qualified"
    OUTREACH_PENDING = "outreach_pending"
    CONTACTED = "contacted"
    DISCOVERY = "discovery"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    SCHEDULED = "scheduled"
    WON = "won"
    LOST = "lost"
    SUPPRESSED = "suppressed"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class SalesDecision:
    stage: SalesStage
    next_action: str
    requires_human: bool
    reason: str


class SalesEngine:
    """Deterministic workflow policy around the model, rather than a prompt-only agent."""

    HUMAN_ACTIONS = {
        "first_outreach",
        "discount",
        "final_price",
        "contract",
        "refund",
        "legal_or_complaint",
    }

    def decide(self, stage: SalesStage, action: str, *, opted_out: bool = False) -> SalesDecision:
        if opted_out:
            return SalesDecision(SalesStage.SUPPRESSED, "stop_contact", False, "lead opted out")
        if action in self.HUMAN_ACTIONS:
            return SalesDecision(stage, action, True, "policy requires human approval")
        return SalesDecision(stage, action, False, "routine action")
