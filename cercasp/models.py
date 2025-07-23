from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    permissions = db.Column(db.Text)
    otp_secret = db.Column(db.String(16))  # For 2FA

class Intern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    entry_date = db.Column(db.Date, nullable=False)
    initial_drug = db.Column(db.String(100))
    wellbeing_score = db.Column(db.Integer, nullable=False)
    weekly_fee = db.Column(db.Float, nullable=False)
    contact_name_enc = db.Column(db.Text)  # Encrypted
    contact_number_enc = db.Column(db.Text)  # Encrypted
    consent_signed = db.Column(db.Date)

    def set_contact(self, name, number):
        from flask import current_app
        fernet = getattr(current_app, 'fernet', None)
        if fernet is None and hasattr(current_app, 'extensions'):
            fernet = current_app.extensions.get('fernet')
        if fernet is None:
            raise RuntimeError('Fernet no está inicializado en la app')
        self.contact_name_enc = fernet.encrypt(name.encode()).decode()
        self.contact_number_enc = fernet.encrypt(number.encode()).decode()

    def get_contact(self):
        try:
            from flask import current_app
            fernet = getattr(current_app, 'fernet', None)
            if fernet is None and hasattr(current_app, 'extensions'):
                fernet = current_app.extensions.get('fernet')
            if fernet is None:
                raise RuntimeError('Fernet no está inicializado en la app')
            return fernet.decrypt(self.contact_name_enc.encode()).decode(), fernet.decrypt(self.contact_number_enc.encode()).decode()
        except Exception:
            return None, None

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('intern.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    expected_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0)
    payment_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    pending_amount = db.Column(db.Float, default=0)
    __table_args__ = (db.UniqueConstraint('intern_id', 'week_number', name='unique_payment'),)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('intern.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    medical_note = db.Column(db.Text)
    medical_evaluation = db.Column(db.Text)
    psycho_note = db.Column(db.Text)
    psychological_evaluation = db.Column(db.Text)
    payment_status = db.Column(db.String(20), default='pending')
    wellbeing_score = db.Column(db.Integer)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='logs')
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)

class MedInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

# Indexes
db.Index('idx_progress_intern_week', Progress.intern_id, Progress.week)
db.Index('idx_payment_intern_week', Payment.intern_id, Payment.week_number)
db.Index('idx_intern_entry', Intern.entry_date)
db.Index('idx_log_timestamp', Log.timestamp)
