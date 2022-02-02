class DBConfig:
    DB_NAME = 'users.sqlite3'

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DBConfig.DB_NAME}"
    SECRET_KEY = "temporary_secret_key"
