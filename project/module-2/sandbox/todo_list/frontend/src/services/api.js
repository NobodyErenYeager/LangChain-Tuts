const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Helper function to parse error response from backend API
 */
async function handleResponse(response) {
  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`;
    try {
      const errorData = await response.json();
      if (typeof errorData.detail === 'string') {
        errorMessage = errorData.detail;
      } else if (Array.isArray(errorData.detail)) {
        // FastAPI validation errors
        errorMessage = errorData.detail
          .map((err) => {
            const field = err.loc ? err.loc.join('.') : 'field';
            return `${field}: ${err.msg}`;
          })
          .join(', ');
      } else if (errorData.message) {
        errorMessage = errorData.message;
      }
    } catch {
      // Failed to parse JSON error, fall back to default message
    }
    throw new Error(errorMessage);
  }
  return response.json();
}

/**
 * Health check endpoint
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await handleResponse(response);
  } catch (error) {
    // Try root endpoint as fallback
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      return await handleResponse(response);
    } catch (fallbackError) {
      throw new Error(`Unable to connect to backend server at ${API_BASE_URL}`);
    }
  }
}

/**
 * Get all todo items with optional completion status filter
 * @param {boolean|null} completed - Filter by completion status if provided
 */
export async function getTodos(completed = null) {
  let url = `${API_BASE_URL}/api/todos`;
  if (completed !== null && completed !== undefined) {
    url += `?completed=${Boolean(completed)}`;
  }
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
}

/**
 * Get single todo item by ID
 * @param {string} id - Todo item ID
 */
export async function getTodoById(id) {
  const response = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
}

/**
 * Create a new todo item
 * @param {Object} data - { title: string, description?: string | null }
 */
export async function createTodo({ title, description = null }) {
  const response = await fetch(`${API_BASE_URL}/api/todos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      title: title.trim(),
      description: description ? description.trim() : null,
    }),
  });
  return handleResponse(response);
}

/**
 * Update a todo item (title, description, and/or completed status)
 * @param {string} id - Todo item ID
 * @param {Object} data - { title?: string, description?: string | null, completed?: boolean }
 */
export async function updateTodo(id, { title, description, completed }) {
  const body = {};
  if (title !== undefined) body.title = title.trim();
  if (description !== undefined) body.description = description ? description.trim() : null;
  if (completed !== undefined) body.completed = completed;

  const response = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify(body),
  });
  return handleResponse(response);
}

/**
 * Toggle the completion status of a todo item
 * @param {string} id - Todo item ID
 */
export async function toggleTodo(id) {
  const response = await fetch(`${API_BASE_URL}/api/todos/${id}/toggle`, {
    method: 'PATCH',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
}

/**
 * Delete a todo item by ID
 * @param {string} id - Todo item ID
 */
export async function deleteTodo(id) {
  const response = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
}
