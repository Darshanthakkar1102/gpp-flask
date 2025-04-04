from ..extensions import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    exam_id = db.Column(db.String(20))
    exam_type = db.Column(db.String(20))
    exam_name = db.Column(db.String(100))
    declaration_date = db.Column(db.DateTime)
    academic_year = db.Column(db.String(20))
    semester = db.Column(db.Integer)
    institute_code = db.Column(db.String(20))
    institute_name = db.Column(db.String(100))
    course_name = db.Column(db.String(100))
    branch_code = db.Column(db.String(10))
    branch_name = db.Column(db.String(100))
    
    # Result details
    total_credits = db.Column(db.Float)
    total_grade_points = db.Column(db.Float)
    sgpa = db.Column(db.Float)
    result_status = db.Column(db.String(20))  # PASS/FAIL
    
    # Subject results (store as JSON)
    subject_results = db.Column(db.JSON)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Result {self.student_id} {self.exam_name}>'
    
    def __repr__(self):
        return f'<Result {self.student_id} {self.exam_name}>'
