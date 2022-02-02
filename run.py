from app.models import create_db
from app import create_app

if __name__ == "__main__":
    flask_app = create_app()
    create_db()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
