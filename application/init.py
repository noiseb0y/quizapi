from flask import Flask, jsonify
import redis
import config
import db
import traceback
import routes

r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

def init_app():
    app = Flask(__name__)
    
    print('''about to go into "with app.app_context()"''')
    with app.app_context():
        try:
            db.init_db(r)
        except:
            traceback.print_exc()
            
    app.register_blueprint(routes.route_blueprint) 
    app.register_error_handler(404, routes.resource_not_found)
    
    return app