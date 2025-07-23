from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/cambiar-fondo', methods=['GET', 'POST'])
@login_required
def cambiar_fondo():
    if current_user.username != 'ibraehimb':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        file = request.files.get('logo')
        if file and file.filename:
            path = os.path.join('cercasp', 'static', 'img', 'logo_cercasp.png')
            file.save(path)
            flash('Logo actualizado correctamente.', 'success')
            return redirect(url_for('admin.cambiar_fondo'))
        else:
            flash('Selecciona un archivo válido.', 'danger')
    return render_template('admin_cambiar_fondo.html')
