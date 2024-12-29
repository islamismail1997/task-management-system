# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Copy the .env file to the container
COPY .env /app/.env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app's port
EXPOSE 5000

# Set environment variables (use default values for Docker)
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["python", "run.py"]
