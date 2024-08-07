from flask import Flask, g
from .routes import main
from .db import pool
from flask_login import LoginManager



def create_app():
    app = Flask(__name__)
    app.secret_key ="your_secret_key"
    app.register_blueprint(main)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login.manager.login_view = 'main.login'
    
    @login_manager.user_loader
    def load_user(id):
        connection = pool.get.connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return User(user['id'], user['username'], user['password'])
        return None # Specify the name of the login route


    @app.before_request
    def before_request():
        g.db = pool.get_connection()
    
    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()
    
    return app
