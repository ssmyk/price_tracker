from decouple import config

class DBConfig:
    DB_NAME = config('DB_NAME')

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DBConfig.DB_NAME}"
    SECRET_KEY = config('SECRET_KEY')
