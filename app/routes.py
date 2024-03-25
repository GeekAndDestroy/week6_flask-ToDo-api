from flask import request
from app import app
from fake_data.tasks import tasks_list

# Define a route
@app.route("/")
def index():
    return 'This is just an empty page for now...'

@app.route('/tasks') # Show all tasks
def get_tasks():
    tasks = tasks_list
    return tasks

@app.route('/tasks/<int:task_id>') # Show task by ID
def get_post(task_id):
    tasks = tasks_list
    for task in tasks:
        if task['id'] == task_id:
            return task
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

    new_task = {
        'id': len(tasks_list) + 1,
        'title': title,
        'description': description,
        'userId': 1,
        'dateCreated': '2024-03-25T15:21:35',
        'likes': 0
    }

    tasks_list.append(new_task)
    
    return new_task, 201
