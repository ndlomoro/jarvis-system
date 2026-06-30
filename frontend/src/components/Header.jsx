import { useState, useEffect } from 'react';

export default function Header({ connected }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (d) =>
    d.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const formatDate = (d) =>
    d.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: '2-digit' }).toUpperCase();

  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 16px',
        borderBottom: '1px solid rgba(0,212,255,0.2)',
        background: 'linear-gradient(180deg, rgba(0,212,255,0.06) 0%, transparent 100%)',
        position: 'relative',
      }}
    >
      {/* LEFT: Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            className="status-dot"
            style={{ background: connected ? 'var(--core-green)' : 'var(--core-red)', boxShadow: connected ? '0 0 6px var(--core-green)' : '0 0 6px var(--core-red)' }}
          />
          <h1
            className="neon-text"
            style={{
              fontSize: '22px',
              letterSpacing: '6px',
              fontWeight: 'bold',
              textShadow: '0 0 10px rgba(0,212,255,0.6), 0 0 30px rgba(0,212,255,0.3)',
            }}
          >
            J.A.R.V.I.S.
          </h1>
        </div>
        <div style={{ width: 1, height: 30, background: 'rgba(0,212,255,0.2)' }} />
        <span style={{ fontSize: '9px', letterSpacing: '2px', color: 'rgba(0,212,255,0.5)' }}>
          JUST A RATHER VERY INTELLIGENT SYSTEM
        </span>
        <div style={{ width: 1, height: 30, background: 'rgba(0,212,255,0.2)' }} />
        <span style={{ fontSize: '10px', color: 'var(--core-green)', letterSpacing: '1px' }}>
          OBJECTIVE: BUILD YOUR VISION
        </span>
      </div>

      {/* CENTER: Status badges */}
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        {[
          { label: 'ONLINE', color: 'var(--core-green)' },
          { label: 'SECURE', color: 'var(--core-blue)' },
          { label: 'ENCRYPTED', color: 'var(--core-purple)' },
          { label: 'AUTO-LVL-9', color: 'var(--core-orange)' },
        ].map((badge) => (
          <span
            key={badge.label}
            style={{
              fontSize: '9px',
              letterSpacing: '1.5px',
              color: badge.color,
              padding: '3px 8px',
              border: `1px solid ${badge.color}`,
              borderRadius: '3px',
              background: `${badge.color}11`,
              boxShadow: `0 0 6px ${badge.color}33`,
              textShadow: `0 0 4px ${badge.color}66`,
              animation: 'flicker 4s infinite',
            }}
          >
            {badge.label}
          </span>
        ))}
      </div>

      {/* RIGHT: Clock */}
      <div style={{ textAlign: 'right', fontSize: '11px', letterSpacing: '1px' }}>
        <div className="neon-text" style={{ fontSize: '14px' }}>
          {formatTime(time)}
        </div>
        <div style={{ color: 'rgba(200,214,229,0.5)', fontSize: '9px', letterSpacing: '2px' }}>
          {formatDate(time)}
        </div>
      </div>
    </header>
  );
}
