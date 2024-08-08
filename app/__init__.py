from flask import Flask
from flask_login import LoginManager
from .routes import main
from .db import pool
from app.users.models import User  # Make sure you import the User class
from app.users.routes import users_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    @login_manager.user_loader
    def load_user(user_id):
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return User(user['id'], user['username'], user['password'])
        return None

    app.register_blueprint(main)
    app.register_blueprint(users_bp)
    return app
