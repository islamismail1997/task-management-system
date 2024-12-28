from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_mail import Mail
from flask_apscheduler import APScheduler
import os
import logging

# Load environment variables from the .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()  # SQLAlchemy instance for database operations
mail = Mail()  # Flask-Mail instance for sending emails
scheduler = APScheduler()  # APScheduler instance for scheduling tasks
scheduler_started = False  # Flag to track if the scheduler has already been started


def create_app():
    """App Factory: Configures and creates the Flask application."""
    global scheduler_started  # Declare global variable to update its value

    app = Flask(__name__)

    # Application Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_key_for_development')  # Secret key for sessions and JWT
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy modification tracking warnings

    # Email Configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  # Mail server (e.g., SMTP server)
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))  # Mail server port
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'  # Use TLS for secure email communication
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Email account username (from .env)
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Email account password (from .env)

    # Initialize extensions
    db.init_app(app)  # Bind SQLAlchemy to the Flask app
    mail.init_app(app)  # Bind Flask-Mail to the app

    # Ensure all tables are created if they don't already exist
    with app.app_context():
        db.create_all()

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.tasks import tasks_bp
    from .routes.subscriptions import subscriptions_bp
    app.register_blueprint(auth_bp)  # Register authentication blueprint
    app.register_blueprint(tasks_bp)  # Register tasks blueprint
    app.register_blueprint(subscriptions_bp)  # Register subscriptions blueprint

    # Start the scheduler
    if not scheduler_started:
        scheduler.init_app(app)
        scheduler.remove_all_jobs()  # Clear existing jobs
        print("All existing scheduler jobs removed")

        # Import the function for generating and sending reports
        from app.routes.subscriptions import generate_and_send_reports

        # Daily Report Generation Job
        if not scheduler.get_job("Daily Task Report Generation"):
            scheduler.add_job(
                id="Daily Task Report Generation",
                func=lambda: safe_task_execution(generate_and_send_reports, 'daily'),
                trigger="interval",
                hours=24,  # For testing minute=1 is used; adjust to hours=24 for production
                max_instances=1  # Prevent overlapping executions
            )
            print("Daily Task Report Generation job added")

        # Weekly Report Generation Job
        if not scheduler.get_job("Weekly Task Report Generation"):
            scheduler.add_job(
                id="Weekly Task Report Generation",
                func=lambda: safe_task_execution(generate_and_send_reports, 'weekly'),
                trigger="cron",
                day_of_week="mon",
                hour=8,
                max_instances=1
            )
            print("Weekly Task Report Generation job added")

        # Monthly Report Generation Job
        if not scheduler.get_job("Monthly Task Report Generation"):
            scheduler.add_job(
                id="Monthly Task Report Generation",
                func=lambda: safe_task_execution(generate_and_send_reports, 'monthly'),
                trigger="cron",
                day=1,
                hour=8,
                max_instances=1
            )
            print("Monthly Task Report Generation job added")

        scheduler.start()
        scheduler_started = True
        print("Scheduler started")

    # Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]  # Print logs to the console
    )

    return app


def safe_task_execution(task, frequency):
    """Safely execute scheduled tasks to handle errors gracefully."""
    from app import create_app  # Import the app factory function
    app = create_app()  # Create the app instance

    with app.app_context():
        try:
            task(frequency)  # Pass the frequency to the task
        except Exception as e:
            logging.error(f"Scheduled task execution failed for {frequency} reports: {e}")
