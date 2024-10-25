from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    onboarding_documents = db.relationship('Document', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # This will store the path to the uploaded document
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Document {self.document_type} for User {self.user_id}>'
