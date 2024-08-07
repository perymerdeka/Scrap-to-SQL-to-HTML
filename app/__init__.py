from flask import Flask, g
from .routes import main
from .db import pool

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    
    @app.before_request
    def before_request():
        g.db = pool.get_connection()
    
    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()
    
    return app
