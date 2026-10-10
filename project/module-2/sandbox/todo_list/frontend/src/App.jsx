import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import EditTodoModal from './components/EditTodoModal';
import DeleteConfirmModal from './components/DeleteConfirmModal';
import Notification from './components/Notification';
import { getTodos, createTodo, updateTodo, toggleTodo, deleteTodo, checkHealth } from './services/api';
import { AlertCircle, RefreshCw } from 'lucide-react';

export default function App() {
  const [todos, setTodos] = useState([]);
  const [activeFilter, setActiveFilter] = useState('all'); // 'all', 'active', 'completed'
  const [isLoading, setIsLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState('checking'); // 'online', 'offline', 'checking'
  const [isCheckingHealth, setIsCheckingHealth] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [notifications, setNotifications] = useState([]);

  // Modal states
  const [editingTodo, setEditingTodo] = useState(null);
  const [deletingTodo, setDeletingTodo] = useState(null);

  const addNotification = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random();
    setNotifications((prev) => [...prev, { id, message, type }]);

    // Auto dismiss
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, 4000);
  }, []);

  const dismissNotification = useCallback((id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  // Health check
  const verifyHealth = useCallback(async () => {
    setIsCheckingHealth(true);
    try {
      await checkHealth();
      setApiStatus('online');
    } catch {
      setApiStatus('offline');
    } finally {
      setIsCheckingHealth(false);
    }
  }, []);

  // Fetch todos
  const fetchTodos = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);

    let completedFilter = null;
    if (activeFilter === 'active') completedFilter = false;
    if (activeFilter === 'completed') completedFilter = true;

    try {
      const data = await getTodos(completedFilter);
      setTodos(data);
      setApiStatus('online');
    } catch (err) {
      setErrorMessage(err.message || 'Failed to fetch todos');
      setApiStatus('offline');
    } finally {
      setIsLoading(false);
    }
  }, [activeFilter]);

  // Initial load
  useEffect(() => {
    verifyHealth();
    fetchTodos();
  }, [fetchTodos, verifyHealth]);

  // Handlers
  const handleAddTodo = async (todoData) => {
    try {
      const newTodo = await createTodo(todoData);
      addNotification(`Task "${newTodo.title}" created successfully!`, 'success');
      fetchTodos();
      return newTodo;
    } catch (err) {
      addNotification(err.message || 'Failed to create task', 'error');
      throw err;
    }
  };

  const handleToggleTodo = async (id) => {
    try {
      const updated = await toggleTodo(id);
      setTodos((prev) =>
        prev.map((t) => (t.id === id ? updated : t))
      );
      const statusText = updated.completed ? 'completed' : 'active';
      addNotification(`Marked task as ${statusText}`, 'success');
      
      // If we are currently filtering by active/completed, re-fetch to update view
      if (activeFilter !== 'all') {
        fetchTodos();
      }
    } catch (err) {
      addNotification(err.message || 'Failed to toggle task', 'error');
      fetchTodos(); // Sync state on error
    }
  };

  const handleEditSave = async (id, updatedData) => {
    try {
      const updated = await updateTodo(id, updatedData);
      setTodos((prev) =>
        prev.map((t) => (t.id === id ? updated : t))
      );
      addNotification('Task updated successfully!', 'success');
      if (activeFilter !== 'all') {
        fetchTodos();
      }
      return updated;
    } catch (err) {
      addNotification(err.message || 'Failed to update task', 'error');
      throw err;
    }
  };

  const handleDeleteConfirm = async (id) => {
    try {
      const res = await deleteTodo(id);
      setTodos((prev) => prev.filter((t) => t.id !== id));
      addNotification(res.message || 'Task deleted successfully', 'success');
    } catch (err) {
      addNotification(err.message || 'Failed to delete task', 'error');
      throw err;
    }
  };

  return (
    <div className="app-container">
      <Navbar
        apiStatus={apiStatus}
        isCheckingHealth={isCheckingHealth}
        onCheckHealth={() => {
          verifyHealth();
          fetchTodos();
        }}
      />

      {errorMessage && (
        <div className="error-banner">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertCircle size={20} />
            <span>{errorMessage}</span>
          </div>
          <button
            className="btn btn-secondary"
            style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
            onClick={fetchTodos}
          >
            <RefreshCw size={14} /> Retry
          </button>
        </div>
      )}

      <TodoForm onAddTodo={handleAddTodo} />

      <TodoList
        todos={todos}
        isLoading={isLoading}
        activeFilter={activeFilter}
        onFilterChange={setActiveFilter}
        onToggleTodo={handleToggleTodo}
        onEditTodo={(todo) => setEditingTodo(todo)}
        onDeleteTodo={(todo) => setDeletingTodo(todo)}
        onRefresh={fetchTodos}
      />

      {/* Edit Modal */}
      <EditTodoModal
        todo={editingTodo}
        isOpen={Boolean(editingTodo)}
        onClose={() => setEditingTodo(null)}
        onSave={handleEditSave}
      />

      {/* Delete Confirmation Modal */}
      <DeleteConfirmModal
        todo={deletingTodo}
        isOpen={Boolean(deletingTodo)}
        onClose={() => setDeletingTodo(null)}
        onConfirm={handleDeleteConfirm}
      />

      {/* Toast Notifications */}
      <Notification
        notifications={notifications}
        onDismiss={dismissNotification}
      />
    </div>
  );
}
