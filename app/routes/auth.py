from flask import Blueprint, render_template, redirect, url_for, flash, request
from urllib.parse import urlparse
from flask_security import current_user, login_required, logout_user, login_user
from flask_security.utils import hash_password, verify_password
from ..extensions import db, security
from ..forms.auth import ExtendedRegisterForm, LoginForm
from ..forms.profile import EditProfileForm
from ..models.user import User, Role
from ..models.department import Department

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = ExtendedRegisterForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()
        if not role:
            role = Role(name=form.role.data)
            db.session.add(role)
        
        # Get the department
        department = Department.query.get(form.department.data) if form.department.data != 0 else None
        
        user = User(
            email=form.email.data,
            password=hash_password(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            department_id=department.id if department else None,
            active=True,
            roles=[role]
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not verify_password(form.password.data, user.password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        if not user.is_approved and not user.has_role('admin'):
            flash('Your account is pending approval.', 'error')
            return redirect(url_for('auth.login'))
        if not user.has_role(form.role.data):
            flash('You do not have permission to login with this role.', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('dashboard.index')
        flash('Logged in successfully.', 'success')
        return redirect(next_page)
    return render_template('security/login_user.html', login_user_form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.department_id = form.department.data if form.department.data != 0 else None
        
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.edit_profile'))
    
    return render_template('auth/profile.html', form=form)
