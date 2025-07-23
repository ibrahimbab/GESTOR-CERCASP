from werkzeug.security import generate_password_hash
from cercasp import create_app
from cercasp.models import db, User

# Configura la aplicación
app = create_app()

# Nueva contraseña
new_password = "nueva_contraseña_segura"
username = "ibrahimb"

with app.app_context():
    # Busca al usuario
    user = User.query.filter_by(username=username).first()
    if user:
        # Actualiza la contraseña
        user.password = generate_password_hash(new_password)
        db.session.commit()
        print(f"Contraseña actualizada para el usuario {username}.")
    else:
        print(f"Usuario {username} no encontrado.")
