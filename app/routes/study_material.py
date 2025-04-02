import os
from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for, send_from_directory
from flask_security import login_required, current_user, roles_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.study_material import StudyMaterial
from app.models.subject import Subject
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
    # Populate subject choices
    form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in Subject.query.all()]
    
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create unique filename
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{current_user.id}_{form.subject.data}{ext}"
            
            # Save file
            file_path = os.path.join('uploads', 'materials', filename)
            os.makedirs(os.path.dirname(os.path.join(current_app.root_path, 'static', file_path)), exist_ok=True)
            file.save(os.path.join(current_app.root_path, 'static', file_path))
            
            # Create database entry
            material = StudyMaterial(
                title=form.title.data,
                description=form.description.data,
                material_type=form.material_type.data,
                file_path=file_path,
                subject_id=form.subject.data,
                faculty_id=current_user.id
            )
            db.session.add(material)
            db.session.commit()
            
            flash('Study material uploaded successfully!', 'success')
            return redirect(url_for('study_material.list_materials'))
            
    return render_template('study_material/upload.html', form=form)

@bp.route('/materials')
def list_materials():
    subject_id = request.args.get('subject_id', type=int)
    material_type = request.args.get('type')
    
    query = StudyMaterial.query
    if subject_id:
        query = query.filter_by(subject_id=subject_id)
    if material_type:
        query = query.filter_by(material_type=material_type)
        
    materials = query.order_by(StudyMaterial.upload_date.desc()).all()
    subjects = Subject.query.all()
    
    return render_template('study_material/list.html', 
                         materials=materials, 
                         subjects=subjects,
                         current_subject=subject_id,
                         current_type=material_type)

@bp.route('/materials/<int:id>')
def view_material(id):
    material = StudyMaterial.query.get_or_404(id)
    return render_template('study_material/view.html', material=material)

@bp.route('/materials/<int:id>/download')
def download_material(id):
    material = StudyMaterial.query.get_or_404(id)
    directory = os.path.join(current_app.root_path, 'static', 'uploads', 'materials')
    return send_from_directory(directory, os.path.basename(material.file_path))
