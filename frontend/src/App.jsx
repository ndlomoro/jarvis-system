import { useState, useEffect, useCallback, useRef } from 'react';
import Header from './components/Header';
import CoreVisualizer from './components/CoreVisualizer';
import SystemVitals from './components/SystemVitals';
import TelemetryLog from './components/TelemetryLog';
import RightPanel from './components/RightPanel';
import AgentPanel from './components/AgentPanel';
import CommandInput from './components/CommandInput';
import { useWebSocket } from './utils/websocket';

const DEFAULT_AGENTS = [
  { id: 'architect', name: 'ARCHITECT', role: 'System Design & Planning', color: '#00d4ff', status: 'idle' },
  { id: 'researcher', name: 'RESEARCHER', role: 'Information Gathering', color: '#00ff88', status: 'idle' },
  { id: 'coder', name: 'CODER', role: 'Code Generation & Review', color: '#cc44ff', status: 'idle' },
  { id: 'reviewer', name: 'REVIEWER', role: 'Quality Assurance', color: '#ff8800', status: 'idle' },
  { id: 'orchestrator', name: 'ORCHESTRATOR', role: 'Task Coordination', color: '#ffdd00', status: 'idle' },
];

const DEFAULT_VITALS = {
  memory: 42,
  latency: 12,
  signal: 96,
  thermal: 35,
  throughput: 78,
};

export default function App() {
  const [agents, setAgents] = useState(DEFAULT_AGENTS);
  const [systemVitals, setSystemVitals] = useState(DEFAULT_VITALS);
  const [telemetry, setTelemetry] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [transcript, setTranscript] = useState([]);
  const [activeAgent, setActiveAgent] = useState(null);
  const [command, setCommand] = useState('');
  const [wsConnected, setWsConnected] = useState(false);

  // WebSocket connection
  const { sendMessage } = useWebSocket('ws://localhost:3000/ws', {
    onMessage: useCallback((data) => {
      try {
        const msg = typeof data === 'string' ? JSON.parse(data) : data;
        switch (msg.type) {
          case 'agents':
            setAgents(msg.payload);
            break;
          case 'active_agent':
            setActiveAgent(msg.payload);
            break;
          case 'vitals':
            setSystemVitals(msg.payload);
            break;
          case 'telemetry':
            setTelemetry((prev) => [...prev.slice(-49), msg.payload]);
            break;
          case 'task':
            setTasks((prev) => [...prev.slice(-19), msg.payload]);
            break;
          case 'transcript':
            setTranscript((prev) => [...prev.slice(-49), msg.payload]);
            break;
          case 'status':
            setWsConnected(msg.connected ?? true);
            break;
          default:
            setTelemetry((prev) => [
              ...prev.slice(-49),
              { timestamp: new Date().toISOString(), level: 'INFO', message: `[SYS] ${JSON.stringify(msg).slice(0, 120)}` },
            ]);
        }
      } catch {
        setTelemetry((prev) => [
          ...prev.slice(-49),
          { timestamp: new Date().toISOString(), level: 'WARN', message: `Parse error: ${String(data).slice(0, 100)}` },
        ]);
      }
    }, []),
    onConnect: useCallback(() => setWsConnected(true), []),
    onDisconnect: useCallback(() => setWsConnected(false), []),
  });

  // Simulated vitals update when no backend
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemVitals((prev) => ({
        memory: Math.min(100, Math.max(5, prev.memory + (Math.random() - 0.5) * 8)),
        latency: Math.min(200, Math.max(1, prev.latency + (Math.random() - 0.5) * 6)),
        signal: Math.min(100, Math.max(60, prev.signal + (Math.random() - 0.5) * 4)),
        thermal: Math.min(90, Math.max(10, prev.thermal + (Math.random() - 0.5) * 5)),
        throughput: Math.min(100, Math.max(20, prev.throughput + (Math.random() - 0.5) * 10)),
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // Initial telemetry entries
  useEffect(() => {
    const initial = [
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'J.A.R.V.I.S. system initialized' },
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'WebSocket connection established' },
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'All subsystems nominal' },
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'Agent roll call complete — 5 agents registered' },
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'Dashboard ready. Awaiting commands.' },
    ];
    setTelemetry(initial);
  }, []);

  const handleCommand = async (text) => {
    if (!text.trim()) return;

    // Add to telemetry
    setTelemetry((prev) => [
      ...prev.slice(-49),
      { timestamp: new Date().toISOString(), level: 'INFO', message: `> ${text}` },
    ]);

    // Try sending to backend
    try {
      const res = await fetch('/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: text }),
      });
      if (res.ok) {
        const data = await res.json();
        setTelemetry((prev) => [
          ...prev.slice(-49),
          { timestamp: new Date().toISOString(), level: 'INFO', message: `← ${data.response || 'Command accepted'}` },
        ]);
      }
    } catch {
      // Backend not available — fallback
      setTelemetry((prev) => [
        ...prev.slice(-49),
        { timestamp: new Date().toISOString(), level: 'WARN', message: `Command queued (backend unavailable): ${text}` },
      ]);
    }

    setCommand('');
  };

  const handleAgentAction = (agentId, action) => {
    setTelemetry((prev) => [
      ...prev.slice(-49),
      { timestamp: new Date().toISOString(), level: 'INFO', message: `Agent action: ${agentId} → ${action}` },
    ]);
    if (sendMessage) {
      sendMessage(JSON.stringify({ type: 'agent_action', payload: { agent: agentId, action } }));
    }
  };

  return (
    <div className="app-container">
      <Header connected={wsConnected} />
      <div className="main-content">
        {/* LEFT */}
        <div className="left-column" style={{ display: 'flex', flexDirection: 'column', gap: '8px', minHeight: 0 }}>
          <div className="panel" style={{ flex: 1, minHeight: 0 }}>
            <SystemVitals vitals={systemVitals} />
          </div>
          <div className="panel" style={{ flex: 1, minHeight: 0 }}>
            <TelemetryLog entries={telemetry} />
          </div>
        </div>

        {/* CENTER */}
        <div className="center-column" style={{ display: 'flex', flexDirection: 'column', gap: '8px', minHeight: 0 }}>
          <div className="panel" style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 0 }}>
            <CoreVisualizer state={activeAgent ? 'active' : 'idle'} />
          </div>
          <div className="panel" style={{ minHeight: 0 }}>
            <AgentPanel
              agents={agents}
              activeAgent={activeAgent}
              onAction={handleAgentAction}
            />
          </div>
        </div>

        {/* RIGHT */}
        <div className="panel right-column" style={{ minHeight: 0 }}>
          <RightPanel transcript={transcript} tasks={tasks} />
        </div>
      </div>

      {/* BOTTOM COMMAND */}
      <CommandInput value={command} onChange={setCommand} onSubmit={handleCommand} />
    </div>
  );
}
