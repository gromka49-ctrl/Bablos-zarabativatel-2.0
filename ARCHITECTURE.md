# AI Sales OS 2.0 — Original Architecture

This project uses open-source sales-agent projects as research references, but the product architecture and core orchestration are being implemented independently for this repository.

## Design goals

- Local-first LLM through Ollama.
- Provider abstraction so the model can be changed without rewriting the sales engine.
- Persistent per-lead memory: facts, preferences, objections, commitments, and conversation history.
- Explicit sales state machine instead of relying on a prompt to decide the whole workflow.
- Tool-calling layer for research, CRM, scheduling, and outreach.
- Evidence-aware answers: external claims must carry sources or be marked uncertain.
- Human approval gates for first outreach, pricing/discounts, contracts, refunds, and unusual requests.
- Opt-out/suppression handling and escalation for complaints or legal threats.
- Full audit trail of decisions and external actions.
- Transparent AI identity: the assistant does not impersonate a human.

## Core loop

1. Intake lead.
2. Research company and contact using permitted public sources.
3. Build an evidence packet.
4. Qualify lead against the user's offer.
5. Generate a draft and rationale.
6. Ask for approval when the policy requires it.
7. Send only through an approved connector.
8. Parse the reply into structured intent, objections, facts, and next action.
9. Update memory and sales state.
10. Continue, schedule, escalate, or close according to policy.
11. Learn from explicit human corrections and outcomes.

## Ownership

The final implementation in this repository is not a fork of another product. Where external MIT-licensed code is ever copied verbatim, its license and copyright notices will be preserved. Otherwise, external projects are treated as architectural references and the implementation is written for this product.
