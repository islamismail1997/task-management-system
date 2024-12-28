from flask import Blueprint, request, jsonify
from app.models import Subscription, Task, User  # Models for database interaction
from app import db, mail  # Database and mail instances
from flask_mail import Message  # Class for sending emails
from functools import wraps
import jwt
import os
from datetime import datetime, timedelta

# Blueprint for Subscription Routes
subscriptions_bp = Blueprint('subscriptions', __name__)

# Middleware to ensure the user is authenticated
def token_required(f):
    """Middleware to ensure the user is authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')  # Extract the JWT token from headers
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # Decode the JWT token
            data = jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
            current_user_id = data['user_id']  # Extract user ID from token payload
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user_id, *args, **kwargs)  # Pass the user ID to the wrapped function
    return decorated

# Subscribe to Task Reports
@subscriptions_bp.route('/subscriptions', methods=['POST'])
@token_required
def subscribe(current_user_id):
    """Allows a user to subscribe to task reports."""
    data = request.get_json()

    # Validate required fields
    start_date = data.get('start_date')  # Required: Subscription start date
    frequency = data.get('frequency')  # Required: Frequency (daily, weekly, monthly)
    report_time = data.get('report_time')  # Required: Report time (hour only)

    if not start_date or not frequency or not report_time:
        return jsonify({'message': 'Missing required fields!'}), 400

    try:
        # Validate and parse the start_date
        datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid start_date format! Use YYYY-MM-DDTHH:MM:SS.'}), 400

    if frequency not in ['daily', 'weekly', 'monthly']:
        return jsonify({'message': 'Invalid frequency! Must be daily, weekly, or monthly.'}), 400

    try:
        report_time = int(report_time)
        if report_time < 0 or report_time > 23:
            raise ValueError
    except ValueError:
        return jsonify({'message': 'Invalid report_time! Must be between 0 and 23.'}), 400

    # Check if the user already has a subscription
    existing_subscription = Subscription.query.filter_by(user_id=current_user_id).first()
    if existing_subscription:
        return jsonify({'message': 'You are already subscribed!'}), 400

    # Align start_date to report_time
    start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S').replace(
        hour=report_time, minute=0, second=0, microsecond=0
    )

    # Create and save the new subscription
    new_subscription = Subscription(
        start_date=start_date,
        frequency=frequency,
        report_time=report_time,
        user_id=current_user_id
    )
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify({'message': 'Subscribed successfully!'}), 201


    # # Create and save the new subscription
    # new_subscription = Subscription(
    #     start_date=start_date,
    #     frequency=frequency,
    #     report_time=int(report_time),
    #     user_id=current_user_id
    # )
    # db.session.add(new_subscription)
    # db.session.commit()
    # return jsonify({'message': 'Subscribed successfully!'}), 201


# Unsubscribe from Task Reports
@subscriptions_bp.route('/subscriptions', methods=['DELETE'])
@token_required
def unsubscribe(current_user_id):
    """Allows a user to unsubscribe from task reports."""
    subscription = Subscription.query.filter_by(user_id=current_user_id).first()
    if not subscription:
        return jsonify({'message': 'No subscription found!'}), 404

    # Delete the subscription
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({'message': 'Unsubscribed successfully!'}), 200

# Send Task Report Email
def send_task_report(user_email, tasks):
    """Send an email containing the task report."""
    # group tasks by their status in the email report
    grouped_tasks = {
        "Pending": [task for task in tasks if task.status == "Pending"],
        "Completed": [task for task in tasks if task.status == "Completed"],
        "Overdue": [task for task in tasks if task.status == "Overdue"]
    }

    # Format the email body
    email_body = "<html><body><h2>Your Task Report</h2>"
    for status, task_list in grouped_tasks.items():
        email_body += f"<h3>{status} Tasks</h3><ul>"
        for task in task_list:
            email_body += f"<li>{task.title} (Due: {task.due_date})</li>"
        email_body += "</ul>"
    email_body += "</body></html>"

    # Create and send the email
    msg = Message(
        subject="Your Task Report",
        sender=os.getenv('MAIL_USERNAME'),
        recipients=[user_email]
    )
    msg.html = email_body  # Send as HTML
    mail.send(msg)

# Generate and send reports
def generate_and_send_reports(frequency):
    """Generate and send task reports to subscribed users based on frequency."""
    subscriptions = Subscription.query.filter_by(frequency=frequency).all()  # Get subscriptions for this frequency

    for subscription in subscriptions:
        user = User.query.get(subscription.user_id)  # Get the subscribed user
        if not user:
            print(f"No user found for subscription ID {subscription.id}")
            continue

        print(f"Processing {frequency} subscription for {user.email}")

        # Determine the date range for the report
        end_date = datetime.utcnow()
        if frequency == 'daily':
            start_date = end_date - timedelta(days=1)
        elif frequency == 'weekly':
            start_date = end_date - timedelta(weeks=1)
        elif frequency == 'monthly':
            start_date = end_date - timedelta(days=30)
        else:
            print(f"Invalid frequency '{frequency}' for subscription ID {subscription.id}")
            continue

        print(f"Date range for {user.email}: {start_date} to {end_date}")

        # Fetch tasks due within the date range for the user
        tasks = Task.query.filter(
            Task.user_id == subscription.user_id,
            Task.due_date >= start_date,
            Task.due_date <= end_date
        ).all()

        if not tasks:
            print(f"No tasks found for user {user.email} within the range {start_date} to {end_date}.")
            continue  # Skip if no tasks found

        print(f"Tasks found for user {user.email}: {[task.title for task in tasks]}")

        # Send the task report email
        try:
            send_task_report(user.email, tasks)
            print(f"Report sent to {user.email}")
        except Exception as e:
            print(f"Error sending report to {user.email}: {e}")



# Test Route for Subscriptions Blueprint
@subscriptions_bp.route('/subscriptions/test', methods=['GET'])
def test_subscription():
    """Test route to verify the Subscriptions Blueprint."""
    return {"message": "Subscriptions Blueprint is working!"}
