# J.A.R.V.I.S. - Multi-Agent Orchestration System

> **J**ust **A** **R**ather **V**ery **I**ntelligent **S**ystem

A multi-agent AI orchestration platform inspired by Iron Man's JARVIS. Coordinates specialized AI agents to handle customer support, development, research, content operations, and ad management.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  JARVIS DASHBOARD                    │
│              (React + Futuristic UI)                 │
├─────────────────────────────────────────────────────┤
│                  FASTAPI BACKEND                     │
│  ┌──────────┐  WebSocket  ┌──────────────────────┐  │
│  │  JARVIS  │◄────────────┤   Orchestrator       │  │
│  │ Core     │             │   - Task Routing      │  │
│  │ API      │             │   - Status Tracking   │  │
│  │ Server   │             │   - Agent Coordination│  │
│  └──────────┘             └──────────┬───────────┘  │
│                                      │              │
│  ┌─────────┐ ┌────────┐ ┌────────┐  │  ┌────────┐ │
│  │ SARAH   │ │  TOM   │ │ SCOUT  │  │  │ BOBBY  │ │
│  │ Support │ │ Dev    │ │Research│  │  │  Ads   │ │
│  └─────────┘ └────────┘ └────────┘  │  └────────┘ │
│                                      │              │
│                           ┌──────────────────────┐  │
│                           │       EVA            │  │
│                           │   Content Ops        │  │
│                           └──────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Agents (Team ROKU)

| Agent | Role | Color |
|-------|------|-------|
| **SARAH** | Customer Support Agent | 🟢 Green |
| **TOM** | Developer Agent | 🔵 Blue |
| **SCOUT** | Research Agent | 🟠 Orange |
| **EVA** | Content Operations Agent | 🟣 Purple |
| **BOBBY** | Ads Manager Agent | 🟡 Yellow |

## Quick Start

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload --port 3000
```

## Features

- **Real-time dashboard** with holographic UI
- **Multi-agent orchestration** with task routing
- **WebSocket** live telemetry & diagnostics
- **Agent specialization** for different domains
- **Auto-escalation** to human when needed
