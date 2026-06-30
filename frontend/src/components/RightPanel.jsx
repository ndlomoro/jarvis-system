import { useState, useEffect, useRef } from 'react';

export default function RightPanel({ transcript, tasks }) {
  const [gaugeValue, setGaugeValue] = useState(72);
  const [gpsLat, setGpsLat] = useState(40.7128);
  const [gpsLon, setGpsLon] = useState(-74.006);
  const waveformBars = useRef(Array.from({ length: 20 }, () => Math.random()));

  useEffect(() => {
    const interval = setInterval(() => {
      setGaugeValue(Math.min(100, Math.max(10, gaugeValue + (Math.random() - 0.5) * 10)));
      setGpsLat((prev) => prev + (Math.random() - 0.5) * 0.001);
      setGpsLon((prev) => prev + (Math.random() - 0.5) * 0.001);
      waveformBars.current = waveformBars.current.map(() => Math.random());
    }, 800);
    return () => clearInterval(interval);
  }, [gaugeValue]);

  // SVG circular gauge
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (gaugeValue / 100) * circumference;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', gap: '12px', minHeight: 0 }}>
      {/* Gauge */}
      <div>
        <div className="panel-header">SYSTEM LOAD</div>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <svg width="110" height="110" viewBox="0 0 100 100">
            {/* Background circle */}
            <circle
              cx="50" cy="50" r={radius}
              fill="none"
              stroke="rgba(255,255,255,0.05)"
              strokeWidth="6"
            />
            {/* Progress arc */}
            <circle
              cx="50" cy="50" r={radius}
              fill="none"
              stroke="var(--core-blue)"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              transform="rotate(-90 50 50)"
              style={{
                transition: 'stroke-dashoffset 1s ease',
                filter: 'drop-shadow(0 0 4px rgba(0,212,255,0.5))',
              }}
            />
            {/* Center text */}
            <text
              x="50" y="46"
              textAnchor="middle"
              fill="var(--core-blue)"
              fontSize="16"
              fontFamily="var(--font-mono)"
              style={{ textShadow: '0 0 8px rgba(0,212,255,0.5)' }}
            >
              {gaugeValue.toFixed(0)}%
            </text>
            <text
              x="50" y="60"
              textAnchor="middle"
              fill="rgba(200,214,229,0.4)"
              fontSize="7"
              fontFamily="var(--font-mono)"
              letterSpacing="1"
            >
              CAPACITY
            </text>
          </svg>
        </div>
      </div>

      {/* Waveform */}
      <div>
        <div className="panel-header">AUDIO SIGNAL</div>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '2px',
            height: '50px',
          }}
        >
          {waveformBars.current.map((h, i) => (
            <div
              key={i}
              style={{
                width: '3px',
                height: `${(h * 40 + 5)}px`,
                background: `linear-gradient(180deg, var(--core-blue), var(--core-purple))`,
                borderRadius: '1px',
                animation: `waveform ${0.5 + h * 0.5}s ease-in-out infinite alternate`,
                animationDelay: `${i * 0.05}s`,
                boxShadow: '0 0 4px rgba(0,212,255,0.3)',
              }}
            />
          ))}
        </div>
      </div>

      {/* GPS */}
      <div>
        <div className="panel-header">LOCATION</div>
        <div style={{ fontSize: '10px', letterSpacing: '1px' }}>
          <div style={{ color: 'rgba(200,214,229,0.5)', marginBottom: '4px' }}>GPS COORDINATES</div>
          <div className="neon-text" style={{ fontSize: '11px' }}>
            {gpsLat.toFixed(4)}° N
          </div>
          <div className="neon-text" style={{ fontSize: '11px' }}>
            {Math.abs(gpsLon).toFixed(4)}° W
          </div>
          <div style={{ color: 'var(--core-green)', fontSize: '9px', marginTop: '4px', animation: 'pulse 2s infinite' }}>
            ● SIGNAL LOCKED
          </div>
        </div>
      </div>

      {/* Transcript / Diagnostics */}
      <div style={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column' }}>
        <div className="panel-header">DIAGNOSTICS</div>
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            fontSize: '9px',
            fontFamily: 'var(--font-mono)',
            lineHeight: '1.5',
            color: 'rgba(200,214,229,0.5)',
            minHeight: 0,
          }}
        >
          {transcript.map((t, i) => (
            <div key={i} style={{ marginBottom: '3px', animation: 'fadeIn 0.3s ease' }}>
              <span style={{ color: 'var(--core-blue)' }}>{t.speaker || 'SYS'}:</span>{' '}
              {t.text || t.message || JSON.stringify(t).slice(0, 80)}
            </div>
          ))}
          {transcript.length === 0 && (
            <div style={{ color: 'rgba(200,214,229,0.2)', textAlign: 'center', padding: '10px' }}>
              NO ACTIVE TRANSMISSION
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
