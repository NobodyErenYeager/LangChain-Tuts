import React, { useState, useEffect } from 'react';
import { X, Save } from 'lucide-react';

export default function EditTodoModal({ todo, isOpen, onClose, onSave }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [completed, setCompleted] = useState(false);
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (todo) {
      setTitle(todo.title || '');
      setDescription(todo.description || '');
      setCompleted(Boolean(todo.completed));
      setError('');
    }
  }, [todo]);

  if (!isOpen || !todo) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedTitle = title.trim();

    if (!trimmedTitle) {
      setError('Title cannot be empty');
      return;
    }

    setError('');
    setIsSaving(true);

    try {
      await onSave(todo.id, {
        title: trimmedTitle,
        description: description.trim() || null,
        completed: completed,
      });
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to update todo item');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Edit Task</h3>
          <button className="btn-icon" onClick={onClose} disabled={isSaving}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="edit-title">Title *</label>
            <input
              id="edit-title"
              type="text"
              className="form-control"
              value={title}
              onChange={(e) => {
                setTitle(e.target.value);
                if (error) setError('');
              }}
              disabled={isSaving}
            />
            {error && <div className="form-error">{error}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="edit-description">Description</label>
            <textarea
              id="edit-description"
              className="form-control"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isSaving}
              rows={3}
            />
          </div>

          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1rem' }}>
            <input
              id="edit-completed"
              type="checkbox"
              className="todo-checkbox"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
              disabled={isSaving}
            />
            <label htmlFor="edit-completed" style={{ margin: 0, cursor: 'pointer', fontWeight: 500 }}>
              Mark as Completed
            </label>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={isSaving}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSaving || !title.trim()}
            >
              {isSaving ? (
                <>
                  <span className="spinner"></span> Saving...
                </>
              ) : (
                <>
                  <Save size={18} /> Save Changes
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
