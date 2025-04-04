from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from ..models.department import Department

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Profile')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.department.choices = [(0, 'Select Department')] + [
            (dept.id, dept.name) for dept in Department.query.order_by('name')
        ]
