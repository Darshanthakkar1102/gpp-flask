from ..extensions import db

class Department(db.Model):
    __tablename__ = 'department'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    hod_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_department_hod'))
    
    # Relationships
    users = db.relationship('User', backref='department', foreign_keys='User.department_id')
    hod = db.relationship('User', foreign_keys=[hod_id], backref='department_led')
    
    def __repr__(self):
        return f'<Department {self.name}>'
