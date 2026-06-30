import { useState, useRef, useEffect } from 'react';

export default function CommandInput({ value, onChange, onSubmit }) {
  const [focused, setFocused] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (value.trim()) {
      onSubmit(value.trim());
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        padding: '8px 16px',
        borderTop: '1px solid rgba(0,212,255,0.15)',
        background: 'linear-gradient(0deg, rgba(0,212,255,0.04) 0%, transparent 100%)',
        display: 'flex',
        gap: '10px',
        alignItems: 'center',
      }}
    >
      {/* Prompt indicator */}
      <span
        style={{
          color: 'var(--core-green)',
          fontSize: '14px',
          textShadow: '0 0 8px rgba(0,255,136,0.5)',
          animation: 'pulse 2s infinite',
          minWidth: '20px',
        }}
      >
        {'>'}
      </span>

      {/* Input */}
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        placeholder="Enter command..."
        style={{
          flex: 1,
          background: 'rgba(0,0,0,0.4)',
          border: `1px solid ${focused ? 'var(--core-blue)' : 'rgba(0,212,255,0.2)'}`,
          borderRadius: '4px',
          padding: '10px 14px',
          color: '#c8d6e5',
          fontFamily: 'var(--font-mono)',
          fontSize: '13px',
          letterSpacing: '1px',
          outline: 'none',
          transition: 'all 0.3s ease',
          boxShadow: focused
            ? '0 0 12px rgba(0,212,255,0.2), inset 0 0 8px rgba(0,212,255,0.05)'
            : 'none',
        }}
      />

      {/* Send button */}
      <button
        type="submit"
        className="jarvis-btn"
        style={{
          minWidth: '80px',
          padding: '10px 20px',
        }}
      >
        EXECUTE
      </button>
    </form>
  );
}
