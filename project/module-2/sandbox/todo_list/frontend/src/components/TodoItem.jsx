import React, { useState } from 'react';
import { Edit3, Trash2, Calendar, Clock } from 'lucide-react';

export default function TodoItem({ todo, onToggle, onEdit, onDelete }) {
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggle(todo.id);
    } finally {
      setIsToggling(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    try {
      // Append 'Z' if timestamp lacks timezone designator to ensure UTC parsing
      const formattedStr = dateStr.endsWith('Z') ? dateStr : `${dateStr}Z`;
      const date = new Date(formattedStr);
      if (isNaN(date.getTime())) {
        return dateStr;
      }
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      }).format(date);
    } catch {
      return dateStr;
    }
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-checkbox-container">
        {isToggling ? (
          <div className="spinner dark" style={{ margin: '2px 4px' }}></div>
        ) : (
          <input
            type="checkbox"
            className="todo-checkbox"
            checked={Boolean(todo.completed)}
            onChange={handleToggle}
            title={todo.completed ? 'Mark as incomplete' : 'Mark as complete'}
          />
        )}
      </div>

      <div className="todo-content">
        <div className="todo-title">{todo.title}</div>
        
        {todo.description && (
          <div className="todo-description">{todo.description}</div>
        )}

        <div className="todo-meta">
          <span className={`status-badge ${todo.completed ? 'completed' : 'pending'}`}>
            {todo.completed ? 'Completed' : 'Pending'}
          </span>

          <span title="Created timestamp" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
            <Calendar size={13} /> {formatDate(todo.created_at)}
          </span>

          {todo.updated_at && todo.updated_at !== todo.created_at && (
            <span title="Updated timestamp" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
              <Clock size={13} /> Updated {formatDate(todo.updated_at)}
            </span>
          )}
        </div>
      </div>

      <div className="todo-actions">
        <button
          className="btn-icon"
          onClick={() => onEdit(todo)}
          title="Edit task"
        >
          <Edit3 size={17} />
        </button>
        <button
          className="btn-icon danger"
          onClick={() => onDelete(todo)}
          title="Delete task"
        >
          <Trash2 size={17} />
        </button>
      </div>
    </div>
  );
}
