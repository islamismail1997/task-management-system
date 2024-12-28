from flask import Blueprint, request, jsonify
from app.models import Task, DeletedTask
from app import db
from functools import wraps
import jwt
from datetime import datetime, timedelta

tasks_bp = Blueprint('tasks', __name__)

# Middleware to ensure the user is authenticated
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

# Create a Task
@tasks_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user_id):
    """Allows a user to create a task."""
    data = request.get_json()

    # Validate required fields
    required_fields = ['title', 'start_date', 'due_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"'{field}' is a required field."}), 400

    # Validate date formats
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S')
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"message": "Invalid date format! Use YYYY-MM-DDTHH:MM:SS."}), 400

    # Create the task
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        start_date=start_date,
        due_date=due_date,
        status=data.get('status', 'Pending'),
        user_id=current_user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully!'}), 201

# Retrieve Tasks with Filters
@tasks_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user_id):
    """Fetch tasks for the authenticated user with optional filters."""
    status = request.args.get('status')  # Optional status filter
    start_date = request.args.get('start_date')  # Optional date range filter
    end_date = request.args.get('end_date')  # Optional date range filter

    query = Task.query.filter_by(user_id=current_user_id)  # Filter tasks by user ID
    if status:
        query = query.filter_by(status=status)  # Apply status filter

    if start_date or end_date:
        # Check for invalid or missing dates
        if not start_date or not end_date:
            return jsonify({"message": "Both start_date and end_date are required for date filtering!"}), 400
        try:
            # Validate and parse dates
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Task.due_date >= start_date, Task.due_date < end_date)
        except ValueError:
            return jsonify({"message": "Invalid date format for filters! Use YYYY-MM-DD."}), 400

    tasks = query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'start_date': task.start_date.isoformat(),
        'due_date': task.due_date.isoformat(),
        'status': task.status
    } for task in tasks]), 200

# Update a Task
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user_id, task_id):
    """Allows a user to update their task."""
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return jsonify({'message': 'Task not found!'}), 404

    data = request.get_json()

    # Validate allowed fields
    allowed_fields = ['title', 'description', 'start_date', 'due_date', 'status']
    for key in data.keys():
        if key not in allowed_fields:
            return jsonify({'message': f"'{key}' is not a valid field!"}), 400

    # Update fields if present
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'start_date' in data:
        try:
            task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({"message": "Invalid date format for 'start_date'. Use YYYY-MM-DDTHH:MM:SS."}), 400
    if 'due_date' in data:
        try:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({"message": "Invalid date format for 'due_date'. Use YYYY-MM-DDTHH:MM:SS."}), 400
    if 'status' in data:
        task.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Task updated successfully!'}), 200


# Delete a Task
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user_id, task_id):
    """Allows a user to delete their task."""
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return jsonify({'message': 'Task not found!'}), 404

    deleted_task = DeletedTask(
        title=task.title,
        description=task.description,
        start_date=task.start_date,
        due_date=task.due_date,
        completion_date=task.completion_date,
        status=task.status,
        user_id=task.user_id,
        deleted_at=datetime.utcnow()
    )
    db.session.add(deleted_task)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully!'}), 200

# Restore Last Deleted Task
@tasks_bp.route('/tasks/restore', methods=['POST'])
@token_required
def restore_last_deleted_task(current_user_id):
    """Restore the last deleted task."""
    deleted_task = DeletedTask.query.filter_by(user_id=current_user_id).order_by(DeletedTask.deleted_at.desc()).first()
    if not deleted_task:
        return jsonify({'message': 'No recently deleted task found!'}), 404

    restored_task = Task(
        title=deleted_task.title,
        description=deleted_task.description,
        start_date=deleted_task.start_date,
        due_date=deleted_task.due_date,
        completion_date=deleted_task.completion_date,
        status=deleted_task.status,
        user_id=deleted_task.user_id
    )
    db.session.add(restored_task)
    db.session.delete(deleted_task)
    db.session.commit()

    return jsonify({'message': 'Task restored successfully!'}), 200

# Batch Delete Tasks
@tasks_bp.route('/tasks', methods=['DELETE'])
@token_required
def batch_delete_tasks(current_user_id):
    """Delete tasks within a specific date range."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'message': 'start_date and end_date are required!'}), 400

    try:
        # Convert query parameters to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Include the entire end date
    except ValueError:
        return jsonify({'message': 'Invalid date format! Use YYYY-MM-DD.'}), 400

    # Query tasks within the date range
    tasks_to_delete = Task.query.filter(
        Task.user_id == current_user_id,
        Task.due_date >= start_date,
        Task.due_date < end_date  # Use '<' to include all tasks until the end of the day
    ).all()

    if not tasks_to_delete:
        return jsonify({'message': 'No tasks found within the specified date range.'}), 404

    # Save tasks to DeletedTask table and delete them
    for task in tasks_to_delete:
        deleted_task = DeletedTask(
            title=task.title,
            description=task.description,
            start_date=task.start_date,
            due_date=task.due_date,
            completion_date=task.completion_date,
            status=task.status,
            user_id=task.user_id,
            deleted_at=datetime.utcnow()
        )
        db.session.add(deleted_task)
        db.session.delete(task)

    db.session.commit()

    return jsonify({'message': f'{len(tasks_to_delete)} tasks deleted successfully!'}), 200


