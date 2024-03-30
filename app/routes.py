from flask import request, render_template
from app import app, db
from .models import Task, User
from .auth import basic_auth, token_auth

# Define a route
@app.route("/") #Index/documentation
def index():
    return render_template('index.html')




# USER ENDPOINTS

@app.route('/users', methods=['POST'])  # create new user
def create_user():
    #Check to make sure that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # GET the data from the request body
    data = request.json

    #Validate that the data has all the required fields
    required_fields = ['username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Pull the individual data from the body
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
   # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where( (User.username == username) | (User.email == email) )).scalars().all()
    if check_users:
        return {'error': "A user with that username and/or email already exists"}, 400 
        
    # Create a new instance of user with the data from the request
    new_user = User(email=email, password=password, username=username)
    
    return new_user.to_dict(), 201





@app.route('/users/<int:user_id>') # Show user by user_id
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return user.to_dict()
    else:
        return {'error': f"User with an ID of {user_id} does not exist"}, 404
    


    
@app.route('/users/<int:user_id>', methods=['PUT']) # Update User Endpoint
@token_auth.login_required
def edit_user(user_id):
    # Check to see that they have a JSON body
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    # Let's the find post in the db
    user = db.session.get(User, user_id)
    if user is None:
        return {'error': f"User with ID #{user_id} does not exist"}, 404
    # Get the current user based on the token
    current_user = token_auth.current_user()
    # Check if the current user is the author of the post
    if current_user.user_id is not user.user_id:
        return {'error': "This is not you. You do not have permission to edit"}, 403
    
    # Get the data from the request
    data = request.json
    # Pass that data into the post's update method
    user.update(**data)
    return user.to_dict()




@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    # based on the post_id parameter check to see Post exists
    user = db.session.get(User, user_id)
    
    if user is None:
        return {'error': f'User with ID #{user_id} does not exist. Please try again'}, 404
    
    #Make sure user trying to delete post is the user whom created it
    current_user = token_auth.current_user()
    if current_user.user_id is not user.user_id:
        return {'error': 'You do not have permission to delete this user'}, 403
    
    #delete the post
    user.delete()
    return {'success': f"{user_id} was successfully deleted"}, 200



# TOKEN ENDPOINT

@app.route('/token') # get token
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    return user.get_token()



# TASK ENDPOINTS

@app.route('/tasks') # Show all tasks
def get_tasks():
    select_stmt = db.select(Task)
    search = request.args.get('search')
    if search:
        # select_stmt = select_stmt.where(Post.title.like(f"%{search}%"))
        select_stmt = select_stmt.where(Task.completed == search.lower())
    # get the posts from database
    tasks = db.session.execute(select_stmt).scalars().all()
    return [t.to_dict() for t in tasks]




@app.route('/tasks/complete') # Show all completed tasks
def get_complete():
    select_stmt = db.select(Task)
    tasks = db.session.execute(select_stmt.where(Task.completed == True)).scalars().all()
    return [t.to_dict() for t in tasks]




@app.route('/tasks/incomplete') # Show all incomplete tasks
def get_incomplete():
    select_stmt = db.select(Task)
    tasks = db.session.execute(select_stmt.where(Task.completed == False)).scalars().all()
    return [t.to_dict() for t in tasks]




@app.route('/tasks/<int:task_id>') # Show task by ID
def get_post(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f"Task with an ID of {task_id} does not exist"}, 404
    

@app.route('/me') # Show logged in user's tasks
@token_auth.login_required 
def get_my_tasks():
    current_user = token_auth.current_user()
    tasks = db.session.execute(db.select(Task).where(Task.author == current_user)).scalars().all()
    return [t.to_dict() for t in tasks]




@app.route('/tasks', methods=['POST']) # Create new task
@token_auth.login_required
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

    current_user = token_auth.current_user()

    new_task =  Task(title=title, description=description, user_id=current_user.user_id)

    return new_task.to_dict(), 201




@app.route('/tasks/<int:task_id>', methods=['PUT']) # Update Task Endpoint
@token_auth.login_required
def edit_task(task_id):
    # Check to see that they have a JSON body
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    # Let's the find post in the db
    task = db.session.get(Task, task_id)
    if task is None:
        return {'error': f"Task with ID #{task_id} does not exist"}, 404
    # Get the current user based on the token
    current_user = token_auth.current_user()
    # Check if the current user is the author of the post
    if current_user is not task.author:
        return {'error': "This is not your task. You do not have permission to edit"}, 403
    
    # Get the data from the request
    data = request.json
    # Pass that data into the post's update method
    task.update(**data)
    return task.to_dict()




@app.route('/tasks/<int:task_id>', methods=['DELETE']) # Delete task by ID
@token_auth.login_required
def delete_task(task_id):
    # based on the post_id parameter check to see Post exists
    task = db.session.get(Task, task_id)
    
    if task is None:
        return {'error': f'Task with {task_id} does not exist. Please try again'}, 404
    
    #Make sure user trying to delete post is the user whom created it
    current_user = token_auth.current_user()
    if task.author is not current_user:
        return {'error': 'You do not have permission to delete this post'}, 403
    
    #delete the post
    task.delete()
    return {'success': f"{task.title} was successfully deleted"}, 200
