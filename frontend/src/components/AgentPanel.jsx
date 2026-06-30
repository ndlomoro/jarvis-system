import { useState } from 'react';

export default function AgentPanel({ agents, activeAgent, onAction }) {
  const [selectedAgent, setSelectedAgent] = useState(null);

  const current = selectedAgent || activeAgent || agents[0];

  const actions = ['INITIATE', 'RESET', 'SYNC', 'CANCEL', 'READY'];

  return (
    <div>
      <div className="panel-header">ROLL CALL — ACTIVE SPEAKER</div>

      {/* Agent selector tabs */}
      <div style={{ display: 'flex', gap: '6px', marginBottom: '12px', flexWrap: 'wrap' }}>
        {agents.map((agent) => {
          const isActive = current?.id === agent.id;
          return (
            <button
              key={agent.id}
              className={`jarvis-btn ${isActive ? 'active' : ''}`}
              onClick={() => setSelectedAgent(agent)}
              style={{
                borderColor: agent.color,
                color: isActive ? agent.color : 'rgba(200,214,229,0.5)',
                background: isActive ? `${agent.color}18` : 'transparent',
                boxShadow: isActive ? `0 0 10px ${agent.color}44` : 'none',
                fontSize: '9px',
                padding: '5px 10px',
              }}
            >
              {agent.name}
            </button>
          );
        })}
      </div>

      {/* Active agent display */}
      {current && (
        <div
          style={{
            padding: '14px',
            borderRadius: '6px',
            border: `1px solid ${current.color}44`,
            background: `linear-gradient(135deg, ${current.color}08, ${current.color}03)`,
            transition: 'all 0.5s ease',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
            <div
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                background: current.color,
                boxShadow: `0 0 10px ${current.color}`,
                animation: 'pulse 2s infinite',
              }}
            />
            <span
              style={{
                fontSize: '18px',
                letterSpacing: '3px',
                color: current.color,
                textShadow: `0 0 10px ${current.color}66`,
              }}
            >
              {current.name}
            </span>
            <span
              style={{
                fontSize: '9px',
                color: 'rgba(200,214,229,0.4)',
                letterSpacing: '1px',
              }}
            >
              [{current.status || 'IDLE'}]
            </span>
          </div>

          <div
            style={{
              fontSize: '10px',
              color: 'rgba(200,214,229,0.5)',
              letterSpacing: '1px',
              marginBottom: '10px',
            }}
          >
            ROLE: {current.role}
          </div>

          {/* Action buttons */}
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            {actions.map((action) => (
              <button
                key={action}
                className="jarvis-btn"
                onClick={() => onAction(current.id, action)}
                style={{
                  borderColor: `${current.color}66`,
                  color: `${current.color}bb`,
                  background: `${current.color}08`,
                  fontSize: '9px',
                  padding: '4px 10px',
                }}
              >
                {action}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Agent status grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: '4px',
          marginTop: '10px',
        }}
      >
        {agents.map((agent) => {
          const isActive = current?.id === agent.id;
          return (
            <div
              key={agent.id}
              style={{
                textAlign: 'center',
                padding: '6px 2px',
                borderRadius: '4px',
                background: isActive ? `${agent.color}15` : 'rgba(255,255,255,0.02)',
                border: `1px solid ${isActive ? `${agent.color}44` : 'rgba(255,255,255,0.04)'}`,
                transition: 'all 0.3s ease',
              }}
            >
              <div
                style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: agent.status === 'active' ? agent.color : 'rgba(200,214,229,0.2)',
                  boxShadow: agent.status === 'active' ? `0 0 6px ${agent.color}` : 'none',
                  margin: '0 auto 4px',
                  animation: agent.status === 'active' ? 'pulse 1.5s infinite' : 'none',
                }}
              />
              <div
                style={{
                  fontSize: '8px',
                  letterSpacing: '1px',
                  color: isActive ? agent.color : 'rgba(200,214,229,0.3)',
                }}
              >
                {agent.name.slice(0, 6)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
