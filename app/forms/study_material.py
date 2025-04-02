from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class StudyMaterialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    material_type = SelectField('Material Type', 
                              choices=[
                                  ('lab_manual', 'Lab Manual'),
                                  ('lecture_notes', 'Lecture Notes'),
                                  ('slides', 'PowerPoint Slides'),
                                  ('gtu_solutions', 'GTU Paper Solutions'),
                                  ('revision_notes', 'Revision Notes')
                              ],
                              validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx'], 'Only PDF and Office documents are allowed!')
    ])
    submit = SubmitField('Upload Material')
