from cercasp import create_app
from cercasp.models import db, User

# Configura la aplicación
app = create_app()

username = "ibrahimb"

with app.app_context():
    # Busca al usuario
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"Usuario encontrado: {user.username}, Role: {user.role}")
    else:
        print(f"Usuario {username} no encontrado.")
