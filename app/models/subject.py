from app.extensions import db

class Subject(db.Model):
    __tablename__ = 'subject'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    
    # Relationships
    department = db.relationship('Department', backref='subjects')

    def __repr__(self):
        return f'<Subject {self.code} - {self.name}>'
