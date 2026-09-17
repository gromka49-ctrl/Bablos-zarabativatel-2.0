from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class OllamaConfig:
    base_url: str = "http://127.0.0.1:11434"
    model: str = "qwen2.5:7b"
    timeout: float = 120.0


class LocalLLM:
    """Small provider boundary around Ollama; the sales engine never talks to Ollama directly."""

    def __init__(self, config: OllamaConfig | None = None) -> None:
        self.config = config or OllamaConfig()

    async def chat(self, messages: list[dict[str, str]], *, json_mode: bool = False) -> str:
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "stream": False,
        }
        if json_mode:
            payload["format"] = "json"
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(f"{self.config.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
        return str(data["message"]["content"])

    async def structured(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        text = await self.chat(messages, json_mode=True)
        return json.loads(text)
