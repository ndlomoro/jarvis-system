"""
J.A.R.V.I.S. Backend — Pydantic data models.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
#  Enums                                                                      #
# --------------------------------------------------------------------------- #

class AgentStatus(str, Enum):
    """Runtime status of an agent."""

    idle = "idle"
    working = "working"
    error = "error"
    offline = "offline"

    # JSON serialisation helpers
    @classmethod
    def _missing_(cls, value: object) -> AgentStatus:
        return cls.idle


class TaskStatus(str, Enum):
    """Lifecycle status of a task."""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class TelemetryLevel(str, Enum):
    """Log severity for telemetry entries."""

    info = "info"
    warn = "warn"
    error = "error"
    debug = "debug"
    system = "system"


# --------------------------------------------------------------------------- #
#  Agent                                                                      #
# --------------------------------------------------------------------------- #

class Agent(BaseModel):
    """Represents a single agent in the JARVIS system."""

    name: str
    role: str
    color_hex: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    status: AgentStatus = AgentStatus.idle
    current_task: Optional[str] = None
    last_activity: Optional[datetime] = None
    description: str = ""

    model_config = {"json_schema_extra": {
        "examples": [
            {
                "name": "Sarah",
                "role": "Customer Support",
                "color_hex": "#00ff88",
                "status": "idle",
                "current_task": None,
                "last_activity": None,
                "description": "Handles customer inquiries and escalations.",
            }
        ]
    }}


# --------------------------------------------------------------------------- #
#  Task                                                                       #
# --------------------------------------------------------------------------- #

class Task(BaseModel):
    """A unit of work dispatched by the orchestrator."""

    id: str
    type: str
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None

    model_config = {"json_schema_extra": {
        "examples": [
            {
                "id": "task_001",
                "type": "support",
                "assigned_agent": "Sarah",
                "status": "pending",
                "description": "Customer reports login failure on mobile app.",
            }
        ]
    }}


# --------------------------------------------------------------------------- #
#  Telemetry                                                                  #
# --------------------------------------------------------------------------- #

class TelemetryEntry(BaseModel):
    """Single telemetry / log entry."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: str
    level: TelemetryLevel = TelemetryLevel.info


# --------------------------------------------------------------------------- #
#  System Vitals                                                              #
# --------------------------------------------------------------------------- #

class SystemVitals(BaseModel):
    """Real-time system health metrics."""

    memory_pct: float = Field(ge=0, le=100)
    latency_ms: float = Field(ge=0)
    signal_strength: float = Field(ge=0, le=100)
    thermal_c: float = Field(ge=0)
    throughput_mbps: float = Field(ge=0)


# --------------------------------------------------------------------------- #
#  Dashboard State                                                            #
# --------------------------------------------------------------------------- #

class DashboardState(BaseModel):
    """Complete snapshot returned by the /api/status endpoint."""

    vitals: SystemVitals
    agents: list[Agent]
    tasks: list[Task]
    telemetry: list[TelemetryEntry]
    transcript: list[str] = Field(default_factory=list)
