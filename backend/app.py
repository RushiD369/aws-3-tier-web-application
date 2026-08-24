import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Allow frontend requests during local development.
# Later this can be restricted to your actual S3/CloudFront domain.
CORS(app)

# ---------------------------------------------------
# Database Configuration
# ---------------------------------------------------

# Local development:
# SQLite database stored in backend/app.db
#
# Later on AWS:
# DATABASE_URL will point to Amazon RDS MySQL.

database_url = os.getenv("DATABASE_URL")

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------------------------------------------
# Database Model
# ---------------------------------------------------

class UserSubmission(db.Model):
    __tablename__ = "user_submissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }


# ---------------------------------------------------
# Create Database Tables
# ---------------------------------------------------

with app.app_context():
    db.create_all()


# ---------------------------------------------------
# Health Check API
# ---------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "AWS 3-Tier Web Application"
    }), 200


# ---------------------------------------------------
# Submit Data API
# ---------------------------------------------------

@app.route("/submit-data", methods=["POST"])
def submit_data():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No JSON data received"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Basic validation
    if not name or not email or not message:
        return jsonify({
            "success": False,
            "message": "Name, email and message are required"
        }), 400

    submission = UserSubmission(
        name=name,
        email=email,
        message=message
    )

    db.session.add(submission)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Data submitted successfully",
        "data": submission.to_dict()
    }), 201


# ---------------------------------------------------
# Get Submitted Data
# ---------------------------------------------------

@app.route("/users", methods=["GET"])
def get_users():

    submissions = UserSubmission.query.order_by(
        UserSubmission.id.desc()
    ).all()

    return jsonify([
        submission.to_dict()
        for submission in submissions
    ]), 200


# ---------------------------------------------------
# Run Application
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
