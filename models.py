from extensions import db  # Import db from extensions
# from extensions import db  # Import db from extensions


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(120), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=True)
    total_points = db.Column(db.Integer, nullable=False)

    # relationship 
    issues = db.relationship('Issue', backref='reporter', lazy=True)


class Issue(db.Model):
    issue_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    issue_type = db.Column(db.String(20), nullable=False)
    photo_url = db.Column(db.String(256), nullable=True)
    location = db.Column(db.String(120), nullable=False)
    issue_status = db.Column(db.String(120), nullable=False)
    date_reported = db.Column(db.DateTime, nullable=False)
