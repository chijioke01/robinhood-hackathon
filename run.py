from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Issue
from extensions import db  # Import db from extensions
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


@app.route('/')
def index():
    return "Hello, World!"


""" USER MANAGEMENTS ENDPOINTS """
##########################################################################################
"""USER REGISTER ENDPOINT """
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    # Validate the received data
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify(message="Name, email, and password are required!"), 400

    # Check if the email is already in use
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify(message="Email is already in use!"), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # Create a new user
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully!"), 201


""" USER LOGIN ENPOINT """
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(message="Email and password are required!"), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify(message="User not found!"), 404

    if not check_password_hash(user.password, password):
        return jsonify(message="Incorrect password!"), 401

    session['user_id'] = user.user_id
    return jsonify(message="Login successful!")

"""USER PROFILE ENDPOINT """
@app.route('/profile', methods=['GET'])
def get_profile():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return jsonify(message="Please log in to view profile."), 401

    user = User.query.get(session['user_id'])

    # Check if the user exists in the database (this should always be true, but it's good to check)
    if not user:
        return jsonify(message="User not found!"), 404

    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'zip_code': user.zip_code,
        'registration_date': user.registration_date.strftime('%Y-%m-%d %H:%M:%S') if user.registration_date else None,
        'total_points': user.total_points
    }

    return jsonify(profile=user_data)

""" USER LOGOUT ENPOINT"""
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify(message="Logged out successfully!")

##########################################################################################

"""ISSUE REPORTING ENDPOINTS"""
##########################################################################################

""" REPORT USER ENDPOINT """
@app.route('/report', methods=['POST'])
def report_issue():
    if 'user_id' not in session:
        return jsonify(message="Please log in to report an issue."), 401

    data = request.json
    issue_type = data.get('issue_type')
    photo_url = data.get('photo_url', '')  # Optional field
    location = data.get('location')
    # Assuming the status is always set to 'open' when reported
    issue_status = 'open'

    if not issue_type or not location:
        return jsonify(message="Issue type and location are required!"), 400

    new_issue = Issue(
        user_id=session['user_id'],
        issue_type=issue_type,
        photo_url=photo_url,
        location=location,
        issue_status=issue_status,
        date_reported=datetime.utcnow()
    )

    db.session.add(new_issue)
    db.session.commit()

    return jsonify(message="Issue reported successfully!", issue_id=new_issue.issue_id), 201

""" GET ISSUES ENPOINT """

@app.route('/issues', methods=['GET'])
def get_issues():
    issues = Issue.query.all()
    # Convert the list of issues into a list of dictionaries
    output = []
    for issue in issues:
        issue_data = {
            'issue_id': issue.issue_id,
            'user_id': issue.user_id,
            'issue_type': issue.issue_type,
            'photo_url': issue.photo_url,
            'location': issue.location,
            'issue_status': issue.issue_status,
            'date_reported': issue.date_reported.strftime('%Y-%m-%d %H:%M:%S')  # format the datetime object to string
        }
        output.append(issue_data)
    
    return jsonify(issues=output)

""" UPDATE ISSUE STATUS ENDPOINT """
@app.route('/api/issues/<int:issue_id>/status', methods=['PUT'])
def update_issue_status(issue_id):
    data = request.json
    new_status = data.get('status')
    
    # Validate the new status
    if not new_status:
        return jsonify(message="Status is required!"), 400

    # Check if the status is one of the predefined statuses (you can adjust this list)
    if new_status not in ['open', 'in progress', 'closed']:
        return jsonify(message="Invalid status!"), 400

    issue = Issue.query.get(issue_id)
    if not issue:
        return jsonify(message="Issue not found!"), 404

    issue.issue_status = new_status
    db.session.commit()

    return jsonify(message="Issue status updated successfully!")
##########################################################################################


if __name__ == "__main__":
    app.run(debug=True)
