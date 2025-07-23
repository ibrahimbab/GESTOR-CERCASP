from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from pyotp import TOTP
from ..forms import LoginForm, UserForm
from ..models import User
from ..utils import log_action, create_user
from .. import limiter
from flask_babel import _

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # Si quieres activar 2FA solo para usuarios con otp_secret, descomenta el siguiente bloque:
            # if user.otp_secret:
            #     try:
            #         otp = TOTP(user.otp_secret)
            #         if otp.verify(form.otp.data):
            #             login_user(user)
            #             log_action('Inició sesión', details=f'IP: {request.remote_addr}')
            #             return redirect(url_for('dashboard.dashboard'))
            #         else:
            #             flash(_('Código 2FA inválido.'), 'danger')
            #     except Exception:
            #         flash(_('Código 2FA inválido.'), 'danger')
            #     return render_template('login.html', form=form)
            login_user(user)
            log_action('Inició sesión', details=f'IP: {request.remote_addr}')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(_('Credenciales incorrectas.'), 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    log_action('Cerró sesión')
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required  # Only admins
def register():
    form = UserForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.password.data, form.role.data, form.otp_secret.data)
        flash(_('Usuario registrado exitosamente.'), 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('register.html', form=form)
