import { useState, useEffect } from 'react';

export default function CoreVisualizer({ state }) {
  const [hue, setHue] = useState(190);

  useEffect(() => {
    if (state === 'active') {
      setHue(120);
    } else {
      setHue(190);
    }
  }, [state]);

  const coreColor = state === 'active' ? 'var(--core-green)' : 'var(--core-blue)';

  // Generate orbiting data points
  const dataPoints = Array.from({ length: 12 }, (_, i) => ({
    id: i,
    delay: `${(i * 0.3).toFixed(1)}s`,
    duration: `${(2 + Math.random() * 3).toFixed(1)}s`,
    size: 2 + Math.random() * 3,
  }));

  return (
    <div
      style={{
        position: 'relative',
        width: '320px',
        height: '320px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {/* Grid floor effect */}
      <div
        style={{
          position: 'absolute',
          bottom: '-40px',
          width: '400px',
          height: '200px',
          background:
            'linear-gradient(180deg, rgba(0,212,255,0.08) 0%, transparent 100%)',
          borderBottom: '1px solid rgba(0,212,255,0.1)',
          borderLeft: '1px solid rgba(0,212,255,0.05)',
          borderRight: '1px solid rgba(0,212,255,0.05)',
          transform: 'perspective(400px) rotateX(60deg)',
          transformOrigin: 'top center',
          backgroundImage:
            'linear-gradient(rgba(0,212,255,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,255,0.06) 1px, transparent 1px)',
          backgroundSize: '30px 30px',
        }}
      />

      {/* Outer ring */}
      <div
        style={{
          position: 'absolute',
          width: '300px',
          height: '300px',
          borderRadius: '50%',
          border: '1px solid rgba(0,212,255,0.15)',
          animation: 'rotate 20s linear infinite',
          boxSizing: 'border-box',
        }}
      >
        {dataPoints.map((dp) => (
          <div
            key={dp.id}
            style={{
              position: 'absolute',
              width: `${dp.size}px`,
              height: `${dp.size}px`,
              borderRadius: '50%',
              background: coreColor,
              boxShadow: `0 0 6px ${coreColor}`,
              top: '50%',
              left: '50%',
              marginTop: '-1px',
              marginLeft: '-1px',
              animation: `orbit ${dp.duration} linear infinite`,
              animationDelay: dp.delay,
              ['--orbit-radius']: '145px',
            }}
          />
        ))}
      </div>

      {/* Middle ring */}
      <div
        style={{
          position: 'absolute',
          width: '220px',
          height: '220px',
          borderRadius: '50%',
          border: '1px dashed rgba(0,212,255,0.25)',
          animation: 'rotate-reverse 14s linear infinite',
        }}
      />

      {/* Inner ring */}
      <div
        style={{
          position: 'absolute',
          width: '150px',
          height: '150px',
          borderRadius: '50%',
          border: '2px solid rgba(0,212,255,0.3)',
          animation: 'rotate 8s linear infinite',
        }}
      />

      {/* Core orb */}
      <div
        style={{
          width: '100px',
          height: '100px',
          borderRadius: '50%',
          background: `radial-gradient(circle at 35% 35%,
            ${coreColor}dd 0%,
            ${coreColor}88 30%,
            ${coreColor}33 60%,
            transparent 100%)`,
          animation: 'coreGlow 3s ease-in-out infinite',
          position: 'relative',
          zIndex: 2,
        }}
      >
        {/* Inner bright spot */}
        <div
          style={{
            position: 'absolute',
            width: '30px',
            height: '30px',
            borderRadius: '50%',
            background: `radial-gradient(circle, #ffffff 0%, ${coreColor} 60%, transparent 100%)`,
            top: '20%',
            left: '25%',
            animation: 'pulse 2s ease-in-out infinite',
          }}
        />

        {/* Cross-hair lines */}
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '10%',
            right: '10%',
            height: '1px',
            background: `linear-gradient(90deg, transparent, ${coreColor}66, transparent)`,
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: '50%',
            top: '10%',
            bottom: '10%',
            width: '1px',
            background: `linear-gradient(180deg, transparent, ${coreColor}66, transparent)`,
          }}
        />
      </div>

      {/* State label */}
      <div
        style={{
          position: 'absolute',
          bottom: '10px',
          fontSize: '10px',
          letterSpacing: '3px',
          color: coreColor,
          textShadow: `0 0 8px ${coreColor}`,
          animation: 'flicker 3s infinite',
        }}
      >
        {state === 'active' ? '● PROCESSING' : '● STANDBY'}
      </div>
    </div>
  );
}
