# Cercasp

Cercasp es un sistema web diseñado para la gestión de internos, pagos y progreso, con características avanzadas de autenticación y autorización.

## Características principales

### 1. Autenticación y Autorización
- Manejo de usuarios con roles y permisos.
- Inicio de sesión y registro de usuarios.
- Soporte para autenticación de dos factores (2FA).

### 2. Gestión de Internos
- Registro y seguimiento de internos con datos como edad, género, progreso y contacto.

### 3. Pagos
- Gestión de pagos semanales, incluyendo montos esperados, pagados y pendientes.

### 4. Progreso
- Seguimiento del progreso de los internos.

### 5. Interfaz Web
- Plantillas HTML para diferentes vistas como login, dashboard, inventario, y más.

### 6. Modelos de Base de Datos
- Modelos definidos para usuarios, internos, pagos y progreso.

### 7. Utilidades
- Funciones para cifrar datos sensibles como contactos.

### 8. Estructura Modular
- Uso de Blueprints de Flask para organizar el código en módulos como `auth`, `dashboard`, `inventory`, etc.

## Requisitos
- Python 3.7+
- Flask y extensiones relacionadas (ver `requirements.txt`)

## Instalación
1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura la base de datos y ejecuta la aplicación:
   ```bash
   flask db upgrade
   python app.py
   ```

## Uso
- Accede a la aplicación en `http://localhost:5000`.
- Usa las credenciales de administrador para iniciar sesión o registra nuevos usuarios.

## Contribuciones
¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT.
