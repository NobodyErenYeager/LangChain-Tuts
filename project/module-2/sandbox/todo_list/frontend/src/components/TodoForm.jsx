import React, { useState } from 'react';
import { PlusCircle, Loader2 } from 'lucide-react';

export default function TodoForm({ onAddTodo }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedTitle = title.trim();

    if (!trimmedTitle) {
      setError('Title is required (minimum 1 character)');
      return;
    }

    setError('');
    setIsSubmitting(true);

    try {
      await onAddTodo({
        title: trimmedTitle,
        description: description.trim() || null,
      });
      setTitle('');
      setDescription('');
    } catch (err) {
      setError(err.message || 'Failed to create todo item');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card">
      <h2 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '1rem', color: 'var(--color-text-main)' }}>
        Add New Task
      </h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="todo-title">Title *</label>
          <input
            id="todo-title"
            type="text"
            className="form-control"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError('');
            }}
            disabled={isSubmitting}
          />
          {error && <div className="form-error">{error}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="todo-description">Description (Optional)</label>
          <textarea
            id="todo-description"
            className="form-control"
            placeholder="Add details, notes, or links..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isSubmitting}
            rows={2}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting || !title.trim()}
          >
            {isSubmitting ? (
              <>
                <span className="spinner"></span> Creating...
              </>
            ) : (
              <>
                <PlusCircle size={18} /> Add Task
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
