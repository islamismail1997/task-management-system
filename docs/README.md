1. Project Title and Description:

# Task Management and Report Subscription System

This project is a Flask-based backend system for managing tasks and sending task reports to subscribed users. It includes features such as user authentication, task management (CRUD operations), and automated report generation for daily, weekly, and monthly frequencies.
____________________________________________________________________________________________________________________

2. Table of Contents:

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
____________________________________________________________________________________________________________________

3. Features:

## Features
- **Authentication**: Sign-Up and Sign-In functionality with JWT-based authentication.
- **Task Management**:
  - Create, Retrieve, Update, and Delete tasks.
  - Batch delete tasks within a specified date range.
  - Restore the last deleted task.
- **Report Subscription**:
  - Subscribe to daily, weekly, or monthly task reports.
  - Automated email delivery of task reports.
- **Automated Scheduling**:
  - Reports are generated and sent based on the subscription frequency.

____________________________________________________________________________________________________________________

4.  Technologies Used:

## Technologies Used
- **Backend Framework**: Flask
- **Database**: SQLite
- **Scheduler**: APScheduler
- **Email Service**: Flask-Mail
- **Programming Language**: Python
- **API Documentation**: Postman

____________________________________________________________________________________________________________________

5. Setup Instructions:

## Setup Instructions
1. **Clone the Repository**:
     git clone https://github.com/islamismail1997/task-management-system.git
         cd task-management-system
2. **Create and Activate Virtual Environment**:
        python -m venv env
            env\Scripts\activate
3. **Install Dependencies**:
        pip install -r requirements.txt
4. **Set Up Environment Variables**:
    -Create a .env file in the root directory and add the following:
        SECRET_KEY=your_secret_key
        MAIL_SERVER=smtp.gmail.com
        MAIL_PORT=587
        MAIL_USE_TLS=True
        MAIL_USERNAME=your_email@gmail.com
        MAIL_PASSWORD=your_email_password
____________________________________________________________________________________________________________________

6. How to Run:
### how to run
    - Run the Application:
        python run.py
____________________________________________________________________________________________________________________

7. API Documentation:

## api documentation
    - The full API documentation is included in the Postman collection.
    - You can import the `docs/TaskManagementAPI.postman_collection.json` file into Postman to view and test all endpoints.

____________________________________________________________________________________________________________________

8. Project Structure:

## project structure

Task Managment project/
├── app/
│   ├── __init__.py       # App factory and initialization
│   ├── models.py         # Database models
│   ├── routes/
│   │   ├── auth.py       # Authentication routes
│   │   ├── tasks.py      # Task routes
│   │   ├── subscriptions.py  # Subscription routes
├── docs/
│   ├── TaskManagementAPI.postman_collection.json  # Postman collection file
│   ├── README.md        # Project README file
├── requirements.txt     # Python dependencies
├── run.py               # Entry point to run the Flask app


