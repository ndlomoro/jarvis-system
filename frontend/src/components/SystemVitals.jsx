export default function SystemVitals({ vitals }) {
  const metrics = [
    { label: 'MEMORY', value: vitals.memory, unit: '%', max: 100 },
    { label: 'LATENCY', value: vitals.latency, unit: 'ms', max: 200 },
    { label: 'SIGNAL', value: vitals.signal, unit: '%', max: 100 },
    { label: 'THERMAL', value: vitals.thermal, unit: '°C', max: 90 },
    { label: 'THROUGHPUT', value: vitals.throughput, unit: '%', max: 100 },
  ];

  const barColor = (value, max) => {
    const pct = (value / max) * 100;
    if (pct > 80) return 'var(--core-red)';
    if (pct > 60) return 'var(--core-orange)';
    if (pct > 40) return 'var(--core-yellow)';
    return 'var(--core-green)';
  };

  return (
    <div>
      <div className="panel-header">SYSTEM VITALS</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {metrics.map((m) => {
          const pct = Math.min(100, Math.max(0, (m.value / m.max) * 100));
          const color = barColor(m.value, m.max);
          return (
            <div key={m.label}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '10px',
                  letterSpacing: '1.5px',
                  marginBottom: '4px',
                }}
              >
                <span style={{ color: 'rgba(200,214,229,0.7)' }}>{m.label}</span>
                <span style={{ color, textShadow: `0 0 6px ${color}` }}>
                  {typeof m.value === 'number' ? m.value.toFixed(1) : m.value}
                  {m.unit}
                </span>
              </div>
              <div
                style={{
                  height: '4px',
                  background: 'rgba(255,255,255,0.05)',
                  borderRadius: '2px',
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    height: '100%',
                    width: `${pct}%`,
                    background: `linear-gradient(90deg, ${color}88, ${color})`,
                    borderRadius: '2px',
                    transition: 'width 1s ease',
                    boxShadow: `0 0 8px ${color}66`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Decorative divider */}
      <div
        style={{
          marginTop: '14px',
          borderTop: '1px solid rgba(0,212,255,0.1)',
          paddingTop: '10px',
        }}
      >
        <div style={{ fontSize: '9px', letterSpacing: '2px', color: 'rgba(200,214,229,0.3)' }}>
          DIAGNOSTIC MODE
        </div>
        <div
          style={{
            fontSize: '9px',
            color: 'var(--core-green)',
            marginTop: '4px',
            animation: 'pulse 2s infinite',
          }}
        >
          ● ALL SYSTEMS NOMINAL
        </div>
      </div>
    </div>
  );
}
