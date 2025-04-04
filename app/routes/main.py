from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.result import Result
from app.models.user import User

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard/')
@login_required
def dashboard():
    if current_user.has_role('admin'):
        # Get stats for admin dashboard
        stats = {
            'students': User.query.filter(User.roles.any(name='student')).count(),
            'total_results': Result.query.count(),
            'recent_results': Result.query.order_by(Result.declaration_date.desc()).limit(5).all()
        }
        return render_template('dashboard/admin.html', stats=stats)
    elif current_user.has_role('student'):
        # Get latest result for the student
        latest_result = Result.query.filter_by(
            student_id=current_user.id
        ).order_by(Result.declaration_date.desc()).first()
        
        return render_template('dashboard/student.html', latest_result=latest_result)
    else:
        return render_template('dashboard/default.html')

@bp.route('/results')
@login_required
def view_results():
    if current_user.has_role('student'):
        results = Result.query.filter_by(student_id=current_user.id).order_by(Result.declaration_date.desc()).all()
        return render_template('student/results.html', results=results)
    else:
        flash('You do not have permission to view results.', 'error')
        return redirect(url_for('main.dashboard'))

@bp.route('/results/<int:result_id>')
@login_required
def view_result_details(result_id):
    if current_user.has_role('student'):
        result = Result.query.filter_by(id=result_id, student_id=current_user.id).first_or_404()
        return render_template('student/result_details.html', result=result)
    else:
        flash('You do not have permission to view this result.', 'error')
        return redirect(url_for('main.dashboard'))
