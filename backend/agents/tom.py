"""
TOM — Developer Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from core.agent_base import AgentBase

logger = logging.getLogger("jarvis.agents.tom")


class Tom(AgentBase):
    """
    Investigates bugs, writes code, makes changes, and opens pull requests.
    Methodical, security-conscious, and writes clean code.
    """

    name: str = "Tom"
    role: str = "Developer"
    color_hex: str = "#00aaff"
    description: str = (
        "Investigates bugs, writes code, makes changes, and opens pull "
        "requests. Methodical and security-conscious."
    )
    system_prompt: str = (
        "You are TOM, a developer agent. You investigate bugs, write code, "
        "make changes, and open pull requests. You are methodical, "
        "security-conscious, and write clean code."
    )

    # ------------------------------------------------------------------ #
    #  Task-type handlers                                                 #
    # ------------------------------------------------------------------ #

    async def investigate_bug(self, task: dict) -> str:
        """Investigate a reported bug."""
        logger.info("Tom investigating bug: %s", task.get("description"))
        prompt = (
            "Investigate the following bug report and provide root cause "
            "analysis, reproduction steps, and a recommended fix:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def make_code_changes(self, task: dict) -> str:
        """Propose code changes."""
        logger.info("Tom making code changes: %s", task.get("description"))
        prompt = (
            "Write the code changes needed for the following requirement. "
            "Include file paths, diffs, and any migration notes:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def open_pr(self, task: dict) -> str:
        """Draft a pull request description."""
        logger.info("Tom drafting PR: %s", task.get("description"))
        prompt = (
            "Draft a clear pull request description including title, "
            "summary, testing notes, and checklist for:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    # Delegate generic handlers
    _handle_bug = investigate_bug
    _handle_code = make_code_changes
    _handle_pr = open_pr
    _handle_development = make_code_changes
    _handle_fix = investigate_bug
