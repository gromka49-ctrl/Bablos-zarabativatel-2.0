from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LeadMemory:
    lead_id: str
    facts: dict[str, str] = field(default_factory=dict)
    preferences: dict[str, str] = field(default_factory=dict)
    objections: list[str] = field(default_factory=list)
    commitments: list[str] = field(default_factory=list)
    messages: list[dict[str, str]] = field(default_factory=list)
    corrections: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def remember_correction(self, correction: str) -> None:
        if correction and correction not in self.corrections:
            self.corrections.append(correction)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def context(self) -> dict:
        return {
            "facts": self.facts,
            "preferences": self.preferences,
            "objections": self.objections,
            "commitments": self.commitments,
            "corrections": self.corrections,
            "recent_messages": self.messages[-20:],
        }
