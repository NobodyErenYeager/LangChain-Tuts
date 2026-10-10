import React from 'react';
import { X, CheckCircle, AlertCircle, Info } from 'lucide-react';

export default function Notification({ notifications, onDismiss }) {
  if (!notifications || notifications.length === 0) return null;

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle size={18} />;
      case 'error':
        return <AlertCircle size={18} />;
      case 'info':
      default:
        return <Info size={18} />;
    }
  };

  return (
    <div className="toast-container">
      {notifications.map((n) => (
        <div key={n.id} className={`toast ${n.type || 'info'}`}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {getIcon(n.type)}
            <span>{n.message}</span>
          </div>
          <button
            className="toast-close"
            onClick={() => onDismiss(n.id)}
            aria-label="Close notification"
          >
            <X size={16} />
          </button>
        </div>
      ))}
    </div>
  );
}
