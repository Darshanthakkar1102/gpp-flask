from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class StudyMaterialForm(FlaskForm):
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    semester = SelectField('Semester', 
                         choices=[(i, f"Semester {i}") for i in range(1, 9)],
                         coerce=int,
                         validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    material_type = SelectField('Material Type', 
                              choices=[
                                  ('lab_manual', 'Lab Manual'),
                                  ('lecture_notes', 'Lecture Notes'),
                                  ('slides', 'PowerPoint Slides'),
                                  ('gtu_solutions', 'GTU Paper Solutions'),
                                  ('revision_notes', 'Revision Notes'),
                                  ('assignments', 'Assignments'),
                                  ('question_papers', 'Question Papers')
                              ],
                              validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx'], 'Only PDF and Office documents are allowed!')
    ])
    submit = SubmitField('Upload Material')
