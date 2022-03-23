from decouple import config

class DBConfig:
    DB_NAME = config('DB_NAME')
    DB_USERNAME = config('DB_USERNAME')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_SERVER = config('DB_SERVER')
    DB_SERVER_PORT = config('DB_SERVER_PORT')

class Config:
    #SQLALCHEMY_DATABASE_URI = f"sqlite:///{DBConfig.DB_NAME}"
    #'postgresql://postgres:123456@localhost:5432/notebook'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DBConfig.DB_USERNAME}:{DBConfig.DB_PASSWORD}@{DBConfig.DB_SERVER}:{DBConfig.DB_SERVER_PORT}/{DBConfig.DB_NAME}'
    SECRET_KEY = config('SECRET_KEY')
