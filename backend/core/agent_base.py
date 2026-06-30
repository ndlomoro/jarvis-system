"""
J.A.R.V.I.S. Backend — Abstract base class for all agents.
"""

from __future__ import annotations

import abc
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from openai import AsyncOpenAI, APIConnectionError, APIStatusError, RateLimitError

from core.models import AgentStatus

logger = logging.getLogger("jarvis.agents")


def _load_llm_config():
    """Load LLM endpoint config from environment variables."""
    from dotenv import load_dotenv
    import os

    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return {
        "base_url": os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1"),
        "api_key": os.getenv("OPENAI_API_KEY", "not-needed"),
        "model": os.getenv("JARVIS_MODEL", "qwen/qwen3.6-27b"),
    }


class AgentBase(abc.ABC):
    """
    Abstract base class every JARVIS agent inherits from.

    Provides:
    - Identity properties (name, role, colour, description)
    - OpenAI LLM integration via ``process_task()``
    - Async ``execute()`` and ``status()`` hooks
    - Internal status tracking
    """

    # ------------------------------------------------------------------ #
    #  Identity (override in subclasses)                                  #
    # ------------------------------------------------------------------ #
    name: str = "Unknown"
    role: str = "Generic"
    color_hex: str = "#888888"
    description: str = ""
    system_prompt: str = ""

    def __init__(self) -> None:
        self._status: AgentStatus = AgentStatus.idle
        self._current_task: Optional[str] = None
        self._last_activity: Optional[datetime] = None
        self._client: Optional[AsyncOpenAI] = None
        # Load LLM config from environment
        llm_config = _load_llm_config()
        self._base_url = llm_config["base_url"]
        self._api_key = llm_config["api_key"]
        self._model = llm_config["model"]
        logger.info("[%s] Configured LLM: model=%s, base_url=%s", self.name, self._model, self._base_url)

    # ------------------------------------------------------------------ #
    #  Public interface                                                   #
    # ------------------------------------------------------------------ #

    async def execute(self, task: dict) -> dict:
        """
        Execute a single task.

        Parameters
        ----------
        task : dict
            At minimum must contain ``"description"``.  May also carry
            ``"type"`` which the agent can dispatch to a specialised
            handler method.

        Returns
        -------
        dict
            ``{"status": "completed"|"failed", "result": ..., "error": ...}``
        """
        self._status = AgentStatus.working
        self._current_task = task.get("description", "unknown")
        self._last_activity = datetime.now(timezone.utc)
        logger.info("[%s] Starting task: %s", self.name, self._current_task)

        try:
            task_type = task.get("type", "general")
            handler = getattr(self, f"_handle_{task_type}", None)
            if handler is not None and callable(handler):
                result = await handler(task)
            else:
                result = await self.process_task(task.get("description", ""))

            self._status = AgentStatus.idle
            self._last_activity = datetime.now(timezone.utc)
            logger.info("[%s] Task completed.", self.name)
            return {"status": "completed", "result": result}

        except (APIConnectionError, RateLimitError) as exc:
            self._status = AgentStatus.error
            logger.error("[%s] API error: %s", self.name, exc)
            return {"status": "failed", "error": str(exc)}
        except APIStatusError as exc:
            self._status = AgentStatus.error
            logger.error("[%s] API status error (%s): %s", self.name, exc.status_code, exc.message)
            return {"status": "failed", "error": f"API {exc.status_code}: {exc.message}"}
        except Exception as exc:
            self._status = AgentStatus.error
            logger.exception("[%s] Unexpected error: %s", self.name, exc)
            return {"status": "failed", "error": str(exc)}
        finally:
            self._current_task = None

    async def status(self) -> dict:
        """Return a serialisable snapshot of the agent's current state."""
        return {
            "name": self.name,
            "role": self.role,
            "color_hex": self.color_hex,
            "status": self._status.value,
            "current_task": self._current_task,
            "last_activity": self._last_activity.isoformat() if self._last_activity else None,
            "description": self.description,
        }

    # ------------------------------------------------------------------ #
    #  LLM integration                                                    #
    # ------------------------------------------------------------------ #

    def _get_client(self) -> AsyncOpenAI:
        """Lazy-initialise the OpenAI async client pointing to configured endpoint."""
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
            )
        return self._client

    async def process_task(self, task_description: str) -> str:
        """
        Call the OpenAI API with the agent-specific system prompt.

        Parameters
        ----------
        task_description : str
            The user/incoming task to process.

        Returns
        -------
        str
            The assistant's response text.
        """
        client = self._get_client()
        response = await client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": task_description},
            ],
            max_tokens=2048,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        logger.info("[%s] LLM response (%d tokens used approx)", self.name, len(content))
        return content or ""

    # ------------------------------------------------------------------ #
    #  Simulated (offline) fallback                                       #
    # ------------------------------------------------------------------ #

    async def process_task_simulated(self, task_description: str) -> str:
        """
        Simulated LLM response for environments without an API key.
        Adds a small delay to mimic network latency.
        """
        await asyncio.sleep(0.5)
        return (
            f"[{self.name} SIMULATED] Processed: {task_description}\n"
            f"Agent {self.name} ({self.role}) completed the task successfully."
        )
