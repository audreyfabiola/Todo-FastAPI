from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

todos = {}

next_todo_id = 1  # Initialize the ID counter

class Todo(BaseModel):
    title: str
    id: int
    completed: bool = False

class UpdateTodo(BaseModel):
    title: Optional[str] = None
    id: Optional[int] = None
    completed: Optional[bool] = None

@app.get("/")
def index():
    return {"message": "Welcome to the Todo FastAPI!"}

# Get all todo items
@app.get("/todos/all")
def get_all_todos():
    return list(todos.values())

# Post todo (create new todo object in todos list)
@app.post("/todos")
def create_todo(todo: Todo):
    global next_todo_id  # Use the global variable for ID incrementation
    todo.id = next_todo_id  
    todos[next_todo_id] = todo
    next_todo_id += 1 
    return todo

# Query parameters (solely function parameters)
@app.get("/todos")
def get_todo_by_title(title: str):
    for todo_id in todos:
        if todos[todo_id].title == title:
            return todos[todo_id]
    return {"Error": f"Todo item with title '{title}' not found."}

# Get todo by id
@app.get("/todos/get/{todo_id}")
def get_todo_by_id(todo_id: int):
    if todo_id not in todos:
        return {"Error": f"Todo item with ID {todo_id} not found."}
    return todos[todo_id]

# Update todo
@app.put("/todos/put/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    if todo_id not in todos:
        return {"Error": f"Todo item with ID {todo_id} does not exist."}

    if todo.title != None:
        todos[todo_id].title = todo.title
    if todo.completed != None:
        todos[todo_id].completed = todo.completed

    return todos[todo_id]

# Delete todo by id
@app.delete("/todos/delete/{todo_id}")
def delete_todo_by_id(todo_id: int):
    if todo_id not in todos:
        return {"Error": f"Todo item with ID {todo_id} does not exist."}
    del todos[todo_id]
    return {"Message": "Todo item deleted successfully."}

# Delete todo by title
@app.delete("/todos/delete_by_title")
def delete_todo_by_title(title: str):
    for todo_id, todo in list(todos.items()):  
        if todo.title == title:
            del todos[todo_id]
            return {"Message": f"Todo item with title '{title}' deleted successfully."}
    return {"Error": f"Todo item with title '{title}' does not exist."}

# Delete all todos
@app.delete("/todos/delete_all")
def delete_all_todos():
    todos.clear()
    return {"Message": "All todo items deleted successfully."}