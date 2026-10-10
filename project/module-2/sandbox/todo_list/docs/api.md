# Todo List API Documentation

Backend API documentation for the FastAPI Todo List application. Frontend developers can use this guide to integrate with the backend without inspecting the source code.

---

## General Configuration

- **Base URL**: `http://localhost:8000`
- **Port**: `8000`
- **API Version**: `1.0.0`
- **Data Storage**: Single JSON file (`backend/todos.json`)
- **Authentication**: None (Public API)
- **CORS**: Allowed for all origins (`*`), HTTP methods (`*`), and headers (`*`)
- **Default Headers**:
  - Request: `Content-Type: application/json`
  - Response: `Content-Type: application/json`

---

## Data Models

### 1. `TodoItem`
Represents a complete Todo object returned by the API.

| Field | Type | Description | Required | Constraints / Default |
|---|---|---|---|---|
| `id` | `string` | Unique identifier (UUID v4) | Yes (Server-generated) | e.g. `"e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e"` |
| `title` | `string` | Title of the todo item | Yes | Non-empty string (`min_length=1`) |
| `description` | `string` \| `null` | Detailed description | No | Default: `null` |
| `completed` | `boolean` | Completion status | Yes | Default: `false` |
| `created_at` | `string` | ISO 8601 UTC timestamp of creation | Yes (Server-generated) | e.g. `"2025-02-22T10:00:00.000000"` |
| `updated_at` | `string` | ISO 8601 UTC timestamp of last update | Yes (Server-generated) | e.g. `"2025-02-22T10:00:00.000000"` |

### 2. `TodoCreate`
Payload schema for creating a new todo item.

| Field | Type | Description | Required | Constraints / Default |
|---|---|---|---|---|
| `title` | `string` | Title of the todo item | Yes | Must be at least 1 character long |
| `description` | `string` \| `null` | Detailed description | No | Default: `null` |

### 3. `TodoUpdate`
Payload schema for updating an existing todo item. All fields are optional.

| Field | Type | Description | Required | Constraints / Default |
|---|---|---|---|---|
| `title` | `string` | Updated title | No | Must be at least 1 character long if provided |
| `description` | `string` \| `null` | Updated description | No | `null` or string |
| `completed` | `boolean` | Updated completion status | No | `true` or `false` |

---

## Standard Error Response Schemas

### 404 Not Found
Returned when requesting or updating a non-existent todo item.

```json
{
  "detail": "Todo with ID 'e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e' not found"
}
```

### 422 Unprocessable Entity
Returned when validation fails (e.g., missing required `title`, title shorter than 1 character, invalid data types).

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "title"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Endpoints

### Health Check

#### 1. `GET /`
Check API root status.

- **HTTP Method**: `GET`
- **Path**: `/`
- **Tags**: `Health Check`
- **Parameters**: None
- **Request Body**: None
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    {
      "status": "ok",
      "message": "Todo List API is running"
    }
    ```

#### 2. `GET /health`
Check service health status.

- **HTTP Method**: `GET`
- **Path**: `/health`
- **Tags**: `Health Check`
- **Parameters**: None
- **Request Body**: None
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    {
      "status": "healthy"
    }
    ```

---

### Todos Management

#### 3. `GET /api/todos`
Retrieve a list of all todo items, optionally filtered by completion status.

- **HTTP Method**: `GET`
- **Path**: `/api/todos`
- **Tags**: `Todos`
- **Query Parameters**:
  | Name | Type | Required | Description |
  |---|---|---|---|
  | `completed` | `boolean` | No | Filter todos by completion status (`true` or `false`). Omit parameter to return all todos. |

- **Request Body**: None
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Array of `TodoItem` objects.
  - **Example**:
    ```json
    [
      {
        "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e",
        "title": "Buy groceries",
        "description": "Milk, eggs, and bread",
        "completed": false,
        "created_at": "2025-02-22T10:00:00.000000",
        "updated_at": "2025-02-22T10:00:00.000000"
      },
      {
        "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "title": "Complete documentation",
        "description": null,
        "completed": true,
        "created_at": "2025-02-22T09:00:00.000000",
        "updated_at": "2025-02-22T09:30:00.000000"
      }
    ]
    ```

---

#### 4. `POST /api/todos`
Create a new todo item.

- **HTTP Method**: `POST`
- **Path**: `/api/todos`
- **Tags**: `Todos`
- **Parameters**: None
- **Request Body**:
  - **Content-Type**: `application/json`
  - **Schema**: `TodoCreate`
  - **Example**:
    ```json
    {
      "title": "Buy groceries",
      "description": "Milk, eggs, and bread"
    }
    ```
- **Response**:
  - **Status Code**: `201 Created`
  - **Body**: Created `TodoItem` object.
  - **Example**:
    ```json
    {
      "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e",
      "title": "Buy groceries",
      "description": "Milk, eggs, and bread",
      "completed": false,
      "created_at": "2025-02-22T10:00:00.000000",
      "updated_at": "2025-02-22T10:00:00.000000"
    }
    ```
- **Error Responses**:
  - `422 Unprocessable Entity`: Validation failure if `title` is missing or empty.

---

#### 5. `GET /api/todos/{todo_id}`
Retrieve a single todo item by its unique ID.

- **HTTP Method**: `GET`
- **Path**: `/api/todos/{todo_id}`
- **Tags**: `Todos`
- **Path Parameters**:
  | Name | Type | Required | Description |
  |---|---|---|---|
  | `todo_id` | `string` | Yes | The ID of the todo item (UUID v4 string) |

