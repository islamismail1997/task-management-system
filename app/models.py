from app import db  # Import the database object from the app module.

class User(db.Model):
    """Represents a User in the database."""
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the User table.
    username = db.Column(db.String(50), nullable=False)  # User's username, required.
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email address, required.
    password = db.Column(db.String(200), nullable=False)  # Hashed password, required.

class Task(db.Model):
    """Represents a Task created by a user."""
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Task table.
    title = db.Column(db.String(100), nullable=False)  # Title of the task, required.
    description = db.Column(db.Text, nullable=True)  # Description of the task, optional.
    start_date = db.Column(db.DateTime, nullable=False)  # Task start date, required.
    due_date = db.Column(db.DateTime, nullable=False)  # Task due date, required.
    completion_date = db.Column(db.DateTime, nullable=True)  # Completion date, optional.
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Task status (Pending, Completed, etc.).
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to the User table.

class Subscription(db.Model):
    """Represents a subscription for task reports."""
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Subscription table.
    start_date = db.Column(db.DateTime, nullable=False)  # Date the subscription starts, required.
    frequency = db.Column(db.String(10), nullable=False)  # Frequency of the report (daily, weekly, monthly), required.
    report_time = db.Column(db.Integer, nullable=False)  # Hour of the day for report generation, required.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to the User table.
    
class DeletedTask(db.Model):
    """Represents a recently deleted task for temporary storage."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    user_id = db.Column(db.Integer, nullable=False)  # ID of the user who owns the task
    deleted_at = db.Column(db.DateTime, nullable=False)  # Timestamp when the task was deleted
