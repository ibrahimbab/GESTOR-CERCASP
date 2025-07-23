import os
from cryptography.fernet import Fernet

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/cercasp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    CACHE_TYPE = 'simple'
    BABEL_DEFAULT_LOCALE = 'es'
    LANGUAGES = ['es', 'en']
    ENCRYPTION_KEY = b'l1aInE2Vkx2xrlotus-1qwYG0ea9mi9DTnATPHlAoR8='
