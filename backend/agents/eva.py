"""
EVA — Content Operations Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from core.agent_base import AgentBase

logger = logging.getLogger("jarvis.agents.eva")


class Eva(AgentBase):
    """
    Pulls raw footage from Google Drive, edits content, schedules posts,
    and publishes across platforms.  Creative and organised.
    """

    name: str = "Eva"
    role: str = "Content Operations"
    color_hex: str = "#cc44ff"
    description: str = (
        "Pulls raw footage from Google Drive, edits content, schedules "
        "posts, and publishes across platforms."
    )
    system_prompt: str = (
        "You are EVA, a content operations agent. You pull raw footage "
        "from Google Drive, edit content, schedule posts, and publish "
        "across platforms. You are creative and organized."
    )

    # ------------------------------------------------------------------ #
    #  Task-type handlers                                                 #
    # ------------------------------------------------------------------ #

    async def pull_footage(self, task: dict) -> str:
        """Retrieve raw footage from Google Drive."""
        logger.info("Eva pulling footage: %s", task.get("description"))
        prompt = (
            "Plan the steps to retrieve and organise raw footage for:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def edit_content(self, task: dict) -> str:
        """Edit / produce content."""
        logger.info("Eva editing content: %s", task.get("description"))
        prompt = (
            "Create an editing plan and describe the final output for:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def schedule_publish(self, task: dict) -> str:
        """Schedule and publish content across platforms."""
        logger.info("Eva scheduling publish: %s", task.get("description"))
        prompt = (
            "Create a publishing schedule and platform-specific optimisation "
            "plan for:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    # Delegate generic handlers
    _handle_footage = pull_footage
    _handle_edit = edit_content
    _handle_publish = schedule_publish
    _handle_content = edit_content
    _handle_schedule = schedule_publish
