import json
import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Constants & Paths
DATA_FILE = os.path.join(os.path.dirname(__file__), "todos.json")

# Helper for Pydantic v1 & v2 compatibility
def dump_model(model: BaseModel, **kwargs):
    if hasattr(model, "model_dump"):
        return model.model_dump(**kwargs)
    return model.dict(**kwargs)

# Pydantic Models
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: Optional[str] = Field(None, description="Detailed description of the todo item")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoItem(TodoBase):
    id: str
    completed: bool = False
    created_at: str
    updated_at: str

# Helper functions for JSON storage
def read_todos_from_file() -> List[dict]:
    if not os.path.exists(DATA_FILE):
        write_todos_to_file([])
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        write_todos_to_file([])
        return []

def write_todos_to_file(todos: List[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)

# FastAPI App
app = FastAPI(
    title="Todo List API",
    description="A simple FastAPI backend for managing Todo items stored in a JSON file.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "Todo List API is running"}

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy"}

@app.get("/api/todos", response_model=List[TodoItem], tags=["Todos"])
def get_todos(completed: Optional[bool] = Query(None, description="Filter by completed status")):
    todos = read_todos_from_file()
    if completed is not None:
        todos = [todo for todo in todos if todo.get("completed") == completed]
    return todos

@app.get("/api/todos/{todo_id}", response_model=TodoItem, tags=["Todos"])
def get_todo(todo_id: str = Path(..., description="The ID of the todo item")):
    todos = read_todos_from_file()
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID '{todo_id}' not found")

@app.post("/api/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED, tags=["Todos"])
def create_todo(todo_in: TodoCreate):
    todos = read_todos_from_file()
    now_iso = datetime.utcnow().isoformat()
    new_todo = {
        "id": str(uuid.uuid4()),
        "title": todo_in.title,
        "description": todo_in.description,
        "completed": False,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    todos.append(new_todo)
    write_todos_to_file(todos)
    return new_todo

@app.put("/api/todos/{todo_id}", response_model=TodoItem, tags=["Todos"])
def update_todo(todo_id: str, todo_in: TodoUpdate):
    todos = read_todos_from_file()
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            updated_data = dump_model(todo_in, exclude_unset=True)
            if not updated_data:
                return todo
            todo.update(updated_data)
            todo["updated_at"] = datetime.utcnow().isoformat()
            todos[i] = todo
            write_todos_to_file(todos)
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID '{todo_id}' not found")

@app.patch("/api/todos/{todo_id}", response_model=TodoItem, tags=["Todos"])
def patch_todo(todo_id: str, todo_in: TodoUpdate):
    return update_todo(todo_id, todo_in)

@app.patch("/api/todos/{todo_id}/toggle", response_model=TodoItem, tags=["Todos"])
def toggle_todo_completed(todo_id: str):
    todos = read_todos_from_file()
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            todo["updated_at"] = datetime.utcnow().isoformat()
            todos[i] = todo
            write_todos_to_file(todos)
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID '{todo_id}' not found")

@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_200_OK, tags=["Todos"])
def delete_todo(todo_id: str):
    todos = read_todos_from_file()
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted_todo = todos.pop(i)
            write_todos_to_file(todos)
            return {"message": f"Todo '{deleted_todo['title']}' deleted successfully", "id": todo_id}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID '{todo_id}' not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
