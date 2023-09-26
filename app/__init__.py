import os
from flask import Flask, make_response, jsonify

from . import db

mongo = db.init_db()
def create_app(test_config=None):
  
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping()
   

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.errorhandler(400)
    def not_found(error):
        return make_response(jsonify(error='Not found'), 400)

    @app.errorhandler(500)
    def error_500(error):
        return make_response({}, 500)

    db.get_db(mongo=mongo, app=app)
   
    
        
    from   app.api.auth import auth
    from app.api.admin import admin_bp

    app.register_blueprint(auth, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

create_app()
