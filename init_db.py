from app import create_app
from app.extensions import db
from app.models.user import User, Role
from app.models.department import Department
from app.models.project import Project
from app.models.subject import Subject
from flask_security.utils import hash_password
from datetime import datetime
import argparse
import uuid

app = create_app()

def init_base():
    """Initialize basic database structure and roles."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default roles if they don't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='Regular User')
            db.session.add(user_role)
        
        # Create default department if it doesn't exist
        default_dept = Department.query.filter_by(name='General').first()
        if not default_dept:
            default_dept = Department(name='General')
            db.session.add(default_dept)
        
        db.session.commit()
        print("Base database initialized successfully!")

def create_admin():
    """Create admin user if it doesn't exist."""
    with app.app_context():
        # Get admin role
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Error: Admin role not found. Please run init_base first.")
            return False

        # Check if admin user exists
        admin_email = 'admin@gppalanpur.in'
        admin_user = User.query.filter_by(email=admin_email).first()
        
        if not admin_user:
            # Create admin user
            admin_user = User(
                email=admin_email,
                password=hash_password('admin123'),
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                confirmed_at=datetime.utcnow(),
                first_name='Admin',
                last_name='User',
                is_approved=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
            return True
        else:
            print("Admin user already exists!")
            return True

def create_departments():
    """Create sample departments."""
    departments = [
        'Computer Engineering',
        'Mechanical Engineering',
        'EC (Electronics & Communication)',
        'IT (Information Technology)',
        'Civil Engineering',
        'Electrical Engineering',
        'ICT (Information and Communication Technology)'
    ]
    
    with app.app_context():
        # First, delete all existing departments
        Department.query.delete()
        db.session.commit()
        
        # Then add our new departments
        for dept_name in departments:
            dept = Department(name=dept_name)
            db.session.add(dept)
            print(f"Added department: {dept_name}")
        
        db.session.commit()
        print("Sample departments created successfully!")

def create_subjects():
    """Create sample subjects."""
    with app.app_context():
        # Get Computer Engineering department
        comp_dept = Department.query.filter_by(name='Computer Engineering').first()
        if not comp_dept:
            print("Error: Computer Engineering department not found.")
            return False

        sample_subjects = [
            {
                'code': 'CS101',
                'name': 'Introduction to Programming',
                'semester': 1,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS102',
                'name': 'Digital Electronics',
                'semester': 1,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS201',
                'name': 'Data Structures',
                'semester': 2,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS202',
                'name': 'Computer Networks',
                'semester': 2,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS301',
                'name': 'Database Management Systems',
                'semester': 3,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS302',
                'name': 'Object Oriented Programming',
                'semester': 3,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS401',
                'name': 'Operating Systems',
                'semester': 4,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS402',
                'name': 'Software Engineering',
                'semester': 4,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS501',
                'name': 'Web Development',
                'semester': 5,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS502',
                'name': 'Artificial Intelligence',
                'semester': 5,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS601',
                'name': 'Cloud Computing',
                'semester': 6,
                'department_id': comp_dept.id
            },
            {
                'code': 'CS602',
                'name': 'Project Management',
                'semester': 6,
                'department_id': comp_dept.id
            }
        ]

        for subject_data in sample_subjects:
            subject = Subject.query.filter_by(code=subject_data['code']).first()
            if not subject:
                subject = Subject(**subject_data)
                db.session.add(subject)
                print(f"Added subject: {subject_data['code']} - {subject_data['name']}")

        db.session.commit()
        print("Sample subjects created successfully!")
        return True

def create_sample_projects():
    """Create sample projects."""
    with app.app_context():
        # Get Computer Engineering department
        comp_dept = Department.query.filter_by(name='Computer Engineering').first()
        if not comp_dept:
            print("Error: Computer Engineering department not found.")
            return False

        sample_projects = [
            {
                'title': 'AI-Powered Attendance System',
                'description': 'An attendance system using facial recognition and machine learning.',
                'status': 'ongoing',
                'department_id': comp_dept.id
            },
            {
                'title': 'Smart Parking System',
                'description': 'IoT-based parking system with real-time space detection.',
                'status': 'completed',
                'department_id': comp_dept.id
            },
            {
                'title': 'Student Performance Analytics',
                'description': 'Data analytics platform for tracking and improving student performance.',
                'status': 'pending',
                'department_id': comp_dept.id
            }
        ]

        for project_data in sample_projects:
            project = Project.query.filter_by(title=project_data['title']).first()
            if not project:
                project = Project(**project_data)
                db.session.add(project)

        db.session.commit()
        print("Sample projects created successfully!")
        return True

def init_all():
    """Initialize everything in the correct order."""
    print("Initializing database...")
    init_base()
    if create_admin():
        create_departments()
        create_subjects()
        create_sample_projects()
    print("Database initialization complete!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize the database with various options')
    parser.add_argument('--all', action='store_true', help='Initialize everything (default)')
    parser.add_argument('--base', action='store_true', help='Initialize base database structure only')
    parser.add_argument('--admin', action='store_true', help='Create admin user only')
    parser.add_argument('--departments', action='store_true', help='Create departments only')
    parser.add_argument('--subjects', action='store_true', help='Create sample subjects only')
    parser.add_argument('--projects', action='store_true', help='Create sample projects only')
    
    args = parser.parse_args()
    
    # If no arguments provided or --all specified, run everything
    if not any(vars(args).values()) or args.all:
        init_all()
    else:
        if args.base:
            init_base()
        if args.admin:
            create_admin()
        if args.departments:
            create_departments()
        if args.subjects:
            create_subjects()
        if args.projects:
            create_sample_projects()
