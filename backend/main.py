"""
J.A.R.V.I.S. Backend — FastAPI application entry point.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

# ----------------------------------------------------------------------- #
#  Logging setup                                                           #
# ----------------------------------------------------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)-5s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("jarvis")

# ----------------------------------------------------------------------- #
#  Agent imports                                                           #
# ----------------------------------------------------------------------- #

from agents.bobby import Bobby
from agents.eva import Eva
from agents.sarah import Sarah
from agents.scout import Scout
from agents.tom import Tom
from core.models import Task, TaskStatus, TelemetryEntry, TelemetryLevel
from core.orchestrator import Orchestrator

# ----------------------------------------------------------------------- #
#  Global state                                                            #
# ----------------------------------------------------------------------- #

orchestrator: Orchestrator | None = None
ws_clients: list[WebSocket] = []

# ----------------------------------------------------------------------- #
#  Lifespan                                                                #
# ----------------------------------------------------------------------- #

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    global orchestrator

    # Instantiate agents
    agents = [Sarah(), Tom(), Scout(), Eva(), Bobby()]
    orchestrator = Orchestrator(agents)
    logger.info("JARVIS system online — %d agents registered", len(agents))

    # Start vitals refresh background task
    vitals_task = asyncio.create_task(orchestrator.refresh_vitals())

    # Start telemetry heartbeat
    heartbeat_task = asyncio.create_task(_telemetry_heartbeat())

    yield

    # Shutdown
    vitals_task.cancel()
    heartbeat_task.cancel()
    logger.info("JARVIS system shutting down")


# ----------------------------------------------------------------------- #
#  Telemetry heartbeat                                                     #
# ----------------------------------------------------------------------- #

async def _telemetry_heartbeat() -> None:
    """Periodically push simulated telemetry to all connected WebSocket clients."""
    messages = [
        "System diagnostics: nominal",
        "Neural link: stable",
        "Quantum core: operating within parameters",
        "Agent mesh: all nodes responsive",
        "Firewall: active, no threats detected",
        "Memory allocation: optimised",
        "Signal integrity: 99.7%",
    ]
    while True:
        await asyncio.sleep(8)
        msg = TelemetryEntry(
            message=random.choice(messages),
            level=TelemetryLevel.system,
        )
        if orchestrator is not None:
            orchestrator._add_telemetry(msg.message, msg.level)
            await _broadcast(json.dumps(msg.model_dump(mode="json")))


# ----------------------------------------------------------------------- #
#  FastAPI app                                                             #
# ----------------------------------------------------------------------- #

app = FastAPI(
    title="J.A.R.V.I.S. Orchestrator",
    description="Multi-agent orchestration backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------- #
#  Request / response models                                               #
# ----------------------------------------------------------------------- #

class CommandRequest(BaseModel):
    command: str

class TaskRequest(BaseModel):
    type: str
    description: str

# ----------------------------------------------------------------------- #
#  Routes                                                                  #
# ----------------------------------------------------------------------- #

@app.get("/api/health")
async def root():
    """Health check endpoint."""
    return {
        "system": "JARVIS",
        "status": "online",
        "time": datetime.now(timezone.utc).isoformat(),
        "agents_online": len(orchestrator._agents) if orchestrator else 0,
        "docs": "/docs",
    }


@app.get("/api/status")
async def api_status():
    """Full dashboard state snapshot."""
    if orchestrator is None:
        return {"error": "System not initialised"}
    state = await orchestrator.get_dashboard_state()
    return state.model_dump()


@app.get("/api/agents")
async def api_agents():
    """List all registered agents."""
    if orchestrator is None:
        return {"error": "System not initialised"}
    agents = []
    for name, agent in orchestrator._agents.items():
        agents.append(await agent.status())
    return {"agents": agents}


@app.post("/api/command")
async def api_command(req: CommandRequest):
    """
    Submit a natural-language command.

    Example: ``{"command": "Initiate Avengers Protocol"}``
    """
    if orchestrator is None:
        return {"error": "System not initialised"}
    result = await orchestrator.process_command(req.command)
    return {"response": result}


@app.post("/api/task")
async def api_task(req: TaskRequest):
    """
    Submit a structured task.

    Example: ``{"type": "support", "description": "Customer can't log in"}``
    """
    if orchestrator is None:
        return {"error": "System not initialised"}
    result = await orchestrator.route_task({
        "type": req.type,
        "description": req.description,
    })
    return result


# ----------------------------------------------------------------------- #
#  WebSocket                                                               #
# ----------------------------------------------------------------------- #

async def _broadcast(data: str) -> None:
    """Push a message to all connected WebSocket clients."""
    disconnected = []
    for ws in ws_clients:
        try:
            await ws.send_text(data)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        ws_clients.remove(ws)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time telemetry and status updates."""
    await websocket.accept()
    ws_clients.append(websocket)
    logger.info("WebSocket client connected (%d total)", len(ws_clients))

    # Send initial state
    if orchestrator is not None:
        state = await orchestrator.get_dashboard_state()
        await websocket.send_text(json.dumps({
            "type": "initial_state",
            "data": state.model_dump(mode="json"),
        }))

    try:
        while True:
            # Keep connection alive — echo back ping
            data = await websocket.receive_text()
            # If client sends a command, process it
            try:
                payload = json.loads(data)
                if payload.get("type") == "command":
                    result = await orchestrator.process_command(payload["command"])
                    await websocket.send_text(json.dumps({
                        "type": "command_response",
                        "data": result,
                    }))
                elif payload.get("type") == "task":
                    result = await orchestrator.route_task({
                        "type": payload.get("type_str", "general"),
                        "description": payload.get("description", ""),
                    })
                    await websocket.send_text(json.dumps({
                        "type": "task_result",
                        "data": result,
                    }))
            except (json.JSONDecodeError, KeyError):
                # Non-JSON message — just acknowledge
                await websocket.send_text(json.dumps({"type": "ack"}))
    except WebSocketDisconnect:
        ws_clients.remove(websocket)
        logger.info("WebSocket client disconnected (%d remaining)", len(ws_clients))
    except Exception as exc:
        logger.exception("WebSocket error: %s", exc)
        if websocket in ws_clients:
            ws_clients.remove(websocket)


# ----------------------------------------------------------------------- #
#  Serve frontend SPA                                                       #
# ----------------------------------------------------------------------- #

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    logger.warning("Frontend dist not found at %s — SPA serving disabled", FRONTEND_DIST)

# ----------------------------------------------------------------------- #
#  Dev server entry point                                                   #
# ----------------------------------------------------------------------- #

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
