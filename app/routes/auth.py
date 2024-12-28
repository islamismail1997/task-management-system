from flask import Blueprint, request, jsonify  # Import Flask utilities.
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing.
from app.models import User  # Import the User model.
from app import db  # Import the database instance.
import jwt  # Library for JWT token handling.
import datetime  # For handling date and time.
import pytz

auth_bp = Blueprint('auth', __name__)  # Create a blueprint for authentication routes.

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Allows a user to sign up with a unique email."""
    data = request.get_json()  # Get JSON payload from the request.
    
        # Validate required fields # Additional step (not mentioned in the project) to handle the missing fields in the Json Request
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Bad request - missing fields."}), 400
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')  # Hash the user's password securely.

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():  # Query the database for existing email.
        return jsonify({'message': 'User with this email already exists!'}), 400

    # Create a new user
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)  # Add the new user to the database session.
    db.session.commit()  # Commit the transaction to save the user.
    return jsonify({'message': 'User created successfully!'}), 201  # Return success response.

@auth_bp.route('/signin', methods=['POST'])
def signin():
    """Allows a user to log in and receive a JWT."""
    data = request.get_json()  # Get JSON payload from the request.
    
        # Validate required fields
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Bad request - missing fields."}), 400
    
    user = User.query.filter_by(email=data['email']).first()  # Query the user by email.

    if not user or not check_password_hash(user.password, data['password']):  # Validate email and password.
        return jsonify({'message': 'Invalid credentials!'}), 401  # Return error if credentials are invalid.

    # Generate JWT
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)},  # Payload.
        'your_secret_key',  # Secret key.
        algorithm="HS256"  # Encryption algorithm.
    )
    return jsonify({'token': token}), 200  # Return the token as a response.
