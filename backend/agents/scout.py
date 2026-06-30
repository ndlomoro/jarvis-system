"""
SCOUT — Research Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from core.agent_base import AgentBase

logger = logging.getLogger("jarvis.agents.scout")


class Scout(AgentBase):
    """
    Monitors competitors, analyses trends, researches ads and ideas, and
    surfaces new opportunities.  Analytical and data-driven.
    """

    name: str = "Scout"
    role: str = "Research"
    color_hex: str = "#ff8800"
    description: str = (
        "Monitors competitors, analyses trends, researches ads and ideas, "
        "and surfaces new opportunities."
    )
    system_prompt: str = (
        "You are SCOUT, a research agent. You monitor competitors, analyse "
        "trends, research ads and ideas, and surface new opportunities. "
        "You are analytical and data-driven."
    )

    # ------------------------------------------------------------------ #
    #  Task-type handlers                                                 #
    # ------------------------------------------------------------------ #

    async def research_competitors(self, task: dict) -> str:
        """Research competitor activity."""
        logger.info("Scout researching competitors: %s", task.get("description"))
        prompt = (
            "Analyse the competitive landscape for the following topic. "
            "Provide strengths, weaknesses, and strategic recommendations:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def analyze_trends(self, task: dict) -> str:
        """Analyse market / industry trends."""
        logger.info("Scout analysing trends: %s", task.get("description"))
        prompt = (
            "Analyse current trends and forecast near-term developments "
            "for:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    async def surface_opportunities(self, task: dict) -> str:
        """Surface new business / creative opportunities."""
        logger.info("Scout surfacing opportunities: %s", task.get("description"))
        prompt = (
            "Identify actionable opportunities based on the following context:\n\n"
            f"{task.get('description', 'No details.')}"
        )
        return await self.process_task(prompt)

    # Delegate generic handlers
    _handle_research = research_competitors
    _handle_trends = analyze_trends
    _handle_opportunities = surface_opportunities
    _handle_analysis = analyze_trends
