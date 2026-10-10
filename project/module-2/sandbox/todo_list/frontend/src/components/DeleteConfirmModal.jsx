import React, { useState } from 'react';
import { AlertTriangle, Trash2 } from 'lucide-react';

export default function DeleteConfirmModal({ todo, isOpen, onClose, onConfirm }) {
  const [isDeleting, setIsDeleting] = useState(false);

  if (!isOpen || !todo) return null;

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onConfirm(todo.id);
      onClose();
    } catch (err) {
      // Handled by parent or toast
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--color-danger)', marginBottom: '1rem' }}>
          <AlertTriangle size={24} />
          <h3 className="modal-title" style={{ color: 'var(--color-text-main)' }}>Delete Task</h3>
        </div>

        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
          Are you sure you want to delete <strong style={{ color: 'var(--color-text-main)' }}>"{todo.title}"</strong>? This action cannot be undone.
        </p>

        <div className="modal-footer">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onClose}
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button
            type="button"
            className="btn btn-danger"
            onClick={handleDelete}
            disabled={isDeleting}
          >
            {isDeleting ? (
              <>
                <span className="spinner"></span> Deleting...
              </>
            ) : (
              <>
                <Trash2 size={18} /> Delete
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
