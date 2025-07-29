from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(20), default='student')  # 'student' or 'teacher'
    notes = db.relationship('Note')
    grades = db.relationship('Grade', foreign_keys='Grade.student_id', backref='student', lazy=True)
    taught_grades = db.relationship('Grade', foreign_keys='Grade.teacher_id', backref='teacher', lazy=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grades = db.relationship('Grade', backref='subject', lazy=True)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    max_value = db.Column(db.Float, default=20.0)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
