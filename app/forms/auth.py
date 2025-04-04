from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from ..models.department import Department

class ExtendedRegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
        ('hod', 'HOD'),
        ('librarian', 'Librarian'),
        ('principal', 'Principal'),
        ('store_officer', 'Store Officer')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.department.choices = [(0, 'Select Department')] + [
            (dept.id, dept.name) for dept in Department.query.order_by('name')
        ]

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Login As', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
        ('hod', 'HOD'),
        ('librarian', 'Librarian'),
        ('principal', 'Principal'),
        ('store_officer', 'Store Officer'),
        ('admin', 'Administrator')
    ], validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
