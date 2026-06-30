"""
J.A.R.V.I.S. Backend — Central Orchestrator.

Coordinates all agents, routes tasks, tracks progress, and maintains
the global dashboard state.
"""

from __future__ import annotations

import asyncio
import logging
import random
import uuid
from datetime import datetime, timezone
from typing import Optional

from openai import AsyncOpenAI

from core.agent_base import AgentBase, _load_llm_config
from core.models import (
    Agent,
    AgentStatus,
    DashboardState,
    SystemVitals,
    Task,
    TaskStatus,
    TelemetryEntry,
    TelemetryLevel,
)

logger = logging.getLogger("jarvis.orchestrator")

# --------------------------------------------------------------------------- #
#  Task-type → Agent mapping                                                  #
# --------------------------------------------------------------------------- #

ROUTING_TABLE: dict[str, str] = {
    # Sarah — support
    "support": "Sarah",
    "inquiry": "Sarah",
    "ticket": "Sarah",
    "customer": "Sarah",
    "escalate": "Sarah",
    "auto_reply": "Sarah",
    # Tom — development
    "bug": "Tom",
    "code": "Tom",
    "development": "Tom",
    "fix": "Tom",
    "pr": "Tom",
    "deploy": "Tom",
    # Scout — research
    "research": "Scout",
    "trends": "Scout",
    "analysis": "Scout",
    "opportunities": "Scout",
    "competitor": "Scout",
    # Eva — content
    "content": "Eva",
    "footage": "Eva",
    "edit": "Eva",
    "publish": "Eva",
    "schedule": "Eva",
    # Bobby — ads
    "ads": "Bobby",
    "ad_performance": "Bobby",
    "report": "Bobby",
    "scale": "Bobby",
    "cut": "Bobby",
}


