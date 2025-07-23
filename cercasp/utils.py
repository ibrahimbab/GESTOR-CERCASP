from . import db, fernet
from .models import User, Log
from flask_login import current_user
from datetime import datetime
from werkzeug.security import generate_password_hash
import os
import logging
from flask import current_app

def log_action(action, details=None):
    log = Log(user_id=current_user.id if current_user.is_authenticated else None, action=action, details=details)
    db.session.add(log)
    db.session.commit()
    current_app.logger.info(f'Acción: {action} - Detalles: {details}')

def backup_db():
    try:
        db.session.commit()
        timestamp = datetime.now().strftime('%Y%m%d')
        os.system(f'cp instance/cercasp.db instance/backup_cercasp_{timestamp}.db')
        current_app.logger.info("Backup de DB completado.")
    except Exception as e:
        current_app.logger.error(f'Error en backup_db: {str(e)}')

def send_notification(contact, message):
    current_app.logger.info(f"Enviando notificación: {message} a {contact}")

def create_user(username, password, role, otp_secret):
    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw, role=role, otp_secret=otp_secret)
    db.session.add(user)

    db.session.commit()
