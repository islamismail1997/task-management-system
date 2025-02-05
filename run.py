from app import create_app  # Import the app factory function from app/__init__.py

# Create the Flask app instance
app = create_app()

# if __name__ == '__main__':
#     # Run the Flask development server
#     app.run(debug=True)


# Run the Docker(changing the Default host)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
