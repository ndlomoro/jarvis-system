import { useEffect, useRef } from 'react';

export default function TelemetryLog({ entries }) {
  const logRef = useRef(null);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [entries]);

  const levelColor = (level) => {
    switch (level?.toUpperCase()) {
      case 'WARN': return 'var(--core-yellow)';
      case 'ERROR': return 'var(--core-red)';
      default: return 'var(--core-blue)';
    }
  };

  const formatTime = (iso) => {
    try {
      const d = new Date(iso);
      return d.toLocaleTimeString('en-US', { hour12: false });
    } catch {
      return '--:--:--';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', minHeight: 0 }}>
      <div className="panel-header">TELEMETRY</div>
      <div
        ref={logRef}
        style={{
          flex: 1,
          overflowY: 'auto',
          fontSize: '10px',
          fontFamily: 'var(--font-mono)',
          lineHeight: '1.6',
          minHeight: 0,
        }}
      >
        {entries.map((entry, i) => (
          <div
            key={i}
            style={{
              animation: 'fadeIn 0.3s ease',
              borderBottom: '1px solid rgba(255,255,255,0.02)',
              padding: '2px 0',
            }}
          >
            <span style={{ color: 'rgba(200,214,229,0.3)', marginRight: '6px' }}>
              {formatTime(entry.timestamp)}
            </span>
            <span
              style={{
                color: levelColor(entry.level),
                marginRight: '6px',
                fontWeight: 'bold',
                minWidth: '32px',
                display: 'inline-block',
              }}
            >
              [{entry.level || 'INFO'}]
            </span>
            <span style={{ color: 'rgba(200,214,229,0.7)' }}>
              {entry.message}
            </span>
          </div>
        ))}
        {entries.length === 0 && (
          <div style={{ color: 'rgba(200,214,229,0.2)', textAlign: 'center', padding: '20px' }}>
            AWAITING DATA STREAM...
          </div>
        )}
      </div>
    </div>
  );
}
