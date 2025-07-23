from werkzeug.security import generate_password_hash
from cercasp import create_app
from cercasp.models import db, User

# Configura la aplicación
app = create_app()

# Datos del nuevo usuario
username = "ibrahimb"
password = "nueva_contraseña_segura"
role = "admin"  # Cambiar según sea necesario

with app.app_context():
    # Verifica si el usuario ya existe
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"El usuario {username} ya existe.")
    else:
        # Crea un nuevo usuario
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"Usuario {username} creado exitosamente.")
