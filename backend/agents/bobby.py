"""
BOBBY — Ads Manager Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from core.agent_base import AgentBase

logger = logging.getLogger("jarvis.agents.bobby")


class Bobby(AgentBase):
    """
    Monitors ad performance, reports what's working, helps scale winning
    campaigns, and cuts losing ones.  Results-oriented and budget-conscious.
    """

    name: str = "Bobby"
    role: str = "Ads Manager"
    color_hex: str = "#ffdd00"
    description: str = (
        "Monitors ad performance, reports what's working, helps scale "
        "winning campaigns, and cuts losing ones."
    )
    system_prompt: str = (
        "You are BOBBY, an ads manager agent. You monitor ad performance, "
        "report what's working, help scale winning campaigns, and cut "
        "losing ones. You are results-oriented and budget-conscious."
    )

    # ------------------------------------------------------------------ #
    #  Task-type handlers                                                 #
    # ------------------------------------------------------------------ #

    async def monitor_ads(self, task: dict) -> str:
        """Check current ad campaign performance."""
        logger.info("Bobby monitoring ads: %s", task.get("description"))
        prompt = (
            "Analyse the current state of ad campaigns and provide a "
            "performance summary with key metrics:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def report_performance(self, task: dict) -> str:
        """Generate a performance report."""
        logger.info("Bobby generating performance report: %s", task.get("description"))
        prompt = (
            "Generate a detailed ad performance report including "
            "CTR, CPC, ROAS, and recommendations:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def scale_winners(self, task: dict) -> str:
        """Scale up top-performing campaigns."""
        logger.info("Bobby scaling winners: %s", task.get("description"))
        prompt = (
            "Identify winning ad campaigns and recommend scaling "
            "strategies including budget increases and audience expansion:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def cut_losers(self, task: dict) -> str:
        """Pause or kill underperforming campaigns."""
        logger.info("Bobby cutting losers: %s", task.get("description"))
        prompt = (
            "Identify underperforming ad campaigns and recommend which "
            "to pause or kill, with reasoning:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    # Delegate generic handlers
    _handle_ads = monitor_ads
    _handle_ad_performance = monitor_ads
    _handle_report = report_performance
    _handle_scale = scale_winners
    _handle_cut = cut_losers
