"""
SARAH — Customer Support Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from core.agent_base import AgentBase

logger = logging.getLogger("jarvis.agents.sarah")


class Sarah(AgentBase):
    """
    Handles customer inquiries, troubleshoots issues, and escalates complex
    problems to Slack.  Empathetic, efficient, and thorough.
    """

    name: str = "Sarah"
    role: str = "Customer Support"
    color_hex: str = "#00ff88"
    description: str = (
        "Handles customer inquiries, troubleshoots issues, and escalates "
        "complex problems to Slack."
    )
    system_prompt: str = (
        "You are SARAH, a customer support agent. You handle customer "
        "inquiries, troubleshoot issues, and escalate complex problems to "
        "Slack. You are empathetic, efficient, and thorough."
    )

    # ------------------------------------------------------------------ #
    #  Task-type handlers (called by AgentBase.execute via _handle_<type>) #
    # ------------------------------------------------------------------ #

    async def handle_support_ticket(self, task: dict) -> str:
        """Respond to a support ticket."""
        logger.info("Sarah handling support ticket: %s", task.get("description"))
        return await self.process_task(task.get("description", ""))

    async def auto_reply(self, task: dict) -> str:
        """Generate an automated reply for a customer message."""
        logger.info("Sarah generating auto-reply")
        prompt = (
            "Generate a professional, empathetic customer support reply for: "
            f"{task.get('description', 'No details provided.')}"
        )
        return await self.process_task(prompt)

    async def escalate_to_slack(self, task: dict) -> str:
        """Escalate an issue to the Slack channel."""
        logger.info("Sarah escalating to Slack: %s", task.get("description"))
        # In production this would call the Slack API.
        result = await self.process_task(
            f"Draft a Slack escalation message for the following issue: "
            f"{task.get('description', 'No details.')}"
        )
        return f"[SLACK ESCALATION DRAFT]\n{result}"

    # Delegate generic handlers to the appropriate method
    _handle_support = handle_support_ticket
    _handle_auto_reply = auto_reply
    _handle_escalate = escalate_to_slack
    _handle_inquiry = handle_support_ticket
    _handle_ticket = handle_support_ticket
