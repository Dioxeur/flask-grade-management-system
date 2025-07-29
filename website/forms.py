from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from website.models import User, Subject
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email format'),
        Length(max=150, message='Email too long')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email format'),
        Length(max=150, message='Email too long')
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=150, message='First name must be 2-150 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher')], 
                      validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Choose a different one.')
    
    def validate_first_name(self, first_name):
        if not re.match(r'^[a-zA-Z\s\-\'\.]+$', first_name.data):
            raise ValidationError('First name contains invalid characters.')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[
        DataRequired(message='Subject name is required'),
        Length(min=2, max=100, message='Subject name must be 2-100 characters')
    ])
    code = StringField('Subject Code', validators=[
        DataRequired(message='Subject code is required'),
        Length(min=2, max=20, message='Subject code must be 2-20 characters')
    ])
    
    def validate_name(self, name):
        if not re.match(r'^[a-zA-Z\s\-&]+$', name.data):
            raise ValidationError('Subject name contains invalid characters.')
    
    def validate_code(self, code):
        if not re.match(r'^[A-Z0-9\-]+$', code.data.upper()):
            raise ValidationError('Subject code must contain only letters, numbers, and hyphens.')

class AddGradeForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    value = DecimalField('Grade Value', validators=[
        DataRequired(message='Grade value is required'),
        NumberRange(min=0, max=100, message='Grade must be between 0 and 100')
    ])
    max_value = DecimalField('Maximum Points', validators=[
        DataRequired(message='Maximum points is required'),
        NumberRange(min=0.1, max=100, message='Maximum points must be between 0.1 and 100')
    ], default=20.0)
    
    def __init__(self, *args, **kwargs):
        super(AddGradeForm, self).__init__(*args, **kwargs)
        # Populate student choices
        self.student_id.choices = [(user.id, f"{user.first_name} ({user.email})") 
                                  for user in User.query.filter_by(role='student').all()]

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[
        DataRequired(message='Note content is required'),
        Length(min=1, max=1000, message='Note must be 1-1000 characters')
    ])
    
    def validate_note(self, note):
        # Basic XSS prevention - no script tags
        if '<script' in note.data.lower() or '</script>' in note.data.lower():
            raise ValidationError('Invalid content detected.')

