from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, PasswordField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class InternForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    age = IntegerField('Edad', validators=[DataRequired(), NumberRange(min=18)])
    gender = SelectField('Género', choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    entry_date = DateField('Fecha de Ingreso', validators=[DataRequired()])
    initial_drug = StringField('Droga Inicial')
    wellbeing_score = IntegerField('Puntuación de Bienestar Inicial', validators=[DataRequired(), NumberRange(min=0, max=100)])
    weekly_fee = FloatField('Cuota Semanal', validators=[DataRequired(), NumberRange(min=0)])
    contact_name = StringField('Nombre de Contacto', validators=[DataRequired()])
    contact_number = StringField('Número de Contacto', validators=[DataRequired()])
    consent_signed = DateField('Fecha de Consentimiento')
    submit = SubmitField('Guardar Interno')

class PaymentForm(FlaskForm):
    intern_id = IntegerField('ID Interno', validators=[DataRequired()])
    week_number = IntegerField('Número de Semana', validators=[DataRequired()])
    expected_amount = FloatField('Monto Esperado', validators=[DataRequired()])
    paid_amount = FloatField('Monto Pagado', validators=[DataRequired()])
    payment_date = DateField('Fecha de Pago')
    submit = SubmitField('Registrar Pago')

class ProgressForm(FlaskForm):
    intern_id = IntegerField('ID Interno', validators=[DataRequired()])
    week = IntegerField('Semana', validators=[DataRequired()])
    medical_note = TextAreaField('Nota Médica')
    medical_evaluation = TextAreaField('Evaluación Médica')
    psycho_note = TextAreaField('Nota Psicológica')
    psychological_evaluation = TextAreaField('Evaluación Psicológica')
    wellbeing_score = IntegerField('Puntuación de Bienestar', validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Registrar Progreso')

class InventoryForm(FlaskForm):
    name = StringField('Nombre del Medicamento', validators=[DataRequired()])
    quantity = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    expiration_date = DateField('Fecha de Expiración', validators=[DataRequired()])
    submit = SubmitField('Guardar Inventario')

class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    role = SelectField('Rol', choices=[('admin', 'Administrador'), ('medico', 'Médico'), ('psico', 'Psicólogo'), ('finanzas', 'Finanzas')])
    otp_secret = StringField('Secreto 2FA', validators=[DataRequired(), Length(min=16, max=16)])
    submit = SubmitField('Registrar Usuario')
