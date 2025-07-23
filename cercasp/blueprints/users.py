from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from cercasp.models import User
from cercasp import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def list_users():
    if current_user.username != 'ibrahimb':
        flash('Acceso denegado: solo el usuario autorizado puede gestionar usuarios.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    users = User.query.all()
    return render_template('list_users.html', users=users)

@users_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.username != 'ibrahimb':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('users.list_users'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe.', 'warning')
            return redirect(url_for('users.add_user'))
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('add_user.html')

@users_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if current_user.username != 'ibrahimb':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('users.list_users'))
    user = User.query.get_or_404(id)
    if user.username == 'ibrahimb':
        flash('No puedes eliminar el usuario principal.', 'danger')
        return redirect(url_for('users.list_users'))
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('users.list_users'))
