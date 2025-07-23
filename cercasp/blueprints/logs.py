from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from cercasp.models import Log, User
from cercasp import db

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs')
@login_required
def list_logs():
    if current_user.username != 'ibrahimb':
        flash('Acceso denegado: solo el usuario autorizado puede ver la bitácora.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    logs = Log.query.order_by(Log.timestamp.desc()).limit(200).all()
    return render_template('list_logs.html', logs=logs)
