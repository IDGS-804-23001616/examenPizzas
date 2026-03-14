class Config:
    SECRET_KEY = "clave_secreta_pizzeria"
    SESSION_COOKIE_SECURE = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:23010@localhost/pizzas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

