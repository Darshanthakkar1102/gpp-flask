from ..extensions import db
from flask_security import UserMixin, RoleMixin
import uuid
from datetime import datetime

# Association table for user roles
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id', name='fk_roles_users_user')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id', name='fk_roles_users_role'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    
    # Profile fields
    name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    enrollment_no = db.Column(db.String(20), unique=True)
    semester = db.Column(db.Integer)
    
    # Department relationship
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    
    # Approval fields
    is_approved = db.Column(db.Boolean, default=False)
    approval_date = db.Column(db.DateTime)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_approver'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    roles = db.relationship('Role', secondary='roles_users',
                          backref=db.backref('users', lazy='dynamic'))
    approved_by = db.relationship('User', remote_side=[id],
                                backref='approved_users')
    
    def __str__(self):
        return f"{self.email} ({', '.join(role.name for role in self.roles)})"
    
    @property
    def is_admin(self):
        return any(role.name == 'admin' for role in self.roles)
    
    def has_role(self, role):
        """Check if user has the specified role"""
        return any(r.name == role for r in self.roles)
