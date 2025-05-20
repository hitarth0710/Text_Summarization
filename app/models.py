from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import json


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to summaries
    summaries = db.relationship('Summary', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.commit()


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    original_text = db.Column(db.Text)
    summary_text = db.Column(db.Text)
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Store parameters used for summarization
    parameters = db.Column(db.Text)  # Stored as JSON

    # Statistics
    original_length = db.Column(db.Integer)  # Word count of original text
    summary_length = db.Column(db.Integer)  # Word count of summary
    compression_ratio = db.Column(db.Float)  # Summary length / Original length
    processing_time = db.Column(db.Float)  # Time taken to generate summary

    def __repr__(self):
        return f'<Summary {self.title[:30]}>'

    def set_parameters(self, params_dict):
        self.parameters = json.dumps(params_dict)

    def get_parameters(self):
        if self.parameters:
            return json.loads(self.parameters)
        return {}

    @property
    def shortened_original(self):
        """Return a shortened version of the original text for display"""
        if len(self.original_text) > 300:
            return self.original_text[:300] + '...'
        return self.original_text

    @property
    def formatted_date(self):
        """Return a nicely formatted date"""
        return self.created_at.strftime('%B %d, %Y at %H:%M')


# User loader for Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))