class Orchestrator:
    """
    Central brain of the J.A.R.V.I.S. system.

    Responsibilities
    ----------------
    - Maintain the agent roster
    - Route incoming tasks to the correct agent
    - Track task lifecycle and agent status
    - Generate telemetry entries
    - Simulate system vitals
    - Process natural-language commands via LLM
    """

    system_prompt: str = (
        "You are JARVIS, an AI orchestrator. You coordinate a team of "
        "specialised AI agents, decide who handles each task, track "
        "progress, and ensure nothing falls through the cracks."
    )

    def __init__(self, agents: list[AgentBase]) -> None:
        self._agents: dict[str, AgentBase] = {a.name: a for a in agents}
        self._tasks: list[Task] = []
        self._telemetry: list[TelemetryEntry] = []
        self._transcript: list[str] = []
        self._client: Optional[AsyncOpenAI] = None
        # Load LLM config from environment
        llm_config = _load_llm_config()
        self._base_url = llm_config["base_url"]
        self._api_key = llm_config["api_key"]
        self._model = llm_config["model"]
        logger.info("JARVIS Orchestrator LLM: model=%s, base_url=%s", self._model, self._base_url)
        self._vitals: SystemVitals = self._simulate_vitals()

        self._add_telemetry(
            "JARVIS orchestrator initialised",
            TelemetryLevel.system,
        )
        for agent in agents:
            self._add_telemetry(
                f"Agent {agent.name} ({agent.role}) registered",
                TelemetryLevel.system,
            )

    # ------------------------------------------------------------------ #
    #  Telemetry helpers                                                   #
    # ------------------------------------------------------------------ #

    def _add_telemetry(self, message: str, level: TelemetryLevel = TelemetryLevel.info) -> None:
        entry = TelemetryEntry(message=message, level=level)
        self._telemetry.append(entry)
        # Keep last 200 entries
        if len(self._telemetry) > 200:
            self._telemetry = self._telemetry[-200:]
        logger.info("[TELEMETRY %s] %s", level.value, message)

    # ------------------------------------------------------------------ #
    #  System vitals simulation                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _simulate_vitals() -> SystemVitals:
        """Return plausible randomised system vitals."""
        return SystemVitals(
            memory_pct=round(random.uniform(35, 72), 1),
            latency_ms=round(random.uniform(12, 180), 1),
            signal_strength=round(random.uniform(78, 100), 1),
            thermal_c=round(random.uniform(38, 62), 1),
            throughput_mbps=round(random.uniform(45, 950), 1),
        )

    async def refresh_vitals(self) -> None:
        """Periodically refresh simulated vitals."""
        while True:
            self._vitals = self._simulate_vitals()
            await asyncio.sleep(5)

    # ------------------------------------------------------------------ #
    #  Task routing                                                        #
    # ------------------------------------------------------------------ #

    def _resolve_agent(self, task_type: str) -> Optional[str]:
        """
        Look up the best agent for a given task type.
        Falls back to keyword matching on the type string.
        """
        # Direct lookup
        agent_name = ROUTING_TABLE.get(task_type.lower())
        if agent_name:
            return agent_name

        # Keyword fallback
        type_lower = task_type.lower()
        for key, name in ROUTING_TABLE.items():
            if key in type_lower:
                return name

        # Default: assign to the first available agent
        for name, agent in self._agents.items():
            return name
        return None

    async def route_task(self, task: dict) -> dict:
        """
        Create a Task record, dispatch to the appropriate agent, and wait
        for completion.

        Parameters
        ----------
        task : dict
            Must contain ``"description"``.  Optionally ``"type"``.

        Returns
        -------
        dict
            The completed Task as a serialisable dict.
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task_type = task.get("type", "general")
        description = task.get("description", "No description")

        assigned_agent_name = self._resolve_agent(task_type) or "Sarah"
        assigned_agent = self._agents.get(assigned_agent_name)

        if assigned_agent is None:
            self._add_telemetry(
                f"Agent '{assigned_agent_name}' not found for task {task_id}",
                TelemetryLevel.error,
            )
            return {
                "id": task_id,
                "status": "failed",
                "error": f"No suitable agent found for type '{task_type}'",
            }

        task_record = Task(
            id=task_id,
            type=task_type,
            assigned_agent=assigned_agent_name,
            status=TaskStatus.in_progress,
            description=description,
        )
        self._tasks.append(task_record)

        self._add_telemetry(
            f"Task {task_id} routed to {assigned_agent_name} [{task_type}]",
            TelemetryLevel.info,
        )
        self._transcript.append(
            f"[{assigned_agent_name}] Assigned: {description}"
        )

        # Execute
        result = await assigned_agent.execute(task)

        # Update task record
        task_record.status = (
            TaskStatus.completed if result["status"] == "completed" else TaskStatus.failed
        )
        task_record.completed_at = datetime.now(timezone.utc)
        task_record.result = result.get("result")
        task_record.error = result.get("error")

        self._add_telemetry(
            f"Task {task_id} finished: {result['status']}",
            TelemetryLevel.info if result["status"] == "completed" else TelemetryLevel.error,
        )
        self._transcript.append(
            f"[{assigned_agent_name}] {'✓' if result['status'] == 'completed' else '✗'} {description}"
        )

        # Trim to last 50 tasks / 50 transcript lines
        if len(self._tasks) > 50:
            self._tasks = self._tasks[-50:]
        if len(self._transcript) > 50:
            self._transcript = self._transcript[-50:]

        return task_record.model_dump()

    # ------------------------------------------------------------------ #
    #  Natural-language command processing                                 #
    # ------------------------------------------------------------------ #

    def _get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
            )
        return self._client

    async def process_command(self, command: str) -> str:
        """
        Interpret a natural-language command and either route it as a task
        or return a direct response.

        Parameters
        ----------
        command : str
            E.g. "Initiate Avengers Protocol" or "Check ad performance".

        Returns
        -------
        str
            Human-readable response.
        """
        self._add_telemetry(f"Command received: {command}", TelemetryLevel.info)

        # Quick shortcut: "Initiate Avengers Protocol" → wake all agents
        if "avengers" in command.lower() and ("protocol" in command.lower() or "assemble" in command.lower()):
            return await self._avengers_protocol()

        # Use LLM to decide routing
        try:
            client = self._get_client()
            response = await client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"{self.system_prompt}\n\n"
                            "Available agents and their specialisations:\n"
                            + "\n".join(
                                f"- {a.name} ({a.role}): {a.description}"
                                for a in self._agents.values()
                            )
                            + "\n\n"
                            "Respond with a JSON object containing:\n"
                            '{"action": "route"|"reply", "agent": "<name or null>", '
                            '"task_type": "<type or null>", "response": "<message>"}'
                        ),
                    },
                    {"role": "user", "content": command},
                ],
                max_tokens=1024,
                temperature=0.3,
            )
            decision_text = response.choices[0].message.content or "{}"
            self._transcript.append(f"[JARVIS] {decision_text[:120]}")
            self._add_telemetry("Command processed by JARVIS", TelemetryLevel.info)
            return decision_text

        except Exception as exc:
            logger.exception("Command processing failed")
            return f"JARVIS encountered an error processing your command: {exc}"

    async def _avengers_protocol(self) -> str:
        """Wake all agents — status check across the board."""
        self._add_telemetry("AVENGERS PROTOCOL initiated!", TelemetryLevel.system)
        statuses = []
        for name, agent in self._agents.items():
            st = await agent.status()
            statuses.append(f"  • {st['name']} ({st['role']}): {st['status']}")

        body = "🛡️ AVENGERS PROTOCOL — All Agents Status:\n" + "\n".join(statuses)
        self._transcript.append(body)
        return body

    # ------------------------------------------------------------------ #
    #  Dashboard state                                                     #
    # ------------------------------------------------------------------ #

    async def get_dashboard_state(self) -> DashboardState:
        """Build the full dashboard snapshot."""
        agents_snapshot: list[Agent] = []
        for name, agent in self._agents.items():
            info = await agent.status()
            agents_snapshot.append(Agent(**info))

        return DashboardState(
            vitals=self._vitals,
            agents=agents_snapshot,
            tasks=[t.model_dump() for t in self._tasks],
            telemetry=[t.model_dump() for t in self._telemetry],
            transcript=self._transcript,
        )
