from datetime import datetime
from app.extensions import db

class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    material_type = db.Column(db.String(50), nullable=False)  # Lab Manual, Lecture Notes, etc.
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    subject = db.relationship('Subject', backref='study_materials')
    faculty = db.relationship('User', backref='uploaded_materials')

    def __repr__(self):
        return f'<StudyMaterial {self.title}>'
