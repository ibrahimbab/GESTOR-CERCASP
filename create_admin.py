from cercasp import create_app, db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    from cercasp.models import User  # Importar aquí para evitar error de fernet
    from sqlalchemy.exc import IntegrityError
    from cercasp.models import User
    username = "ibrahimb"
    password = "admincercasp2024"  # Cambia esta contraseña después de ingresar
    role = "admin"
    permissions = "all"
    existing = User.query.filter_by(username=username).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print(f"Usuario {username} eliminado para recrear.")
    hashed = generate_password_hash(password)
    print(f"Hash generado: {hashed}")
    user = User(
        username=username,
        password=hashed,
        role=role,
        permissions=permissions
    )
    db.session.add(user)
    try:
        db.session.commit()
        print(f"Usuario {username} creado con éxito. Contraseña: {password}")
    except IntegrityError:
        db.session.rollback()
        print(f"No se pudo crear el usuario {username} por un error de integridad.")
