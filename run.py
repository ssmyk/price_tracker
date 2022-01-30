from app import create_app
import os
from app import db

def create_db():
    if not os.path.exists('users.sqlite3'):
        with app.app_context():
            db.create_all()

if __name__ == '__main__':
    app = create_app()
    create_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
