import React from 'react';
import { CheckSquare, RefreshCw } from 'lucide-react';

export default function Navbar({ apiStatus, isCheckingHealth, onCheckHealth }) {
  return (
    <header className="app-header">
      <div className="app-title">
        <CheckSquare size={30} color="#4f46e5" />
        <h1>Task Manager</h1>
      </div>
      <div className="api-status-container" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <div
          className={`api-status ${apiStatus === 'online' ? 'online' : apiStatus === 'offline' ? 'offline' : ''}`}
          title={apiStatus === 'online' ? 'Backend API connected' : 'Backend API unreachable'}
        >
          <span className="status-dot"></span>
          <span>{apiStatus === 'online' ? 'API Online' : apiStatus === 'offline' ? 'API Offline' : 'Connecting...'}</span>
        </div>
        <button
          className="btn-icon"
          onClick={onCheckHealth}
          disabled={isCheckingHealth}
          title="Refresh connection status"
        >
          <RefreshCw size={16} className={isCheckingHealth ? 'spin' : ''} />
        </button>
      </div>
    </header>
  );
}
