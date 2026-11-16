from os import path, environ

basedir = path.abspath(path.dirname(__file__))

CORS_ORIGINS = ["http://localhost:9000"]

SQLALCHEMY_DATABASE_URI = "sqlite:///./database.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False

IS_PROD = environ.get("APP_ENV") == "production"

# gestion Set-Cookie
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = IS_PROD
SESSION_COOKIE_SAMESITE = "Strict"

# gestion des JWT
JWT_SECRET = environ.get("JWT_SECRET")
JWT_ALGORITHM = "HS256" # algo de chiffrage
JWT_TTL = 3600 # durée de vie du JWT en secondes
