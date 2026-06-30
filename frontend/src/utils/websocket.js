import { useState, useEffect, useRef, useCallback } from 'react';

let instance = null;

export function useWebSocket(url, options = {}) {
  const { onMessage, onConnect, onDisconnect } = options;
  const wsRef = useRef(null);
  const retryRef = useRef(0);
  const [sendMessage, setSendMessage] = useState(null);

  const connect = useCallback(() => {
    if (wsRef.current && (wsRef.current.readyState === 0 || wsRef.current.readyState === 1)) {
      return;
    }

    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        retryRef.current = 0;
        onConnect?.();
      };

      ws.onmessage = (event) => {
        onMessage?.(event.data);
      };

      ws.onclose = () => {
        onDisconnect?.();
        const backoff = Math.min(2 ** retryRef.current * 1000, 30000);
        retryRef.current += 1;
        setTimeout(connect, backoff);
      };

      ws.onerror = () => {
        ws.close();
      };
    } catch {
      const backoff = Math.min(2 ** retryRef.current * 1000, 30000);
      retryRef.current += 1;
      setTimeout(connect, backoff);
    }
  }, [url, onMessage, onConnect, onDisconnect]);

  useEffect(() => {
    if (instance) {
      setSendMessage(instance);
      return;
    }

    connect();

    setSendMessage((msg) => {
      if (wsRef.current && wsRef.current.readyState === 1) {
        wsRef.current.send(msg);
      }
    });

    return () => {
      if (wsRef.current) {
        wsRef.current.onclose = null;
        wsRef.current.close();
      }
    };
  }, [connect]);

  return { sendMessage };
}
