
# Task Management and Report Subscription System

This project is a Flask-based backend system for managing tasks and sending task reports to subscribed users. It includes features such as user authentication, task management (CRUD operations), and automated report generation for daily, weekly, and monthly frequencies.

____________________________________________________________________________________________________________________

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions-how-to-run)
- [API Documentation](#api-documentation)
- [Using Docker](#using-docker)
- [Project Structure](#project-structure)

____________________________________________________________________________________________________________________

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

## Technologies Used
- **Backend Framework**: Flask
- **Database**: SQLite
- **Scheduler**: APScheduler
- **Email Service**: Flask-Mail
- **Programming Language**: Python
- **API Documentation**: Postman

____________________________________________________________________________________________________________________

## Setup Instructions-How to Run
1. **Clone the Repository**:
     
    git clone https://github.com/islamismail1997/task-management-system.git
    cd task-management-system
     

2. **Create and Activate Virtual Environment**:
     
    python -m venv env
    env\Scripts\activate
     

3. **Install Dependencies**:
     
    pip install -r requirements.txt
     

4. **Set Up Environment Variables**:
    - Create a `.env` file in the root directory and add the following:
        
      SECRET_KEY=your_secret_key
      MAIL_SERVER=smtp.gmail.com
      MAIL_PORT=587
      MAIL_USE_TLS=True
      MAIL_USE_SSL=False
      MAIL_USERNAME=your_email@gmail.com
      MAIL_PASSWORD=your_email_password
       

5. **Run the Application**:
     
    python run.py
     

____________________________________________________________________________________________________________________

## API Documentation
- Postman Collection: [Task Management API Postman Collection](docs/TaskManagementAPI.postman_collection.json)
- The full API documentation is included in the Postman collection.
- You can import the `docs/TaskManagementAPI.postman_collection.json` file into Postman to view and test all endpoints.

____________________________________________________________________________________________________________________

## Using Docker

This project includes Docker support for containerized deployment and testing.

### **Steps to Run with Docker**
1. **Build the Docker Image**:
    - Open a terminal in the project directory and run:
       
      docker build -t task-management-system .
       

2. **Run the Docker Container**:
    - Start the container and map it to port 5000:
       
      docker run -p 5000:5000 task-management-system
       
    - The application will be accessible at `http://localhost:5000`.

### **Using Docker Compose**
1. **Run the Application**:
    - Docker Compose simplifies running the app with predefined configurations:
       
      docker-compose up --build
       

2. **Access the Application**:
    - Navigate to `http://localhost:5000`.

3. **Stop the Application**:
    - To stop the running services:
       
      docker-compose down
       

### **Environment Variables**
The `.env` file is used to configure sensitive settings such as email credentials and the Flask secret key. Ensure the `.env` file is in the project root before running the Docker container.

#### Example `.env` File:
  
SECRET_KEY=a3c5f2b7e9d62e4c23d1a45f7b8c2d9e3f1c4a6e7f8b9d2a3e4f1c6d7a8b9e1f
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=Your_Email@gmail.com
MAIL_PASSWORD=Your App Pass from Gmail settings

____________________________________________________________________________________________________________________

## Project Structure

![alt text](<Project Structure.png>)
