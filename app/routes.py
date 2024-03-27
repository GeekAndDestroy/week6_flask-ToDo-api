from flask import request, render_template
from app import app, db
from .models import Task
from datetime import datetime

# Define a route
@app.route("/")
def index():
    return 'This is just an empty page for now...'

@app.route('/tasks') # Show all tasks
def get_tasks():
    select_stmt = db.select(Task)
    search = request.args.get('search')
    if search:
        select_stmt = select_stmt.where(Task.completed.ilike(f"%{search}%"))
    # get the posts from database
    tasks = db.session.execute(select_stmt).scalars().all()
    return [t.to_dict() for t in tasks]

@app.route('/tasks/<int:task_id>') # Show task by ID
def get_post(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f"Task with an ID of {task_id} does not exist"}, 404

@app.route('/tasks', methods=['POST']) # Create new task
def create_task():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    title = data.get('title')
    description = data.get('description')

    new_task =  Task(title=title, description=description)

    # tasks_list.append(new_task)
    
    return new_task.to_dict(), 201
