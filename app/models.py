from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime, nullable=True,)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # def __init__(self, ):
        