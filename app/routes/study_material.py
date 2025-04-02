import os
from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_security import login_required, current_user, roles_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.study_material import StudyMaterial
from app.models.subject import Subject
from app.models.department import Department
from app.forms.study_material import StudyMaterialForm

bp = Blueprint('study_material', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx', 'ppt', 'pptx'}

@bp.route('/materials/upload', methods=['GET', 'POST'])
@login_required
@roles_required('faculty')
def upload_material():
    form = StudyMaterialForm()
    
    # Populate department choices
    form.department.choices = [(d.id, d.name) for d in Department.query.order_by('name').all()]
    
    if request.method == 'GET':
        # If department is selected, populate subjects for that department and semester
        if request.args.get('department') and request.args.get('semester'):
            department_id = int(request.args.get('department'))
            semester = int(request.args.get('semester'))
            subjects = Subject.query.filter_by(
                department_id=department_id,
                semester=semester
            ).order_by('name').all()
            form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in subjects]
    
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', 'materials', filename)
            full_path = os.path.join(current_app.root_path, 'static', file_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Save the file
            file.save(full_path)
            
            # Create study material
            material = StudyMaterial(
                title=form.title.data,
                description=form.description.data,
                subject_id=form.subject.data,
                material_type=form.material_type.data,
                file_path=file_path,
                faculty_id=current_user.id
            )
            
            db.session.add(material)
            db.session.commit()
            
            flash('Study material uploaded successfully!', 'success')
            return redirect(url_for('study_material.list_materials'))
        else:
            flash('Invalid file type. Please upload PDF, DOC, DOCX, PPT, or PPTX files.', 'error')
    
    return render_template('study_material/modern_upload.html', 
                         title='Upload Study Material',
                         form=form)

@bp.route('/api/get_subjects')
@login_required
def get_subjects():
    department_id = request.args.get('department_id', type=int)
    semester = request.args.get('semester', type=int)
    
    if not department_id or not semester:
        return jsonify([])
        
    subjects = Subject.query.filter_by(
        department_id=department_id,
        semester=semester
    ).order_by('name').all()
    
    return jsonify([{
        'id': s.id,
        'name': f"{s.code} - {s.name}"
    } for s in subjects])

@bp.route('/materials')
def list_materials():
    # Get filter parameters
    selected_dept = request.args.get('department', type=int)
    selected_sem = request.args.get('semester', type=int)
    
    # Get all departments for the filter dropdown
    departments = Department.query.order_by('name').all()
    
    # Base query for materials
    query = StudyMaterial.query
    
    # Apply filters if selected
    if selected_dept:
        query = query.join(Subject).filter(Subject.department_id == selected_dept)
    if selected_sem:
        query = query.join(Subject).filter(Subject.semester == selected_sem)
    
    # Get materials
    materials = query.order_by(StudyMaterial.upload_date.desc()).all()
    
    return render_template('study_material/modern_list.html',
                         title='Study Materials',
                         materials=materials,
                         departments=departments,
                         selected_dept=selected_dept,
                         selected_sem=selected_sem)

@bp.route('/materials/<int:id>')
def view_material(id):
    material = StudyMaterial.query.get_or_404(id)
    return render_template('study_material/view.html', material=material)

@bp.route('/materials/<int:id>/download')
def download_material(id):
    material = StudyMaterial.query.get_or_404(id)
    directory = os.path.join(current_app.root_path, 'static', 'uploads', 'materials')
    return send_from_directory(directory, os.path.basename(material.file_path))