- **Request Body**: None
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: `TodoItem` object.
  - **Example**:
    ```json
    {
      "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e",
      "title": "Buy groceries",
      "description": "Milk, eggs, and bread",
      "completed": false,
      "created_at": "2025-02-22T10:00:00.000000",
      "updated_at": "2025-02-22T10:00:00.000000"
    }
    ```
- **Error Responses**:
  - `404 Not Found`: No todo item matches `todo_id`.

---

#### 6. `PUT /api/todos/{todo_id}`
Update an existing todo item.

- **HTTP Method**: `PUT`
- **Path**: `/api/todos/{todo_id}`
- **Tags**: `Todos`
- **Path Parameters**:
  | Name | Type | Required | Description |
  |---|---|---|---|
  | `todo_id` | `string` | Yes | The ID of the todo item |

- **Request Body**:
  - **Content-Type**: `application/json`
  - **Schema**: `TodoUpdate`
  - **Example**:
    ```json
    {
      "title": "Buy groceries and snacks",
      "description": "Milk, eggs, bread, and chips",
      "completed": true
    }
    ```
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Updated `TodoItem` object.
  - **Example**:
    ```json
    {
      "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e",
      "title": "Buy groceries and snacks",
      "description": "Milk, eggs, bread, and chips",
      "completed": true,
      "created_at": "2025-02-22T10:00:00.000000",
      "updated_at": "2025-02-22T10:15:00.000000"
    }
    ```
- **Error Responses**:
  - `404 Not Found`: No todo item matches `todo_id`.
  - `422 Unprocessable Entity`: Validation failure (e.g., `title` set to an empty string).

---

#### 7. `PATCH /api/todos/{todo_id}`
Partially update an existing todo item.

- **HTTP Method**: `PATCH`
- **Path**: `/api/todos/{todo_id}`
- **Tags**: `Todos`
- **Path Parameters**:
  | Name | Type | Required | Description |
  |---|---|---|---|
  | `todo_id` | `string` | Yes | The ID of the todo item |

- **Request Body**:
  - **Content-Type**: `application/json`
  - **Schema**: `TodoUpdate`
  - **Example**:
    ```json
    {
      "completed": true
    }
    ```
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Updated `TodoItem` object.
  - **Example**:
    ```json
    {
      "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e",
      "title": "Buy groceries",
      "description": "Milk, eggs, and bread",
      "completed": true,
      "created_at": "2025-02-22T10:00:00.000000",
      "updated_at": "2025-02-22T10:20:00.000000"
    }
    ```
- **Error Responses**:
  - `404 Not Found`: No todo item matches `todo_id`.
  - `422 Unprocessable Entity`: Validation failure.

---

#### 8. `PATCH /api/todos/{todo_id}/toggle`
Toggle the `completed` status of a todo item (flips `false` to `true` or `true` to `false`).

- **HTTP Method**: `PATCH`
- **Path**: `/api/todos/{todo_id}/toggle`
- **Tags**: `Todos`
- **Path Parameters**:
  | Name | Type | Required | Description |
  |---|---|---|---|
  | `todo_id` | `string` | Yes | The ID of the todo item |

- **Request Body**: None
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Updated `TodoItem` object with toggled `completed` value and updated `updated_at` timestamp.
  - **Example**:
    ```json
    {
      "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e",
      "title": "Buy groceries",
      "description": "Milk, eggs, and bread",
      "completed": true,
      "created_at": "2025-02-22T10:00:00.000000",
      "updated_at": "2025-02-22T10:25:00.000000"
    }
    ```
- **Error Responses**:
  - `404 Not Found`: No todo item matches `todo_id`.

---

#### 9. `DELETE /api/todos/{todo_id}`
Delete a todo item by its unique ID.

- **HTTP Method**: `DELETE`
- **Path**: `/api/todos/{todo_id}`
- **Tags**: `Todos`
- **Path Parameters**:
  | Name | Type | Required | Description |
  |---|---|---|---|
  | `todo_id` | `string` | Yes | The ID of the todo item |

- **Request Body**: None
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Confirmation message object.
  - **Example**:
    ```json
    {
      "message": "Todo 'Buy groceries' deleted successfully",
      "id": "e4a2c1b3-4f5a-6b7c-8d9e-0f1a2b3c4d5e"
    }
    ```
- **Error Responses**:
  - `404 Not Found`: No todo item matches `todo_id`.

---

## Implementation Notes & Observed Behaviors

1. **PUT vs PATCH Behavior**: In the current implementation, `PUT /api/todos/{todo_id}` delegates to the same logic as `PATCH /api/todos/{todo_id}` (`exclude_unset=True`). Both endpoints perform partial updates rather than strictly replacing the entire object. Unsupplied fields in the payload remain unchanged on the resource.
2. **Empty Update Body**: Sending an empty JSON object `{}` to `PUT` or `PATCH` returns the item unchanged without altering its `updated_at` field or rewriting the JSON persistence file.
3. **DELETE Response**: Deleting a resource returns HTTP status `200 OK` with a JSON payload `{"message": "...", "id": "..."}`, rather than standard HTTP `204 No Content`.
4. **Timestamps**: `created_at` and `updated_at` are formatted as UTC ISO strings without a trailing `Z` timezone designator (e.g. `"2025-02-22T10:00:00.000000"`).
5. **Interactive OpenAPI / Swagger Docs**: FastAPI automatically generates interactive UI documentation at `http://localhost:8000/docs` and Redoc documentation at `http://localhost:8000/redoc`.
