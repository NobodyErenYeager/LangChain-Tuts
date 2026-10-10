import React from 'react';
import TodoItem from './TodoItem';
import { CheckCircle2, ListTodo, Loader2 } from 'lucide-react';

export default function TodoList({
  todos,
  isLoading,
  activeFilter,
  onFilterChange,
  onToggleTodo,
  onEditTodo,
  onDeleteTodo,
  onRefresh,
}) {
  const completedCount = todos.filter((t) => t.completed).length;
  const pendingCount = todos.length - completedCount;

  return (
    <div className="card">
      <div className="filter-bar">
        <div className="filter-tabs">
          <button
            className={`filter-tab ${activeFilter === 'all' ? 'active' : ''}`}
            onClick={() => onFilterChange('all')}
          >
            All ({todos.length})
          </button>
          <button
            className={`filter-tab ${activeFilter === 'active' ? 'active' : ''}`}
            onClick={() => onFilterChange('active')}
          >
            Active ({pendingCount})
          </button>
          <button
            className={`filter-tab ${activeFilter === 'completed' ? 'active' : ''}`}
            onClick={() => onFilterChange('completed')}
          >
            Completed ({completedCount})
          </button>
        </div>

        <div className="stats-badge">
          <span>{completedCount} of {todos.length} completed</span>
        </div>
      </div>

      {isLoading ? (
        <div className="loading-container">
          <div className="spinner dark" style={{ width: 28, height: 28, borderWidth: 3 }}></div>
          <p>Loading tasks from server...</p>
        </div>
      ) : todos.length === 0 ? (
        <div className="empty-state">
          <span className="empty-icon">
            {activeFilter === 'completed' ? '🎉' : '📋'}
          </span>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--color-text-main)', marginBottom: '0.35rem' }}>
            {activeFilter === 'completed'
              ? 'No completed tasks yet'
              : activeFilter === 'active'
              ? 'No active tasks!'
              : 'No tasks found'}
          </h3>
          <p style={{ fontSize: '0.9rem' }}>
            {activeFilter === 'all'
              ? 'Get started by creating your first task above.'
              : activeFilter === 'completed'
              ? 'Complete tasks to see them here.'
              : 'All your tasks are completed! Enjoy your day.'}
          </p>
        </div>
      ) : (
        <div className="todo-list">
          {todos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onToggle={onToggleTodo}
              onEdit={onEditTodo}
              onDelete={onDeleteTodo}
            />
          ))}
        </div>
      )}
    </div>
  );
}
