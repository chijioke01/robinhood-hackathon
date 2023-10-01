from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Issue
from extensions import db  # Import db from extensions
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')


""" USER MANAGEMENTS ENDPOINTS """
##########################################################################################
"""USER REGISTER ENDPOINT """
@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    data = request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    confirm_password = data.get('confPass')



    #validate that the password is equal to confirmed pass!
    if password != confirm_password:
        return jsonify(message="Passwords dont match!"), 400
    
    # Validate the received data
    if not data or not name or not email or not password:
        return jsonify(message="Name, email, and password are required!"), 400

    # Check if the email is already in use
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(message="Email is already in use!"), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(name=name, email=email, password=hashed_password, zip_code=95120, total_points=0)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('onboarding'))


""" USER LOGIN ENPOINT """
@app.route('/login', methods=['POST'])
def login():
    data = request.form
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
    return redirect(url_for('dashboard'))

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
@app.route('/logout', methods=['POST'])
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

    # Get form data
    issue_type = request.form.get('issue_type')
    location = request.form.get('location')

    # Get the uploaded photo (if any)
    photo = request.files.get('photo')
    photo_url = ''  # Placeholder. You might want to save the photo and then store the URL here.
    # Assuming the status is always set to 'open' when reported
    issue_status = 'open'

    # Extract latitude and longitude from the form
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))

    if not issue_type or not location:
        return jsonify(message="Issue type and location are required!"), 400

    if photo:
        # Save the photo or upload it to a cloud storage and get the URL
        pass

    new_issue = Issue(
        user_id=session['user_id'],
        issue_type=issue_type,
        photo_url=photo_url,
        location=location,
        latitude=latitude,
        longitude=longitude,
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
@app.route('/issues/<int:issue_id>/status', methods=['PUT'])
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

"""ERROR HANDLING """
##########################################################################################
@app.errorhandler(404)
def not_found_error(error):
    return jsonify(message="Resource not found."), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback the session in case of database errors
    return jsonify(message="An internal error occurred."), 500


"""FRONT END """

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/report', methods=['GET', 'POST'])
def report_form():
    if request.method == 'POST':
        # Handle the form submission logic here
        pass
    return render_template('issue_reporting.html')


@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')


if __name__ == "__main__":
    app.run(debug=True)
